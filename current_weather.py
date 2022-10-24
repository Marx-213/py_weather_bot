from typing import Any, Literal, Optional, Tuple
import requests
from http import HTTPStatus
import logging
from config import CODE_TO_SMILE
from calculating_funcs import temp_to_smile, calculate_right_timezone


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


def get_location(data: Any) -> Tuple:
    lon = data['coord']['lon']
    lat = data['coord']['lat']
    return lon, lat
