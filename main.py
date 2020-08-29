import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove
import scrape
import os
from flask import Flask, request


server = Flask(__name__)
TOKEN = "1245288199:AAHrFIrxoJPsqeHzUmOtZ1cDvJ3lwR3zb9g"
bot = telebot.TeleBot(TOKEN)
LIBRARY = {"Li Ka Shing Library": "lks",
           "Kwa Geok Choo Law Library": "kgc"}
OCCUPANCY = scrape.get_occupancy()


# ========Functions=======
@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    chat_id = message.chat.id

    markup = ReplyKeyboardMarkup()
    itembtn1 = KeyboardButton("Li Ka Shing Library")
    itembtn2 = KeyboardButton("Kwa Geok Choo Law Library")
    markup.row(itembtn1)
    markup.row(itembtn2)
    markup.one_time_keyboard = True

    answer = bot.send_message(chat_id, "Hi, welcome to SMU Library bot! \nWhich library would you want to check?", reply_markup=markup)
    bot.register_next_step_handler(answer, show_occupancy)

def show_occupancy(message):
    chat_id = message.chat.id
    if message.text in LIBRARY:
        key = LIBRARY[message.text]
        bot.send_message(chat_id, f"The current occupancy in <code>{message.text}</code> is <code><strong>{OCCUPANCY[key]}</strong></code>." , parse_mode="HTML")
    else:
        bot.register_next_step_handler(message, command_default)

# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(message):
    chat_id = message.chat.id
    # this is the standard reply to a normal message
    bot.send_message(chat_id, f"I don't understand \n <code>{message.text}</code> \nMaybe try the help page at /help", parse_mode="HTML")


# ========Server=======
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://shrouded-ravine-38898.herokuapp.com/' + TOKEN)
    return "!", 200

bot.polling()
# server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

# if __name__ == "__main__":