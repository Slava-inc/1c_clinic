from aiogram import Router, F
from aiogram.types import Message
from bot.services.db_service import DatabaseService
from bot.services.mis_service import MISService
import asyncio

notifications_router = Router()

# Проверка и отправка уведомлений
async def send_notifications(db: DatabaseService, mis: MISService):
    while True:
        # Получаем ближайшие записи на прием
        appointments = await db.fetch_all(
            """
            SELECT patient_id, appointment_date
            FROM appointments
            WHERE appointment_date BETWEEN datetime('now') AND datetime('now', '+24 hours')
            """
        )
        for appointment in appointments:
            patient_id = appointment["patient_id"]
            appointment_date = appointment["appointment_date"]

            # Отправляем напоминание
            user = await db.fetch_one(
                "SELECT telegram_id FROM patients WHERE id = ?", (patient_id,)
            )
            if user and user["telegram_id"]:
                await mis.send_notification(
                    chat_id=user["telegram_id"],
                    text=f"Напоминаем о приеме {appointment_date}. Подготовьтесь заранее."
                )

        # Ждем час перед следующей проверкой
        await asyncio.sleep(3600)

@notifications_router.message(F.text == "Тест уведомлений")
async def test_notifications(message: Message, db: DatabaseService, mis: MISService):
    await send_notifications(db, mis)
    await message.answer("Тест уведомлений завершен.")