import aiosqlite
from config import DATABASE_PATH

async def init_database():

    async with aiosqlite.connect(DATABASE_PATH) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS api_logs(

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            endpoint TEXT,
            ip TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

        await db.commit()