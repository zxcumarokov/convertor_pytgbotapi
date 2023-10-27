# Third Party Stuff
from sqlalchemy import select
from sqlalchemy.orm import Session
from telebot import types

# My Stuff
from bot_instance import bot
from db_engine import engine
from helper import update_exchange_rate
from models import User
from router import router

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


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)
    bot.send_message(message.chat.id, message.text)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "button1":
        bot.send_message(call.message.chat.id, "Вы нажали на кнопку 1")
    elif call.data == "button2":
        bot.send_message(call.message.chat.id, "Вы нажали на кнопку 2")
    else:
        bot.send_message(call.message.chat.id, "Ошибка")


bot.infinity_polling()
