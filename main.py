import datetime as dt
import logging
from http import HTTPStatus
from typing import Any, Literal, Optional

import requests
import telebot

from config import TOKEN, WEATHER_TOKEN


bot = telebot.TeleBot(TOKEN)
logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    filemode='w',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)
current_seconds = 21600
temp_to_smile_dict = {
    'Heat': '\U0001F525',
    'Norm': '\U0001f321',
    'Cold': '\U00002744',
}
code_to_smile = {
    'Clear': 'Ясно \U00002600',
    'Clouds': 'Облачно \U00002601',
    'Rain': 'Дождь \U00002614',
    'Drizzle': 'Дождь \U00002614',
    'Thunderstorm': 'Гроза \U0001F329',
    'Snow': 'Снег \U0001F328',
    'Mist': 'Туман \U0001F32B'
}


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

        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
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
        temp_smile = temp_to_smile_dict['Heat']
    elif 10 < int(temp) < 28:
        temp_smile = temp_to_smile_dict['Norm']
    else:
        temp_smile = temp_to_smile_dict['Cold']
    return temp_smile


def calculate_right_timezone(timezone: int, sunrise: int) -> int:
    if current_seconds <= timezone:
        a = sunrise - (timezone - current_seconds)
    else:
        a = sunrise - (current_seconds - timezone)
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
    bot.polling()


if __name__ == '__main__':
    main()
