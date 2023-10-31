# Third Party Stuff
from sqlalchemy import select
from sqlalchemy.orm import Session

# My Stuff
from bot_instance import bot
from db.db_engine import engine
from helper import get_directions_keyboard
from helper import get_languages_keyboard
from models import Phrase
from models import User
from helper import callback_data




def router(user_id: int, language_id: int = None):
    """ """
    with Session(engine) as session:
        user = session.scalars(select(User).where(User.id == user_id)).one_or_none()
        messages = session.scalars(select(Phrase).where(Phrase.phrase_code == "CHOOSE_DIRECTION")).all()
        if not user:
            bot.send_message(user_id, "Вы не зарегистрированы, введите /start")


        if not user.language_id:

                bot.send_message(
                    user_id,
                    text="choose language:",
                    reply_markup=get_languages_keyboard(),
                )

    if not user.direction_id:
        if callback_data == "language#1":
            bot.send_message(
                user_id,
                text="выберете направление",
                reply_markup=get_directions_keyboard(language_id),
            )
        else:
            bot.send_message(
                user_id,
                text="выберете направление",
                reply_markup=get_directions_keyboard(language_id),
            )
