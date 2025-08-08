from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from phonenumbers import parse, is_valid_number
from bot.services.db_service import DatabaseService
from bot.keyboards.builder import KeyboardBuilder

# Создаем роутер для обработки событий
auth_router = Router()  # Определяем auth_router

# Класс для управления состояниями FSM
class RegistrationState(StatesGroup):
    waiting_for_confirmation = State()  # Ожидание подтверждения регистрации
    waiting_for_full_name = State()    # Ожидание ввода ФИО
    waiting_for_date_of_birth = State()  # Ожидание ввода даты рождения

@auth_router.message(F.text == "/start")
async def start_command(message: Message):
    """
    Обработчик команды /start.
    Предлагает пользователю привязать аккаунт Telegram к карте пациента.
    """
    await message.answer(
        "Добро пожаловать! Чтобы начать, отправьте ваш контакт.",
        reply_markup=KeyboardBuilder.build_contact_request()
    )

# Обработчик контакта
@auth_router.message(F.content_type == "contact")
async def handle_contact(message: Message, state: FSMContext):
    db = DatabaseService("clinic.db")  # Создаем экземпляр DatabaseService
    phone_number = extract_phone_number(message.contact.phone_number)
    if not phone_number:
        await message.answer("Не удалось распознать номер телефона. Попробуйте еще раз.")
        return

    # Проверяем, зарегистрирован ли пользователь
    user = await db.fetch_one("SELECT * FROM patients WHERE phone_number = ?", (phone_number,))
    if user:
        # Привязка Telegram ID к пациенту
        await db.execute_query(
            "UPDATE patients SET telegram_id = ? WHERE id = ?", 
            (message.from_user.id, user[0])
        )
        await message.answer(f"Добро пожаловать, {user[1]}!",
                             reply_markup=KeyboardBuilder.build_main_menu()
                             )
    else:
        # Предложение зарегистрироваться
        await message.answer(
            "Вы не зарегистрированы. Хотите зарегистрироваться?",
            reply_markup=KeyboardBuilder.build_confirmation()
        )
        # Сохраняем номер телефона в состоянии FSM
        await state.update_data(phone_number=phone_number)
        await state.set_state(RegistrationState.waiting_for_confirmation)

# Обработчик подтверждения регистрации
@auth_router.message(F.text.in_(["Да", "Нет"]), RegistrationState.waiting_for_confirmation)
async def handle_registration_confirmation(message: Message, state: FSMContext):
    data = await state.get_data()
    phone_number = data.get("phone_number")

    if message.text == "Да":
        await message.answer("Введите ваше ФИО:", reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegistrationState.waiting_for_full_name)
    else:
        await message.answer("Регистрация отменена.", reply_markup=ReplyKeyboardRemove())
        await state.clear()

# Обработчик ввода ФИО
@auth_router.message(RegistrationState.waiting_for_full_name)
async def handle_full_name(message: Message, state: FSMContext):
    full_name = message.text.strip()
    if not full_name:
        await message.answer("ФИО не может быть пустым. Попробуйте снова.")
        return

    # Сохраняем ФИО в состоянии FSM
    await state.update_data(full_name=full_name)
    await message.answer("Введите вашу дату рождения (в формате ГГГГ-ММ-ДД):")
    await state.set_state(RegistrationState.waiting_for_date_of_birth)

# Обработчик ввода даты рождения
@auth_router.message(RegistrationState.waiting_for_date_of_birth)
async def handle_date_of_birth(message: Message, state: FSMContext):
    db = DatabaseService("clinic.db")
    date_of_birth = message.text.strip()
    if not validate_date(date_of_birth):
        await message.answer("Дата рождения указана в неверном формате. Попробуйте снова (ГГГГ-ММ-ДД).")
        return

    # Получаем данные из состояния FSM
    data = await state.get_data()
    full_name = data.get("full_name")
    phone_number = data.get("phone_number")

    # Регистрация пользователя
    await db.execute_query(
        """
        INSERT INTO patients (full_name, phone_number, date_of_birth, telegram_id)
        VALUES (?, ?, ?, ?)
        """,
        (full_name, phone_number, date_of_birth, message.from_user.id)
    )

    await message.answer(f"Вы успешно зарегистрированы, {full_name}!")

    # Очищаем состояние FSM
    await state.clear()

# Вспомогательные функции
def extract_phone_number(phone: str) -> str:
    try:
        parsed_phone = parse(phone, None)
        if is_valid_number(parsed_phone):
            return f"+{parsed_phone.country_code}{parsed_phone.national_number}"
    except Exception:
        pass
    return None

def validate_date(date: str) -> bool:
    try:
        from datetime import datetime
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False