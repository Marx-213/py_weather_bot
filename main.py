import logging
import time
from typing import Any
import telebot
from dotenv import load_dotenv
from telebot import types
from db_funcs import db_user_save, select_all_users_id
from weather_tomorrow import get_api_tomorrow, get_tomorrow_weather
from current_weather import get_api_answer, get_location, get_weather
from five_days_weather import get_api_five_days, get_five_days_weather
import os


load_dotenv()
TOKEN = os.getenv('TOKEN')
WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')
bot = telebot.TeleBot(TOKEN)
WEATHER_TOKEN = WEATHER_TOKEN
bot = telebot.TeleBot(TOKEN)
logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    filemode='a',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)


@bot.message_handler(commands=['start'])
def start(message: Any) -> None:
    # markup = types.InlineKeyboardMarkup(row_width=2)
    # item = types.InlineKeyboardButton(
    # 'Погода на завтра',
    # callback_data='weather_tomorrow')
    # item2 = types.InlineKeyboardButton(
    # 'Погода на на 3 дня',
    # callback_data='weather_5_days')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Погода на завтра')
    btn2 = types.KeyboardButton('Погода на 3 дня')
    markup.add(btn1, btn2)
    db_user_save(message.chat.id)
    # markup.add(item, item2)
    bot.send_message(
        message.chat.id,
        (
            'Я погодный бот! ☀️⛅️🌧❄️\n'
            'Введите город, чтобы получить погоду на сегодня '
            'или выберите другой вариант'
        ),
        reply_markup=markup
    )


@bot.message_handler(commands=['allusers'])
def send_message_to_all_users(message: Any) -> None:
    all_users = select_all_users_id()
    for i in range(len(all_users)):
        bot.send_message(
            all_users[i][0],
            (
                f'Приветствую, {message.from_user.id}]\n {message.from_user.first_name}}!✋🏼'
                f'{message.from_user.last_name} {message.from_user.username}'
                'Если тебе пришло  это сообщение,'
                ' то это значит, что ты когда-то использовал этого бота\n'
                'У меня появились новые функциии'
            )
        )


def back_main_menu(message: Any) -> None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Погода на завтра')
    btn2 = types.KeyboardButton('Погода на 3 дня')
    markup.add(btn1, btn2)
    msg = bot.send_message(
        message.chat.id,
        ('Вы в главном меню, просто напишите название '
         'города или нажмите на одну из кнопок'),
        reply_markup=markup
    )
    bot.register_next_step_handler(msg, send_message)


def tmrrw_weather(message: Any) -> None:
    if message.text == '<<< Назад':
        back_main_menu(message)
    elif message.text == 'Погода на 3 дня':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('<<< Назад')
        btn2 = types.KeyboardButton('Погода на завтра')
        markup.add(btn1, btn2)
        msg = bot.send_message(
            message.chat.id,
            'Ок, введите город, чтобы получить погоду на ближайшие 3 дня',
            reply_markup=markup
        )
        bot.register_next_step_handler(msg, five_days_weather)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('<<< Назад')
        btn2 = types.KeyboardButton('Погода на 3 дня')
        markup.add(btn1, btn2)
        response = get_api_tomorrow(message.text, WEATHER_TOKEN)
        if response == 400:
            msg = bot.send_message(
                message.chat.id,
                'Город не найден, попробуйте еще',
                reply_markup=markup
            )
            bot.register_next_step_handler(msg, tmrrw_weather)
        weather = get_tomorrow_weather(response)
        msg = bot.send_message(
            message.chat.id,
            weather,
            reply_markup=markup
        )
        bot.register_next_step_handler(msg, tmrrw_weather)


def five_days_weather(message: Any) -> None:
    if message.text == '<<< Назад':
        back_main_menu(message)
    elif message.text == 'Погода на завтра':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('<<< Назад')
        btn2 = types.KeyboardButton('Погода на 3 дня')
        markup.add(btn1, btn2)
        msg = bot.send_message(
            message.chat.id,
            'Ок, введите город, чтобы получить погоду на завтра',
            reply_markup=markup
        )
        bot.register_next_step_handler(msg, tmrrw_weather)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('<<< Назад')
        btn2 = types.KeyboardButton('Погода на завтра')
        markup.add(btn1, btn2)
        response = get_api_five_days(message.text, WEATHER_TOKEN)
        if response == 400:
            msg = bot.send_message(
                message.chat.id,
                'Город не найден, попробуйте еще',
                reply_markup=markup
            )
            bot.register_next_step_handler(msg, five_days_weather)
        weather = get_five_days_weather(response)
        msg = bot.send_message(
            message.chat.id,
            weather,
            reply_markup=markup
        )
        bot.register_next_step_handler(msg, five_days_weather)


@bot.message_handler(content_types='text')
def send_message(message: Any) -> None:
    if message.text == 'Погода на завтра':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('<<< Назад')
        btn2 = types.KeyboardButton('Погода на 3 дня')
        markup.add(btn1, btn2)
        msg = bot.send_message(
            message.chat.id,
            'Ок, введите город, чтобы получить погоду на завтра',
            reply_markup=markup
        )
        bot.register_next_step_handler(msg, tmrrw_weather)
    elif message.text == 'Погода на 3 дня':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('<<< Назад')
        btn2 = types.KeyboardButton('Погода на 3 дня')
        markup.add(btn1, btn2)
        msg = bot.send_message(
            message.chat.id,
            'Ок, введите город, чтобы получить погоду на ближайшие 3 дня',
            reply_markup=markup
        )
        bot.register_next_step_handler(msg, five_days_weather)
    else:
        response = get_api_answer(message.text, WEATHER_TOKEN)
        if response == 400:
            bot.send_message(
                message.chat.id,
                'Город не найден, попробуйте еще раз'
            )
        lon, lat = get_location(response)
        weather = get_weather(response)
        bot.send_message(message.chat.id, weather)
        bot.send_location(message.chat.id, lon, lat)
# @bot.callback_query_handler(func=lambda call:True)
# def callback(call):
#     if call.message:
#         if call.data == 'weather_tomorrow':
#             bot.send_message(call.message.chat.id, 'пкhhtrh')
#         if call.data == 'weather_5_days':
#             bot.send_message(call.message.chat.id, 'пкпуп')


def main() -> None:
    while True:
        try:
            logging.info("Bot running..")
            bot.polling(none_stop=True, interval=2)
            break
        except telebot.apihelper.ApiException as e:
            logging.error(e)
            bot.stop_polling()
            time.sleep(15)
            logging.info("Running again!")


if __name__ == '__main__':
    main()
