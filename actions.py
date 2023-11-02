from bot_instance import bot
from helper import (get_languages_keyboard, get_phrase, )


def choose_language(user_id: int):
    bot.send_message(user_id, text="choose language:", reply_markup=get_languages_keyboard(), )


def get_amount(user_id: int):
    message = bot.send_message(text=get_phrase('ENTER_AMOUNT'), chat_id=user_id, )
    from main import amoun_inputed
    bot.register_next_step_handler(mesage=message, callback=amoun_inputed, )
