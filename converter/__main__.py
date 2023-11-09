# Standard Library
import logging

# Third Party Stuff
from sqlalchemy import select
from sqlalchemy.orm import Session
from telebot import types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# My Stuff
from converter.bot_instance import bot
from converter.helper import clear_direction
from converter.router import router
from db.db_engine import engine
from db.models import User

direction_actions = {
    "set_direction#1": {"phrase_code": "ENTER_AMOUNT", "text_index": 0},
    "set_direction#2": {"phrase_code": "ENTER_AMOUNT", "text_index": 1},
    # Добавьте другие действия здесь
}


@bot.message_handler(commands=["start", "info"])
def start(message: types.Message):
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
        clear_direction(user.id)
    logger.info(f"User {user_id} started the conversation.")
    router(user_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("set_language"))
def callback_inline(call: types.CallbackQuery):
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
            logger.info(f"User {user_id} set language to {language_id}")
        elif call.data.startswith("set_language#2"):
            language_id = int(call.data.split("#")[1])
            user.language_id = language_id
            session.commit()
            logger.info(f"User {user_id} set language to {language_id}")
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
            logger.info(f"User {user_id} set direction to {direction_id}")

        router(user_id)
    bot.edit_message_reply_markup(
        chat_id=user_id, message_id=call.message.message_id, reply_markup=None
    )
    bot.delete_message(chat_id=user_id, message_id=call.message.message_id)


if __name__ == "__main__":
    logger.info("Bot started.")
    bot.infinity_polling()
