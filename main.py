import datetime as dt
import logging
import os
import time
from http import HTTPStatus
from typing import Any, Literal, Optional

import requests
import telebot
from dotenv import load_dotenv

from config import CODE_TO_SMILE, CURRENT_SECONDS, TEMP_TO_SMILE_DICT

load_dotenv()
TOKEN = os.getenv('TOKEN')
WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')
bot = telebot.TeleBot(TOKEN)
logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    filemode='w',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)


def get_api_answer(city: str,
                   WEATHER_TOKEN: str
                   ) -> dict[str, str] | Literal[400]:
    """Делает запрос к URL, возвращает json-файл."""
    response = requests.get(
        f'https://api.openweathermap.org/data/2.5/'
        f'weather?q={city}&appid={WEATHER_TOKEN}&units=metric&lang=ru'
    )
    if response.status_code != HTTPStatus.OK:
        logging.error(f'Сайт не доступен, код ответа {response.status_code}')
        return 400
    try:
        response = response.json()
        logging.info(f'Получен ответ: {response}')
        return response
    except Exception as error:
        logging.error(f'Произошла ошибка: {error}')
        raise Exception(f'Произошла ошибка: {error}')


def get_weather(response: str) -> Optional[str]:
    '''Принимает json-файл '''
    try:
        data = response
        city = data['name']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        feels_like = data['main']['feels_like']
        wind = data['wind']['speed']
        weather = data['weather'][0]['description']
        weather_description = data['weather'][0]['main']
        timezone = data['timezone']
        sunrise = data['sys']['sunrise']
        sunset = data['sys']['sunset']
        right_sunrise = calculate_right_timezone(timezone, sunrise)
        right_sunset = calculate_right_timezone(timezone, sunset)
        temp_smile = temp_to_smile(temp)
        dtf = dt.datetime.now()

        if weather_description in CODE_TO_SMILE:
            wd = CODE_TO_SMILE[weather_description]
        else:
            wd = ''

        message_date = (
            f'Город: {city}, {wd}\nТемпература: {temp} C° {temp_smile}\n'
            f'Ощущается как {feels_like} C°{temp_smile}\n'
            f'Погода: {weather} \nВлажность: {humidity}% 💧\n'
            f'Ветер: {wind} м/с \nРассвет: {right_sunrise}\n'
            f'Закат: {right_sunset}'
        )
        return message_date

    except Exception as error:
        logging.error(f'Произошла ошибка: {error}')
        print(f'Проверьте название города. Ошибка: {error}')


def temp_to_smile(temp: str) -> str:
    if int(temp) >= 28:
        temp_smile = TEMP_TO_SMILE_DICT['Heat']
    elif 10 < int(temp) < 28:
        temp_smile = TEMP_TO_SMILE_DICT['Norm']
    else:
        temp_smile = TEMP_TO_SMILE_DICT['Cold']
    return temp_smile


def calculate_right_timezone(timezone: int, sunrise: int) -> int:
    if CURRENT_SECONDS <= timezone:
        a = sunrise + (timezone - CURRENT_SECONDS)
    else:
        a = sunrise + (CURRENT_SECONDS - timezone)
    sunrise = dt.datetime.fromtimestamp(a)
    return sunrise


@bot.message_handler(commands=['start'])
def start(message: Any) -> None:
    bot.send_message(
        message.chat.id,
        'Система включена, человек.\nВведите город:'
    )


@bot.message_handler(content_types='text')
def send_message(message: Any) -> None:
    response = get_api_answer(message.text, WEATHER_TOKEN)
    if response == 400:
        bot.send_message(
            message.chat.id,
            'Город не найден, попробуйте еще раз'
        )
    weather = get_weather(response)
    bot.send_message(message.chat.id, weather)


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
