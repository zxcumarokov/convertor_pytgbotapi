# Third Party Stuff
import telebot

# My Stuff
from core.config import TOKEN

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
