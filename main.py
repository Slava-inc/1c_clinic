from aiogram import Bot
import asyncio
from bot.core import BotCore
from bot.services.db_service import DatabaseService
from bot.handlers.auth import auth_router
from bot.handlers.appointments import appointments_router
from bot.handlers.analyses import analyses_router
from bot.handlers.notifications import notifications_router
from bot.handlers.main_menu import main_menu_router
from tokens import TOKEN

# Инициализация базы данных
async def init_database():
    """
    Инициализация базы данных: выполнение SQL-скрипта из файла init_db.sql.
    """
    db = DatabaseService("clinic.db")
    with open("migrations/init_db.sql", "r") as f:
        sql_script = f.read()
    await db.executescript(sql_script)
    print("Database initialized successfully.")

# Удаление Webhook
async def clear_webhook(bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)
    print("Webhook удален, очередь обновлений очищена.")

# Запуск бота
async def start_bot():
    bot_core = BotCore(TOKEN)

    # Удаление Webhook
    await clear_webhook(bot_core.bot)

    # Регистрация роутеров
    bot_core.register_routers(
        auth_router,
        appointments_router,
        main_menu_router,
        analyses_router,
        notifications_router
    )

    # Запуск бота в режиме long polling
    print("Запуск бота в режиме long polling...")
    await bot_core.start_polling()

# Точка входа
async def main():

     # Инициализация базы данных
    await init_database() 
    # Запуск бота
    await start_bot()

if __name__ == "__main__":
    asyncio.run(main())