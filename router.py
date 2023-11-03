# Third Party Stuff
from sqlalchemy import select
# from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
# from telebot import types
# from main import bot
# My Stuff
from bot_instance import bot
from db.db_engine import engine
from helper import get_languages_keyboard
from models import Phrase
from models import User

# from telebot import types

from helper import update_exchange_rate
from telebot import types
from actions import choose_language
from actions import get_amount
from actions import choose_direction


def router(user_id: int):
    """ """
    with Session(engine) as session:
        user = session.scalars(select(User).where(User.id == user_id)).one_or_none()

        if not user:
            bot.send_message(user_id, "Вы не зарегистрированы, введите /start")
            return

        if not user.language_id:
            choose_language(user.id)
            return

        if not user.direction_id:
            choose_direction(user.id,user.language_id)
            return

        get_amount(user_id)
        return
