import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN, POSTGRES_DSN
from db.db_conn import get_pool
from handlers.dev import router as dev_router
from handlers.payments import router as payments_router
from handlers.start import router as start_router

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# регистрация роутов
dp.include_router(start_router)
dp.include_router(dev_router)
dp.include_router(payments_router)


@dp.startup()
async def on_startup(_bot: Bot) -> None:
    pool = await get_pool(conninfo=POSTGRES_DSN)
    await pool.open()
    print("Pool opened")


@dp.shutdown()
async def on_shutdown(_bot: Bot) -> None:
    pool = await get_pool(conninfo=POSTGRES_DSN)
    await pool.close()
    print("Pool closed")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
