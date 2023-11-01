import requests
from bs4 import BeautifulSoup
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.db_engine import engine
from models import Language, Direction
from models import Phrase
from bot_instance import bot
from telebot import types
import router
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

def get_directions_keyboard(language_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    with Session(engine) as session:   #КАЛЛБЭК ДАТА
        directions = session.scalars(select(Direction)).all()
        for direction in directions:
            keyboard.add(
                InlineKeyboardButton(
                    text=direction.name,
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

