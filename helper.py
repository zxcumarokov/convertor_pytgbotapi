import requests
from bs4 import BeautifulSoup
from sqlalchemy import select
from sqlalchemy.orm import Session
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

# My Stuff
from db.db_engine import engine
from models import Language
from models import Phrase
from models import User


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


def get_directions_keyboardru(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    with Session(engine) as session:
        user = session.query(User).filter(User.id == user_id).one_or_none()
        # direction = session.scalars(select(Direction)).all()

        if user.language_id == 1:
            txmessage = session.query(Phrase).filter(
                (Phrase.phrase_code == "RUB_TO_USD") |
                (Phrase.phrase_code == "USD_TO_RUB"),
                Phrase.language_id == user.language_id
            ).all()
            for direction in txmessage:
                keyboard.add(
                    InlineKeyboardButton(
                        text=direction.text,
                        callback_data=f"set_direction#{direction.id}",
                    )
                )
        return keyboard


def get_directions_keyboarden(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    with Session(engine) as session:
        user = session.query(User).filter(User.id == user_id).one_or_none()
        # direction = session.scalars(select(Direction)).all()

        if user:
            txmessage = session.query(Phrase).filter(
                (Phrase.phrase_code == "RUB_TO_USD") |
                (Phrase.phrase_code == "USD_TO_RUB"),
                Phrase.language_id == user.language_id
            ).all()
            for direction in txmessage:
                keyboard.add(
                    InlineKeyboardButton(
                        text=direction.text,
                        callback_data=f"set_direction#{direction.id}",
                    )
                )
        return keyboard


def convert():
    pass


# @bot.callback_query_handler(func=lambda call: True)
# def callback_inline(call: types.CallbackQuery):
#     user_id = call.from_user.id
#     language_id = int(call.data.split("#")[1])
#     with Session(engine) as session:
#         messages = session.scalars(select(Phrase).where(Phrase.phrase_code == "CHOOSE_DIRECTION")).all()
#         if call.data == "set_direction#1":
#             bot.send_message(user_id, messages[0], reply_markup=get_directions_keyboard(language_id))
#         else:
#             bot.send_message(user_id, messages[1], reply_markup=get_directions_keyboard(language_id))


def clear_direction(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
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
        if not phrase:
            raise ValueError(f"Phrase {key} not found in database")
        return phrase
