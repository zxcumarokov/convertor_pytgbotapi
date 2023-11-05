# Third Party Stuff
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session
from telebot import types

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardRemove


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


@bot.message_handler(commands=["start", "info"])
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

        router(user_id)
     # Remove the keyboard
    bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id, reply_markup=None)

    # Delete the message
    bot.delete_message(chat_id=user_id, message_id=call.message.message_id)


bot.infinity_polling()