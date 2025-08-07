# bot/core.py
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

class BotCore:
    def __init__(self, token: str):
        self.bot = Bot(token=token)
        self.storage = MemoryStorage()
        self.dp = Dispatcher(storage=self.storage)

    def register_routers(self, *routers):
        for router in routers:
            self.dp.include_router(router)

    async def start_polling(self):
        await self.dp.start_polling(self.bot)