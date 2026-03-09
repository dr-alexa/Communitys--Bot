from aiogram import Router, html, types
from aiogram.filters import Command

# инициализация роутера
router = Router()

# todo: можно разделить на 2 команды, start и help
@router.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    await message.answer(
        f"Привет, {html.bold(message.from_user.full_name)}!\n\n"
        "/donate для поддержки. /refund + id для возврата звезд.",
        parse_mode="html",
    )
