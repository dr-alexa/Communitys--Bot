import aiogram
import asyncio
import logging
import time
from aiogram import Bot, Dispatcher, types
from config import TOKEN
from app.handlers import router


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()



async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
    asyncio.run(main())
