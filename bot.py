import os
import time
import schedule
import telebot

BOT_TOKEN = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(BOT_TOKEN)



def start_command():
    bot.send_message(838386449, 'тут будет чота гавгать')



schedule.every(30).seconds.do(start_command) #Здесь запускаем бота в нужный момент



while True:
    schedule.run_pending()
    time.sleep(1)