import os
import telebot
import logging
import psycopg2
#from config import *
from boto.s3.connection import S3Connection
s3=S3Connection(os.environ['DATABASE_URL'], os.environ['BOT_TOKEN'], os.environ['APP_URL'])
print(s3)
from flask import Flask, request
from telebot import types


bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)
logger = telebot.logger
logger.setLevel(logging.DEBUG)

db_connection = psycopg2.connect(DB_URI,sslmode="require")
db_object = db_connection.cursor()

def update_messages_count(user_id): #Функция для счетчика сообщений от пользователя
    db_object.execute(f"UPDATE users SET messages=messages+1 WHERE user_id={user_id}")
    db_connection.commit()

@bot.message_handler(commands=["start"]) #обработка событий при вводе команды СТРАТ
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) # создаем клавиатуру
    item1 = types.KeyboardButton("О системе")    # Макет кнопки
    item2 = types.KeyboardButton("Видеолекции")
    item3 = types.KeyboardButton("Расписание")
    item4 = types.KeyboardButton("Об авторе")

    markup.add(item1, item2, item3, item4)

    user_id = message.from_user.id # Определяем ID пользовтеля
    username = message.from_user.first_name # Определяем имя пользовтеля
    bot.reply_to(message, f"Привет, {username}!Я бот-Макс. Я буду помогать тебе менять привычки . Готов? Жми меню.", reply_markup=markup) # Приветствуем пользователя

    db_object.execute(f"SELECT user_id FROM users WHERE user_id = {user_id}") # Проверяем есть ли пользователь в БД и если нет то добавляем
    result = db_object.fetchone()
    if not result:
        db_object.execute("INSERT INTO users(user_id,user_name,messages) VALUES(%s, %s, %s)", (user_id, username, 0))
        db_connection.commit()
    update_messages_count(user_id)



@bot.message_handler(func=lambda message: True, content_types=["text"]) # Отслеживаем все сообщения пользователя и  увеличиваем счетчик



def message_from_user(message):
    if message.text == "Об авторе":
        file = open('VAG.jpg', 'rb')
        bot.send_photo(message.from_user.id, file, caption= "Жданов Владимир Алексеевич, врач ЛФК. Тут нужно написать все , что хотите о себе рассказать и ссылки на каналы YouTube")
    elif message.text == "О системе":
        file = open('System.jpg', 'rb')
        bot.send_photo(message.from_user.id, file, caption= "Система 'Самооздоровления в ходе повседневных дел' обеспечивает оздоровление в ходе повседневных дел , весь период "
                                                               "бодрствования и даже во сне , а не в определенное время занятий в спортзале , юассейне или во время пробежек...")
    elif message.text == "Видеолекции":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создаем клавиатуру
        item1 = types.KeyboardButton("Правило 5 пальцев")  # Макет кнопки
        item2 = types.KeyboardButton("2")
        item3 = types.KeyboardButton("3")
        back = types.KeyboardButton("Назад")
        markup.add(item1, item2, item3, back)
        bot.send_message(message.from_user.id, "Видеолекции", reply_markup=markup)
    elif message.text == "Правило 5 пальцев":
        file = open('5fingers.mp4', 'rb')
        bot.send_document(message.from_user.id, file)

    elif message.text == "Назад":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создаем клавиатуру
        item1 = types.KeyboardButton("О системе")  # Макет кнопки
        item2 = types.KeyboardButton("Видеолекции")
        item3 = types.KeyboardButton("Расписание")
        item4 = types.KeyboardButton("Об авторе")
        markup.add(item1, item2, item3, item4)
        bot.send_message(message.from_user.id, "Назад", reply_markup=markup)

    user_id = message.from_user.id
    update_messages_count(user_id)

@server.route(f"/{BOT_TOKEN}", methods=["POST"])
def redirect_message():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))