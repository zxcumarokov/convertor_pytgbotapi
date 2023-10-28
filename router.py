# Third Party Stuff
from sqlalchemy import select
from sqlalchemy.orm import Session

# My Stuff
from bot_instance import bot
from db_engine import engine
from models import User

from helper import get_languages_keyboard


def router(user_id: int, language_id: int = None):
    """ """
    with Session(engine) as session:
        user = session.scalars(select(User).where(User.id == user_id)).one_or_none()

        if not user:
            bot.send_message(user_id, "Вы не зарегистрированы, введите /start")

    if not user.language_id:
        # Пользователь не выбрал язык
        bot.send_message(
            chat_id=user_id,
            text="Выберите язык:",
            reply_markup=get_languages_keyboard()
        )
        return
