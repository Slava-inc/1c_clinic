# bot/handlers/auth.py
from aiogram import Router, F
from aiogram.types import Message
from phonenumbers import parse, is_valid_number
from bot.services.db_service import DatabaseService
from bot.keyboards.builder import KeyboardBuilder

router = Router()

@router.message(F.content_type == "contact")
async def handle_contact(message: Message, db: DatabaseService):
    phone_number = extract_phone_number(message.contact.phone_number)
    if not phone_number:
        await message.answer("Не удалось распознать номер телефона.")
        return

    user = await db.fetch_one("SELECT * FROM patients WHERE phone_number = ?", (phone_number,))
    if user:
        await message.answer(f"Добро пожаловать, {user['full_name']}!")
    else:
        await message.answer(
            "Вы не зарегистрированы. Хотите зарегистрироваться?",
            reply_markup=KeyboardBuilder.build_confirmation()
        )

def extract_phone_number(phone: str) -> str:
    try:
        parsed_phone = parse(phone, None)
        if is_valid_number(parsed_phone):
            return f"+{parsed_phone.country_code}{parsed_phone.national_number}"
    except Exception:
        pass
    return None