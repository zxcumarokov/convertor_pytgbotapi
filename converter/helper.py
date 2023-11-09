# Standard Library
import logging
from decimal import Decimal

# Third Party Stuff
import requests
from bs4 import BeautifulSoup
from sqlalchemy import select
from sqlalchemy.orm import Session
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# My Stuff
from db.db_engine import engine
from db.models import (
    Direction,
    Language,
    Phrase,
    User,
)


def update_exchange_rate() -> Decimal | None:
    try:
        url = "https://www.google.com/finance/quote/USD-RUB?sa=X&ved=2ahUKEwjoxe30pcCBAxW3AhAIHfMmAxYQmY0JegQIDRAr"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/117.0.0.0 Safari/537.36"
        }
        full_page = requests.get(url, headers=headers)
        soup = BeautifulSoup(full_page.content, "html.parser")
        convert = soup.findAll("div", {"class": "YMlKec fxKbKc"})

        if convert:
            exchange_rate = Decimal(convert[0].text.replace(",", "."))
            logger.info(f"Exchange rate updated: {exchange_rate}")
            return exchange_rate
        else:
            logger.warning("Failed to retrieve exchange rate.")
            return None
    except Exception as e:
        logger.error(f"Error updating exchange rate: {e}")
        return None


def get_languages_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    with Session(engine) as session:
        languages = session.scalars(select(Language)).all()
        for language in languages:
            keyboard.add(
                InlineKeyboardButton(
                    text=language.name,
                    callback_data=f"set_language#{language.id}",
                )
            )
    return keyboard


def get_directions_keyboard(language_id: int):
    keyboard = InlineKeyboardMarkup()

    with Session(engine) as session:
        directions = session.scalars(select(Direction)).all()

        for direction in directions:
            button_text = get_phrase(direction.phrase_code, language_id)

            if button_text:
                callback_data = f"set_direction#{direction.id}"
                keyboard.add(
                    InlineKeyboardButton(text=button_text, callback_data=callback_data)
                )

    return keyboard


def clear_direction(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            logger.warning(f"User {user_id} not found in database")
            return
        user.direction_id = None
        session.commit()


def get_phrase(key: str, language_id: int) -> str:
    with Session(engine) as session:
        phrase = session.scalar(
            select(Phrase.text)
            .where(Phrase.phrase_code == key)
            .where(Phrase.language_id == language_id)
        )
        if phrase:
            return phrase
        else:
            new_phrase = Phrase(
                key=key,
                language_id=1,
                value=key.replace("_", " ").capitalize(),
            )
            session.add(new_phrase)
            session.commit()
            return new_phrase


def get_user_currency(user_id: int) -> int:
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found in database")
        return user.direction_id
