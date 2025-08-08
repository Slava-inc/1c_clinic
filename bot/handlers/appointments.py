from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot.services.db_service import DatabaseService
from bot.keyboards.builder import KeyboardBuilder

appointments_router = Router()

@appointments_router.message(F.text == "Записаться на прием")
async def schedule_appointment(message: Message, db: DatabaseService):
    # Получаем список доступных врачей
    doctors = await db.fetch_all("SELECT id, name, specialization FROM doctors")
    if not doctors:
        await message.answer("К сожалению, сейчас нет доступных врачей.")
        return

    # Формируем клавиатуру с врачами
    keyboard = KeyboardBuilder.build_doctors_keyboard(doctors)
    await message.answer("Выберите врача:", reply_markup=keyboard)

@appointments_router.callback_query(F.data.startswith("doctor_"))
async def select_doctor(callback: CallbackQuery, db: DatabaseService):
    doctor_id = int(callback.data.split("_")[1])
    # Получаем расписание врача
    schedule = await db.fetch_all(
        "SELECT appointment_date FROM schedule WHERE doctor_id = ? AND status = 'free'",
        (doctor_id,)
    )
    if not schedule:
        await callback.message.answer("У выбранного врача нет свободных слотов.")
        return

    # Формируем клавиатуру со свободными слотами
    keyboard = KeyboardBuilder.build_schedule_keyboard(schedule)
    await callback.message.answer("Выберите удобное время:", reply_markup=keyboard)

@appointments_router.callback_query(F.data.startswith("slot_"))
async def confirm_appointment(callback: CallbackQuery, db: DatabaseService):
    slot_data = callback.data.split("_")
    doctor_id = int(slot_data[1])
    appointment_date = slot_data[2]

    # Записываем пациента на прием
    patient_id = callback.from_user.id
    await db.execute_query(
        "INSERT INTO appointments (patient_id, doctor_id, appointment_date) VALUES (?, ?, ?)",
        (patient_id, doctor_id, appointment_date)
    )
    await db.execute_query(
        "UPDATE schedule SET status = 'busy' WHERE doctor_id = ? AND appointment_date = ?",
        (doctor_id, appointment_date)
    )

    await callback.message.answer(f"Вы успешно записаны на {appointment_date}!")