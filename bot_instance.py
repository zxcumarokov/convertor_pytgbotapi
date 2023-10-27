# Third Party Stuff
import telebot

# My Stuff
from config import TOKEN

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
