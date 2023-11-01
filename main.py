# Third Party Stuff
from sqlalchemy import select
from sqlalchemy.orm import Session
from telebot import types

# My Stuff
from bot_instance import bot
from db.db_engine import engine
from models import User
from router import router

from models import Phrase
from models import Language
from models import Direction




# inline_keyboard = types.InlineKeyboardMarkup()

# Создание кнопок
# button1 = types.InlineKeyboardButton("Кнопка 1", callback_data="button1")
# button2 = types.InlineKeyboardButton("Кнопка 2", callback_data="button2")

# Добавление кнопок в клавиатуру
# inline_keyboard.add(button1, button2)

# Отправка сообщения с inline клавиатурой


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
            user = User(
                id=user_id,
                name=message.from_user.full_name,
            )
            session.add(user)
            session.commit()
    router(user_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("set_language"))
def callback_inline(call: types.CallbackQuery):
    """
    Обработчик inline кнопок
    """
    user_id = call.from_user.id
    with Session(engine) as session:
        user = session.scalars(select(User).where(User.id == user_id)).one_or_none()
        messages = session.scalars(select(Phrase).where(Phrase.phrase_code == "SELECT_LANGUAGE")).all()
        if not user:
            bot.send_message(user_id, "Вы не зарегистрированы, введите /start")
            return

        if call.data.startswith("set_language#1"):
            language_id = int(call.data.split("#")[1])
            user.language_id = language_id
            session.commit()
            bot.send_message(user_id, messages[0].text)
            router(user_id)
        elif call.data.startswith("set_language#2"):
            language_id = int(call.data.split("#")[1])
            user.language_id = language_id
            session.commit()
            bot.send_message(user_id, messages[1].text)
            router(user_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("set_direction"))
def callback_dir(call: types.CallbackQuery):
    user_id = call.from_user.id
    with Session(engine) as session:
        user = session.scalars(select(User).where(User.id == user_id)).one_or_none()
        messages = session.scalars(select(Phrase).where(Phrase.phrase_code == "SELECT_LANGUAGE")).all()
        if not user:
            bot.send_message(user_id, "Вы не зарегистрированы, введите /start")
            return

        if call.data.startswith("set_direction#1"):
            direction_id = int(call.data.split("#")[1])
            user.direction_id = direction_id
            session.commit()
            bot.send_message(user_id, messages[0].text)
            router(user_id)
        elif call.data.startswith("set_direction#2"):
            direction_id = int(call.data.split("#")[1])
            user.direction_id = direction_id
            session.commit()
            bot.send_message(user_id, messages[1].text)
            router(user_id)


        # elif call.data.startswith("set_direction"):
        #     direction_id = int(call.data.split("#")[1])
        #     user.direction_id = direction_id
        #     session.commit()
        #     bot.send_message(user_id, "Направление успешно выбрано")
        #     router(user_id)
        # elif call.data.startswith("convert"):
        #     bot.send_message(user_id, "Введите сумму для конвертации")
        #     bot.register_next_step_handler(call.message, convert)


bot.infinity_polling()
