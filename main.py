import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import scrape
import os

TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)
LIBRARY = {"Li Ka Shing Library": "lks",
           "Kwa Geok Choo Law Library": "kgc"}


# ========Functions=======
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_id = message.chat.id

    answer = bot.send_message(
        chat_id, "<p>Hi, welcome to SMU Library bot!</p><br/><p>Simply click which library you would like to check the occupancy of!</p>", reply_markup="HTML")
    ask(message)

def ask(message):
    chat_id = message.chat.id

    markup = ReplyKeyboardMarkup()
    itembtn1 = KeyboardButton("Li Ka Shing Library")
    itembtn2 = KeyboardButton("Kwa Geok Choo Law Library")
    markup.row(itembtn1)
    markup.row(itembtn2)
    markup.one_time_keyboard = True

    answer = bot.send_message(
        chat_id, "Which library would you want to check?", reply_markup=markup)
    bot.register_next_step_handler(answer, show_occupancy)


def show_occupancy(message):
    chat_id = message.chat.id
    if message.text in LIBRARY:
        key = LIBRARY[message.text]
        OCCUPANCY = scrape.get_occupancy()
        bot.send_message(
            chat_id, f"The current occupancy in <code>{message.text}</code> is <code><strong>{OCCUPANCY[key]}</strong></code>.", parse_mode="HTML")
    else:
        bot.register_next_step_handler(message, command_default)

    ask(message)

# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(message):
    chat_id = message.chat.id
    # this is the standard reply to a normal message
    bot.send_message(
        chat_id, f"I don't understand \n <code>{message.text}</code> \nMaybe try the help page at /help", parse_mode="HTML")
    ask(message)

bot.polling()