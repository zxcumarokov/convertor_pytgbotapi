import telebot
from helper import update_exchange_rate
from telebot import types
# from models import Language, Phrase
#
# from db_engine import engine
# from models import Base, Language, Phrase, User, Direction
from config import TOKEN, db_url


bot = telebot.TeleBot(TOKEN, parse_mode=None)

remove_keyboard = types.ReplyKeyboardRemove(selective=False)

markup = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('a')
itembtn2 = types.KeyboardButton('v')
itembtn3 = types.KeyboardButton('d')
markup.add(itembtn1, itembtn2, itembtn3)





from telebot import types

# Создание объекта InlineKeyboardMarkup
inline_keyboard = types.InlineKeyboardMarkup()

# Создание кнопок
button1 = types.InlineKeyboardButton("Кнопка 1", callback_data="button1")
button2 = types.InlineKeyboardButton("Кнопка 2", callback_data="button2")

# Добавление кнопок в клавиатуру
inline_keyboard.add(button1, button2)

# Отправка сообщения с inline клавиатурой


@bot.message_handler(commands=['start', 'help'])
def start(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    # Проверяем наличие пользователя в базе данных
    with Session(engine) as session:
        user = session.scalars(
            select(User)
            .where(User.id == user_id)
        ).one_or_none()

        if not user:
            create_user(user_id, full_name)
    await router(user_id)




@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, message.text)
	bot.send_message(message.chat.id, message.text)

	
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	if call.data == "button1":
		bot.send_message(call.message.chat.id, "Вы нажали на кнопку 1")
	elif call.data == "button2":
		bot.send_message(call.message.chat.id, "Вы нажали на кнопку 2")
	else:
		bot.send_message(call.message.chat.id, "Ошибка")

bot.infinity_polling()