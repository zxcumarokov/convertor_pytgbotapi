import requests
from bs4 import BeautifulSoup
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.db_engine import engine
from models import Language, Direction


def update_exchange_rate() -> float | None:
    url = "https://www.google.com/finance/quote/USD-RUB?sa=X&ved=2ahUKEwjoxe30pcCBAxW3AhAIHfMmAxYQmY0JegQIDRAr"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36"
        # noqa E501
    }
    full_page = requests.get(url, headers=headers)
    soup = BeautifulSoup(full_page.content, "html.parser")
    convert = soup.findAll("div", {"class": "YMlKec fxKbKc"})

    if convert:
        return float(convert[0].text.replace(",", "."))
    else:
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

def get_directions_keyboard(language_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    with Session(engine) as session:   #КАЛЛБЭК ДАТА
        directions = session.scalars(select(Direction).where(Direction.phrase_code == "ru_en_direction")).all()
        for direction in directions:
            keyboard.add(
                InlineKeyboardButton(
                    text=direction.name,
                    callback_data=f"set_direction#{direction.id}",
                )
            )
    return keyboard

def callbackdatahendler():
