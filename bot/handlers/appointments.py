from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot.services.db_service import DatabaseService
from bot.keyboards.builder import KeyboardBuilder

appointments_router = Router()

@appointments_router.callback_query(F.data == "schedule_appointment")
async def schedule_appointment(callback: CallbackQuery):
    db = DatabaseService('clinic.db')
    # Получаем список доступных врачей
    doctors = await db.fetch_all("SELECT id, name, specialization FROM doctors")
    if not doctors:
        await callback.answer("К сожалению, сейчас нет доступных врачей.")
        return
    else:
        results = []
        for doctor in doctors:
            result = {'id': doctor[0], 'name': doctor[1], 'specialization': doctor[2]}
            results.append(result)


    # Формируем клавиатуру с врачами
    await callback.answer()
    keyboard = KeyboardBuilder.build_doctors_keyboard(results)
    await callback.message.answer("Выберите врача:", reply_markup=keyboard)

@appointments_router.callback_query(F.data.startswith("doctor_"))
async def select_doctor(callback: CallbackQuery):
    db = DatabaseService('clinic.db')
    doctor_id = int(callback.data.split("_")[1])
    # Получаем расписание врача
    schedule = await db.fetch_all(
        "SELECT appointment_date FROM schedule WHERE doctor_id = ? AND status = 'free'",
        (doctor_id,)
    )
    if not schedule:
        await callback.message.answer("У выбранного врача нет свободных слотов.")
        return

    # Преобразуем список кортежей в список словарей
    schedule = [{"appointment_date": slot[0], "doctor_id": doctor_id} for slot in schedule]

    # Формируем клавиатуру со свободными слотами
    keyboard = KeyboardBuilder.build_schedule_keyboard(schedule)
    await callback.message.answer("Выберите удобное время:", reply_markup=keyboard)

@appointments_router.callback_query(F.data.startswith("slot_"))
async def confirm_appointment(callback: CallbackQuery):
    db = DatabaseService('clinic.db')
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

    await callback.message.answer(f"Вы успешно записаны на {appointment_date}!",
                                  reply_markup=KeyboardBuilder.build_main_menu())

