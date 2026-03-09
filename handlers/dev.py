from aiogram import Router, types
from aiogram.filters import Command
from psycopg.rows import dict_row

from config import POSTGRES_DSN
from db.db_conn import get_pool

# инициализация роутера
router = Router()


# ручной тест доступности бд
@router.message(Command("pg"))
async def cmd_pg(message: types.Message) -> None:
    pool = await get_pool(conninfo=POSTGRES_DSN)
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cursor:
            await cursor.execute("SELECT 'Hello from PostgreSQL' as message;")
            response = await cursor.fetchall()
            if response:
                await message.answer(response[0]["message"])

