# bot/handlers/home_visit.py
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.keyboards.builder import KeyboardBuilder
from bot.services.db_service import DatabaseService
import re

# Создаем маршрутизатор
home_visit_router = Router()

# Определяем состояния
class HomeVisitStates(StatesGroup):
    """
    Состояния для процесса вызова врача на дом.
    """
    waiting_for_specialization = State("waiting_for_specialization")
    waiting_for_address = State("waiting_for_address")
    waiting_for_time = State("waiting_for_time")

# Обработчик нажатия кнопки "Вызов врача на дом"
@home_visit_router.callback_query(F.data == "home_visit")
async def request_specialization(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик нажатия кнопки "Вызов врача на дом".
    Отправляет список доступных специализаций.
    """
    db = DatabaseService('clinic.db')
    specializations = await db.fetch_all("SELECT id, name FROM specializations WHERE home_visit_available = 1")
    if not specializations:
        await callback.message.answer("К сожалению, сейчас нет доступных специализаций для вызова врача на дом.")
        return
    # Преобразуем список кортежей в список словарей
    specializations = [{"id": spec[0], "name": spec[1]} for spec in specializations]

    keyboard = KeyboardBuilder.build_home_visit_specializations(specializations)
    await callback.message.answer("Выберите специализацию врача:", reply_markup=keyboard)
    await state.set_state(HomeVisitStates.waiting_for_specialization)

# Обработчик выбора специализации врача
@home_visit_router.callback_query(HomeVisitStates.waiting_for_specialization)
async def request_address(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик выбора специализации врача.
    Запрашивает адрес пациента.
    """
    specialization_id = int(callback.data.split("_")[3])
    await state.update_data(specialization_id=specialization_id)
    await callback.message.answer("Введите адрес, по которому врач должен прибыть:")
    await state.set_state(HomeVisitStates.waiting_for_address)

# Обработчик ввода адреса
@home_visit_router.message(HomeVisitStates.waiting_for_address)
async def request_time(message: Message, state: FSMContext):
    """
    Обработчик ввода адреса.
    Запрашивает предпочтительное время визита.
    """
    address = message.text.strip()
    await state.update_data(address=address)
    await message.answer("Введите предпочтительное время визита (например, 14:00):")
    await state.set_state(HomeVisitStates.waiting_for_time)

# Обработчик ввода времени
@home_visit_router.message(HomeVisitStates.waiting_for_time)
async def confirm_home_visit(message: Message, state: FSMContext):
    """
    Обработчик ввода времени.
    Подтверждает заявку на вызов врача на дом.
    """
    db = DatabaseService('clinic.db')
    time = message.text.strip()
    data = await state.get_data()
    specialization_id = data.get("specialization_id")
    address = data.get("address")

    # Проверка формата времени
    if not is_valid_time(time):
        await message.answer("Некорректный формат времени. Пожалуйста, введите время в формате HH:MM.")
        return

    # Создание заявки в МИС 1С
    patient_id = message.from_user.id  # Используем Telegram ID как ID пациента
    home_visit_id = await db.execute_query(
        "INSERT INTO home_visits (patient_id, specialization_id, address, preferred_time, status) VALUES (?, ?, ?, ?, ?)",
        (patient_id, specialization_id, address, time, "pending")
    )

    # Подтверждение заявки
    await message.answer(
        f"Ваша заявка принята. Врач прибудет по адресу: {address}, в {time}.",
        reply_markup=KeyboardBuilder.build_main_menu()
    )
    await state.clear()

# Функция проверки времени
def is_valid_time(time: str) -> bool:
    """
    Проверяет корректность формата времени (HH:MM).
    
    :param time: Время в формате строки.
    :return: True, если формат корректен, иначе False.
    """
    pattern = r"^([01]?\d|2[0-3]):[0-5]\d$"
    return bool(re.match(pattern, time))