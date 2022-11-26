import datetime
import os
import telebot
import logging
import psycopg2
from flask import Flask, request
from telebot import types
import schedule, time

DATABASE_URL = os.environ['DATABASE_URL']
BOT_TOKEN = os.environ['BOT_TOKEN']
APP_URL = os.environ['APP_URL'] + BOT_TOKEN
DB_URI = os.environ['DB_URI']



bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)
logger = telebot.logger
logger.setLevel(logging.DEBUG)

db_connection = psycopg2.connect(DB_URI,sslmode="require")
db_object = db_connection.cursor()

button = {}

def update_messages_count(user_id): #Функция для счетчика сообщений от пользователя
    db_object.execute(f"UPDATE users SET messages=messages+1 WHERE user_id={user_id}")
    db_connection.commit()

def select_from_db(table, name):#функуция выбора  данных из таблиц
    db_object.execute(f"SELECT * FROM {table} WHERE name LIKE '{name}%'")
    result = db_object.fetchall()
    return (result)

def update_data_video_count(name_video): #Функция для счетчика запроса видео
    db_object.execute(f"UPDATE data_video SET count_views=count_views+1 WHERE name LIKE '{name_video}%'")
    db_connection.commit()



def job1(p):
    bot.send_message('838386449', 'Wake up!')

schedule.every(30).seconds.do(job1, p='Через 10 секунд')




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
        result = select_from_db("info", "author")
        if not result:
            bot.reply_to(message, "No data...")
        else:
            for i, item in enumerate(result):
                img_name = open(f'foto/{item[3].strip()}', 'rb')
                description = item[2].strip()
        bot.send_photo(message.from_user.id, img_name, caption= description)
    elif message.text == "О системе":
        result = select_from_db("info", "system")
        if not result:
            bot.reply_to(message, "No data...")
        else:
            for i, item in enumerate(result):
                img_name = open(f'foto/{item[3].strip()}', 'rb')
                description = item[2].strip()
        bot.send_photo(message.from_user.id, img_name, caption=description)
    elif message.text == "Видеолекции":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создаем клавиатуру
        result = select_from_db("data_video", "")
        if not result:
            bot.reply_to(message, "No data...")
        else:
            for i, item in enumerate(result):
                name_video = item[3].strip()
                description = item[2].strip()
                url_video = item[1].strip()
                button[name_video] = description + url_video
                markup.add(types.KeyboardButton(name_video)) # Макет кнопки
        markup.add(types.KeyboardButton("Назад"))
        bot.send_message(message.from_user.id, "Видеолекции", reply_markup=markup)

    elif message.text in button.keys(): # Проверяем есть ли запрос от пользователя в словаре с видео
        text = button.get(message.text)
        update_data_video_count(message.text)
        bot.send_message(message.from_user.id, text)

    elif message.text == "Назад":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создаем клавиатуру
        item1 = types.KeyboardButton("О системе")  # Макет кнопки
        item2 = types.KeyboardButton("Видеолекции")
        item3 = types.KeyboardButton("Расписание")
        item4 = types.KeyboardButton("Об авторе")
        markup.add(item1, item2, item3, item4)
        bot.send_message(message.from_user.id, "Назад", reply_markup=markup)
    elif message.text == "Расписание":
        print("Hfcgbcfybt ")







    user_id = message.from_user.id
    update_messages_count(user_id)



def sheduler_message():
    now = datetime.datetime.now()
    print(f"!!!!!!!!{now}")
    if (now.hour() > 8) and (now.hour() <20):
        if (now.minute() % 5==0):

            bot.send_message(838386449, 'Wake up!')

    else:
        print("Ошибка в часах")


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