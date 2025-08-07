# bot/services/db_service.py
import aiosqlite

class DatabaseService:
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def execute_query(self, query: str, params: tuple = None):
        async with aiosqlite.connect(self.db_path) as db:
            if params:
                await db.execute(query, params)
            else:
                await db.execute(query)
            await db.commit()

    async def fetch_one(self, query: str, params: tuple = None):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(query, params or ()) as cursor:
                return await cursor.fetchone()

    async def fetch_all(self, query: str, params: tuple = None):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(query, params or ()) as cursor:
                return await cursor.fetchall()