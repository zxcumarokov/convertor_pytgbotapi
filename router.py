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
from helper import get_directions_keyboard

from telebot import types

def router(user_id: int, language_id: int = None, direction_id: int = None):
    """ """
    with Session(engine) as session:
        user = session.scalars(select(User).where(User.id == user_id)).one_or_none()
        msgdirection = session.scalars(select(Phrase).where(Phrase.phrase_code == "CHOOSE_DIRECTION")).all()


        if not user:
            bot.send_message(user_id, "Вы не зарегистрированы, введите /start")


        if not user.language_id:

                bot.send_message(
                    user_id,
                    text="choose language:",
                    reply_markup=get_languages_keyboard(),
                )
        if not user.direction_id:

            if user.language_id == 1:
                bot.send_message(
                    user_id,
                    text=msgdirection[0].text,
                    reply_markup=get_directions_keyboard(language_id = 1),
                )
            elif user.language_id == 2:
                bot.send_message(
                    user_id,
                    text=msgdirection[1].text,
                    reply_markup=get_directions_keyboard(language_id = 2),
                )



