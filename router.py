# Third Party Stuff
from sqlalchemy import select
from sqlalchemy.orm import Session

# My Stuff
from bot_instance import bot
from db_engine import engine
from models import User


def router(user_id: int):
    """ """
    with Session(engine) as session:
        user = session.scalars(select(User).where(User.id == user_id)).one_or_none()

        if not user:
            bot.send_message(user_id, "Вы не зарегистрированы, введите /start")
