TOKEN = <TOKEN>
import logging
from typing import Dict

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
import requests
import json


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING, CHECK_CAP = range(2)

LIBRARY = {"Li Ka Shing Library": "lks",
           "Kwa Geok Choo Law Library": "kgc"}

reply_keyboard = [
    ["Li Ka Shing Library"],
    ["Kwa Geok Choo Law Library"],
    ["End"]
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

def start(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(
        "Hi! This Telegram bot aims to help students check the capacity at the libraries with ease. Hope that you will find this useful! "
    )
    update.message.reply_text("Which library would you like to check?", reply_markup=markup)

    return CHECK_CAP

def library_choice(update: Update, _: CallbackContext) -> int:
    update.message.reply_text("Which library would you like to check?", reply_markup=markup)

    return CHECK_CAP

def get_occupancy(update: Update, context: CallbackContext) -> int:
    URL = "https://smulibraries.southeastasia.cloudapp.azure.com/public/count.json"
    page = requests.get(URL).text
    page = json.loads(page)

    results = {"lks": page["lks"]["inside"],
                "kgc": page["kgc"]["inside"] }

    if update.message.text in LIBRARY.keys():
        key = LIBRARY[update.message.text]
        OCCUPANCY = results[key]

        update.message.reply_html(f"The current occupancy in <code>{update.message.text}</code> is <code><strong>{OCCUPANCY}</strong></code>.")
        update.message.reply_text("Which library would you like to check?", reply_markup=markup)

        return CHECK_CAP
    else:
        return CHOOSING

def end(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        f"Thank you for using this bot! Use the /start command again if you would like to restart the bot. Have a great day ahead! :)",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(
                    Filters.text & ~Filters.command , library_choice
                )
            ],
            CHECK_CAP: [
                MessageHandler(
                    Filters.regex('^(Li Ka Shing Library|Kwa Geok Choo Law Library)$'), get_occupancy
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('^End$'), end)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()