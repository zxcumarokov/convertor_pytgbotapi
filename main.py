# Third Party Stuff
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session
from telebot import types

# My Stuff
from bot_instance import bot
from db.db_engine import engine
from helper import (clear_direction, update_exchange_rate, get_phrase, )
from models import Phrase
from models import User

from router import router


from typing import Tuple


# inline_keyboard = types.InlineKeyboardMarkup()

# Создание кнопок
# button1 = types.InlineKeyboardButton("Кнопка 1", callback_data="button1")
# button2 = types.InlineKeyboardButton("Кнопка 2", callback_data="button2")

# Добавление кнопок в клавиатуру
# inline_keyboard.add(button1, button2)

# Отправка сообщения с inline клавиатурой

# Словарь для сопоставления callback данных с действиями
direction_actions = {
    "set_direction#1": {"phrase_code": "ENTER_AMOUNT", "text_index": 0},
    "set_direction#2": {"phrase_code": "ENTER_AMOUNT", "text_index": 1},
    # Добавьте другие действия здесь
}


@bot.message_handler(commands=["start", "help"])
def start(message: types.Message):
    """
    Команда /start
    проверяет наличие пользователя в базе данных
    если пользователя нет, то добавляет его в базу данных
    в конце отправляет в роутер
    """
    user_id = message.from_user.id
    with Session(engine) as session:
        user = session.scalars(select(User).where(User.id == user_id)).one_or_none()

        if not user:
            user = User(id=user_id, name=message.from_user.full_name, )
            session.add(user)
            session.commit()
        clear_direction(user.id)
    router(user_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("set_language"))
def callback_inline(call: types.CallbackQuery):
    """
    Обработчик inline кнопок
    """
    user_id = call.from_user.id
    with Session(engine) as session:
        user = session.scalars(select(User).where(User.id == user_id)).one_or_none()
        if not user:
            bot.send_message(user_id, "Вы не зарегистрированы, введите /start")
            return

        if call.data.startswith("set_language#1"):
            language_id = int(call.data.split("#")[1])
            user.language_id = language_id
            session.commit()
        elif call.data.startswith("set_language#2"):
            language_id = int(call.data.split("#")[1])
            user.language_id = language_id
            session.commit()
        router(user_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("set_direction"))
def callback_dir(call: types.CallbackQuery):
    user_id = call.from_user.id

    with Session(engine) as session:
        user = session.scalars(select(User).where(User.id == user_id)).one_or_none()

        if not user:
            bot.send_message(user_id, "Вы не зарегистрированы, введите /start")
            return

        direction_data = direction_actions.get(call.data)

        if direction_data:
            direction_id = int(call.data.split("#")[1])
            user.direction_id = direction_id
            session.commit()

            phrase_code = direction_data["phrase_code"]
            text_index = direction_data["text_index"]
            message = session.scalars(select(Phrase).where(Phrase.phrase_code == phrase_code)).all()
            if message and len(message) > text_index:
                bot.send_message(user_id, message[text_index].text)
            else:
                bot.send_message(user_id, "Нет подходящего сообщения")

        router(user_id)

        # elif call.data.startswith("set_direction"):  #     direction_id = int(call.data.split("#")[1])  #     user.direction_id = direction_id  #     session.commit()  #     bot.send_message(user_id, "Направление успешно выбрано")  #     router(user_id)  # elif call.data.startswith("convert"):  #     bot.send_message(user_id, "Введите сумму для конвертации")  #     bot.register_next_step_handler(call.message, convert)


def amoun_inputed(message: types.Message):
    text = message.text.replace(',', '.')  # Заменяем запятую на точку, если она есть
    amount = Decimal(text)
    rate = update_exchange_rate()
    user_id = message.from_user.id
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user_id:
            raise ValueError("User not found")
        direction_id = user_id
    match direction_id:
        # usd-rub
        case 1:
            result = amount * rate
            currency: str = get_phrase('result_rub', user.language_id)
        case 2:
            result = amount / rate
            currency: str = get_phrase('result_usd', user.language_id)
        case _:
            raise ValueError(f"Direction {direction_id} not found")

    final_phrase: str = get_phrase('final_phrase', user.language_id)
    bot.send_message(text=f"{final_phrase}\n{result} {currency}", chat_id=user.id, )


bot.infinity_polling()