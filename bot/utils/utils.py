import re
from phonenumbers import parse, is_valid_number

def extract_phone_number(message_text: str) -> str:
    """
    Извлекает номер телефона из текста сообщения.
    Возвращает номер в международном формате (например, +79991234567).
    """
    # Регулярное выражение для поиска номера телефона
    phone_pattern = r'(\+?\d{10,15})'
    match = re.search(phone_pattern, message_text)
    
    if match:
        raw_phone = match.group(1)
        try:
            # Парсим номер с помощью phonenumbers
            parsed_phone = parse(raw_phone, None)
            if is_valid_number(parsed_phone):
                return f"+{parsed_phone.country_code}{parsed_phone.national_number}"
        except Exception as e:
            print(f"Ошибка при парсинге номера телефона: {e}")
    
    return None

from typing import Optional
import asyncpg

async def authenticate_user(db_pool: asyncpg.Pool, phone_number: str) -> Optional[dict]:
    """
    Аутентифицирует пользователя по номеру телефона.
    Возвращает данные пользователя из 1С, если он найден.
    """
    if not phone_number:
        return None
    
    # SQL-запрос для поиска пациента в базе данных
    query = """
    SELECT id, full_name, email, date_of_birth
    FROM patients
    WHERE phone_number = $1
    """
    try:
        async with db_pool.acquire() as connection:
            user = await connection.fetchrow(query, phone_number)
            if user:
                return dict(user)  # Преобразуем Record в словарь
    except Exception as e:
        print(f"Ошибка при аутентификации пользователя: {e}")
    
    return None