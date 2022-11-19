import os
import telebot
import logging
from config import *
from flask import Flask,request
bot=telebot.Telebot(BOT_TOKEN)
server=Flask(__name__)
logger=telebot.logger
logger.setLevel(logging.DEBUG)


@bot.message_handler(command=["/start"])
def start(message):
    username=message.from_user.username
    bot.reply_to(message,f"Hello,{username}!")


@server.route(f"/{BOT_TOKEN}",methods=["POST"])
def redirect_message():
    json_string=request.get_data().decode("utf=8")
    update=telebot.typed.Update.de_json(json_string)
    bor.process_new_updates({update})
    return"!",200


if __name__=="__name__":
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    server.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)))
