from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    ConversationHandler
)

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InputMediaPhoto,
    InputMediaVideo
)

from datetime import (
    timedelta,
    datetime,
    date
)

from pytz import timezone
import copy
import time
import logging
import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']
BOT_TOKEN = os.environ['BOT_TOKEN']
APP_URL = os.environ['APP_URL'] + BOT_TOKEN
DB_URI = os.environ['DB_URI']
db_connection = psycopg2.connect(DB_URI, sslmode="require")
db_object = db_connection.cursor()\

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start (bot,update):
    update.message.reply_text("Привет")

def echo(bot,update):
    update.message.reply_text('Aanswer')

updater = Updater(BOT_TOKEN)

dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))

text_handler = MessageHandler(Filters.text, echo)

dp.add_handler(text_handler)



updater.start_polling()

updater.idle()

#if __name__ == '__main__':
    #main()

