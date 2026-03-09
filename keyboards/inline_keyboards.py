from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def payment_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Оплата 1 ⭐️", pay=True)],
        ]
    )
