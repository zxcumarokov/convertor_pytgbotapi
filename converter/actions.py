# Standard Library
import logging
from decimal import (
    ROUND_DOWN,
    Decimal,
    InvalidOperation,
)

# Third Party Stuff
from sqlalchemy.orm import Session
from telebot import types

# My Stuff
from converter.bot_instance import bot
from converter.helper import (
    get_directions_keyboard,
    get_languages_keyboard,
    get_phrase,
    get_user_currency,
    update_exchange_rate,
)
from core.constants import DirectionsEnum
from db.db_engine import engine
from db.models import User


def choose_language(user_id: int):
    bot.send_message(
        user_id,
        text="choose language:",
        reply_markup=get_languages_keyboard(),
    )


def get_amount(user_id: int, language_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            logging.warning(f"User {user_id} not found in database")
            return
        match user.direction_id:
            case DirectionsEnum.USD_RUB:
                currency = get_phrase("USD", language_id)
            case DirectionsEnum.RUB_USD:
                currency = get_phrase("RUB", language_id)
            case _:
                raise ValueError(f"Direction {user.direction_id} not found")

    message_text = f"{get_phrase('ENTER_AMOUNT', language_id)} ({get_phrase(currency, language_id)})"
    message = bot.send_message(
        text=message_text,
        chat_id=user_id,
    )
    bot.register_next_step_handler(
        message=message,
        callback=amoun_inputed,
    )


def choose_direction(user_id: int, language_id: int):
    bot.send_message(
        user_id,
        text=get_phrase("CHOOSE_DIRECTION", language_id),
        reply_markup=get_directions_keyboard(language_id),
    )


def amoun_inputed(message: types.Message):
    if not message.text:
        bot.send_message(message.chat.id, "Please, enter a number")
        logging.warning("User didn't enter a number")
        return

    text = message.text.replace(",", ".")  # Заменяем запятую на точку, если она есть
    user_id = message.from_user.id
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise ValueError("User not found")
        language_id = user.language_id
        try:
            amount = Decimal(text)
        except InvalidOperation:
            error_text = get_phrase("INVALID_NUMBER", language_id)
            bot.send_message(message.chat.id, error_text)
            get_amount(message.chat.id, language_id)
            return

    rate = update_exchange_rate()  # Преобразуем rate в Decimal
    if not rate:
        error_text = get_phrase("RATE_NOT_FOUND", language_id)
        bot.send_message(message.chat.id, error_text)
        return

    direction_id = user.direction_id  # Используем direction_id из записи пользователя
    match direction_id:
        # usd-rub
        case 1:
            result = (amount * rate).quantize(Decimal("0.00"), rounding=ROUND_DOWN)
            currency: str = get_phrase("RESULT_RUB", language_id)
        case 2:
            result = (amount / rate).quantize(Decimal("0.00"), rounding=ROUND_DOWN)
            currency: str = get_phrase("RESULT_USD", language_id)
        case _:
            raise ValueError(f"Direction {direction_id} not found")

    final_phrase: str = get_phrase("FINAL_PHRASE", language_id)
    bot.send_message(
        text=f"{final_phrase}\n{result} {currency}",
        chat_id=user.id,
    )
    choose_direction(user_id, language_id)
