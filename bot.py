import asyncio
from os import getenv

from aiogram import Bot, Dispatcher, F, html, types
from aiogram.filters import Command
from aiogram.types import LabeledPrice, PreCheckoutQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from psycopg.rows import dict_row

from db import get_pool

POSTGRES_DSN = getenv("POSTGRES_DSN")
BOT_TOKEN = getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.startup()
async def on_startup(bot: Bot):
    pool = await get_pool(conninfo=POSTGRES_DSN)
    await pool.open()
    print("Pool opened")


@dp.shutdown()
async def on_shutdown(bot: Bot):
    pool = await get_pool(conninfo=POSTGRES_DSN)
    await pool.close()
    print("Pool closed")


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"Привет, {html.bold(message.from_user.full_name)}!\n\n/donate для поддержки. /refund + id для возврата звезд.",
        parse_mode="html",
        # message_effect_id="5046509860389126442",
    )

    pool = await get_pool(conninfo=POSTGRES_DSN)
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cursor:
            await cursor.execute("SELECT 'Hello from PostgreSQL' as message;")
            response = await cursor.fetchall()
            if len(response):
                result = response[0]
                await message.answer(result["message"])


def payment_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Оплата 1 ⭐️", pay=True)
    return builder.as_markup()


@dp.message(Command("donate"))
async def donate_handler(message):
    CURRENCY = "XTR"
    prices = [LabeledPrice(label=CURRENCY, amount=1)]
    await message.answer_invoice(
        title="Поддержка донатом",
        description="Поддержать одной звездой!",
        prices=prices,
        provider_token="",
        payload="channel_support",
        currency=CURRENCY,
        reply_markup=payment_keyboard(),
    )


@dp.pre_checkout_query()
async def pre_checkout_query_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@dp.message(F.successful_payment)
async def successful_payment_handler(message):
    await message.answer(
        f"/refund {message.successful_payment.telegram_payment_charge_id}",
        message_effect_id="5046509860389126442",
    )


@dp.message(Command("refund"))
async def refund(message, bot, command):
    transaction_id = command.args
    try:
        await bot.refund_star_payment(
            user_id=message.from_user.id,
            telegram_payment_charge_id=transaction_id,
        )
    except Exception as exc:
        print(exc)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
