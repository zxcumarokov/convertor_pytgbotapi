from bot_instance import bot
from helper import (get_languages_keyboard, get_phrase, get_directions_keyboard, )


def choose_language(user_id: int):
    bot.send_message(user_id, text="choose language:", reply_markup=get_languages_keyboard(), )


def get_amount(user_id: int,language_id:int):
    message = bot.send_message(text=get_phrase('ENTER_AMOUNT', language_id), chat_id=user_id, )
    from main import amoun_inputed
    bot.register_next_step_handler(mesage=message, callback=amoun_inputed, )



def choose_direction(user_id: int, language_id: int):
    bot.send_message(user_id, text=get_phrase("CHOOSE_DIRECTION", language_id), reply_markup=get_directions_keyboard(language_id), )