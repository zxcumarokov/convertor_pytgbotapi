# Third Party Stuff
from loguru import logger
from sqlalchemy import select

# from sqlalchemy.orm import Session
from sqlalchemy.orm import Session

# My Stuff
from converter.actions import (
    choose_direction,
    choose_language,
    get_amount,
)

# from telebot import types
# from main import bot
from converter.bot_instance import bot
from db.db_engine import engine
from db.models import User

# Configure logging to output to console and file
logger.add("logs/app.log", rotation="500 MB", level="INFO", backtrace=True, diagnose=True)

# from telebot import types


def router(user_id: int):
    """ """
    with Session(engine) as session:
        user = session.scalars(select(User).where(User.id == user_id)).one_or_none()

        if not user:
            logger.warning(f"User with ID {user_id} is not registered. Sending registration message.")
            bot.send_message(user_id, "Вы не зарегистрированы, введите /start")
            return

        if not user.language_id:
            logger.info(f"User with ID {user_id} has not chosen a language. Redirecting to language selection.")
            choose_language(user.id)
            return

        if not user.direction_id:
            logger.info(f"User with ID {user_id} has not chosen a direction. Redirecting to direction selection.")
            choose_direction(user.id, user.language_id)
            return

        logger.info(f"User with ID {user_id} is ready to convert. Redirecting to amount selection.")
        get_amount(user_id, user.language_id)
        return
