from aiogram import Bot, F, Router, types
from aiogram.filters import Command, CommandObject
from aiogram.types import LabeledPrice, PreCheckoutQuery

from keyboards.inline_keyboards import payment_keyboard

# инициализация роутера
router = Router()


# запрос инвойса на донат
@router.message(Command("donate"))
async def donate_handler(message: types.Message) -> None:
    currency = "XTR"
    prices = [LabeledPrice(label=currency, amount=1)]
    await message.answer_invoice(
        title="Поддержка донатом",
        description="Поддержать одной звездой!",
        prices=prices,
        provider_token="",
        payload="channel_support",
        currency=currency,
        reply_markup=payment_keyboard(),
    )


# отправка инвойса
@router.pre_checkout_query()
async def pre_checkout_query_handler(pre_checkout_query: PreCheckoutQuery) -> None:
    await pre_checkout_query.answer(ok=True)


# подтверждение оплаты
@router.message(F.successful_payment)
async def successful_payment_handler(message: types.Message) -> None:
    await message.answer(
        f"/refund {message.successful_payment.telegram_payment_charge_id}",
        message_effect_id="5046509860389126442",
    )


# возврат средств
@router.message(Command("refund"))
async def refund(
    message: types.Message,
    bot: Bot,
    command: CommandObject,
) -> None:
    transaction_id = command.args
    if not transaction_id:
        await message.answer("Укажи id транзакции: /refund <telegram_payment_charge_id>")
        return

    try:
        await bot.refund_star_payment(
            user_id=message.from_user.id,
            telegram_payment_charge_id=transaction_id,
        )
        await message.answer("Возврат выполнен.")
    except Exception:
        await message.answer("Не удалось выполнить возврат.")
