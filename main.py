from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from fastapi import FastAPI
import aiosqlite  # Асинхронная библиотека для работы с SQLite
import redis
import logging
from loguru import logger
from sentry_sdk import init as sentry_init
from typing import Optional
from aiogram.filters import Command
from tokens import TOKEN
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from bot.services.db_service import DatabaseService


# Инициализация FastAPI приложения
app = FastAPI()

# Настройка Sentry для мониторинга ошибок
# sentry_init("YOUR_SENTRY_DSN")

# Инициализация Redis для кэширования
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Инициализация Telegram-бота
bot = Bot(token=TOKEN)
dp = Dispatcher()
DATABASE_PATH = "clinic.db"

# Настройка логирования
logger.add("logs/bot.log", rotation="10 MB", level="INFO")

# Инициализация базы данных
async def init_database():
    """
    Инициализация базы данных: выполнение SQL-скрипта из файла init_db.sql.
    """
    db = DatabaseService(DATABASE_PATH)
    with open("migrations/init_db.sql", "r") as f:
        sql_script = f.read()
    await db.execute_query(sql_script)
    print("Database initialized successfully.")

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    # Создаем билдер для клавиатуры
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="📞 Отправить контакт", request_contact=True),
        KeyboardButton(text="ℹ️ Информация")
    )
    builder.adjust(1)  # Каждая кнопка на новой строке

    # Получаем объект ReplyKeyboardMarkup
    keyboard = builder.as_markup(resize_keyboard=True)

    # Отправляем сообщение с клавиатурой
    await message.answer("Добро пожаловать! Выберите действие:", reply_markup=keyboard)

# Обработчик контакта
@dp.message(F.content_type == "contact")
async def handle_contact(message: types.Message):
    """
    Обработка контакта пользователя для авторизации.
    """
    phone_number = extract_phone_number(message.contact.phone_number)
    if not phone_number:
        await message.answer("Не удалось распознать номер телефона. Попробуйте еще раз.")
        return
    
    user = await authenticate_user(phone_number)
    if user:
        await message.answer(f"Добро пожаловать, {user['full_name']}!")
        # Здесь можно сохранить ID пользователя Telegram в базе данных
    else:
        await message.answer("Пользователь с таким номером не найден. Свяжитесь с администратором.")

# Вспомогательная функция для извлечения номера телефона
def extract_phone_number(phone: str) -> str:
    """
    Извлекает номер телефона из контакта и возвращает его в международном формате.
    """
    try:
        from phonenumbers import parse, is_valid_number
        parsed_phone = parse(phone, None)
        if is_valid_number(parsed_phone):
            return f"+{parsed_phone.country_code}{parsed_phone.national_number}"
    except Exception as e:
        logger.error(f"Ошибка при парсинге номера телефона: {e}")
    return None

# Вспомогательная функция для аутентификации пользователя
async def authenticate_user(phone_number: str) -> dict:
    """
    Аутентифицирует пользователя по номеру телефона.
    Возвращает данные пользователя из базы данных.
    """
    if not phone_number:
        return None
    
    query = """
    SELECT id, full_name, email, date_of_birth
    FROM patients
    WHERE phone_number = ?
    """
    try:
        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(query, (phone_number,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return {
                        "id": row[0],
                        "full_name": row[1],
                        "email": row[2],
                        "date_of_birth": row[3]
                    }
    except Exception as e:
        logger.error(f"Ошибка при аутентификации пользователя: {e}")
    return None


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio

    # Инициализация базы данных
    asyncio.run(init_database())

    # Запуск бота
    asyncio.run(main())