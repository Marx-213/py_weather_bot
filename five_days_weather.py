from typing import Literal, Optional
import requests
from http import HTTPStatus
import logging
from calculating_funcs import temp_to_smile, calculate_right_timezone


def get_api_five_days(
            city: str,
            WEATHER_TOKEN: str
        ) -> dict[str, str] | Literal[400]:
    """Делает запрос к URL, возвращает json-файл."""
    url = (
        f'https://api.openweathermap.org/data/2.5/forecast?'
        f'q={city}&appid={WEATHER_TOKEN}&units=metric&lang=ru'
    )
    response = requests.get(url)
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


def get_five_days_weather(data: str) -> Optional[str]:
    '''Принимает json-файл '''
    try:
        city = data['city']['name']
        timezone = data['city']['timezone']
        sunrise = data['city']['sunrise']
        sunset = data['city']['sunset']
        right_sunrise = calculate_right_timezone(timezone, sunrise)
        right_sunset = calculate_right_timezone(timezone, sunset)
        for i in range(9):
            dt_txt = data['list'][i]['dt_txt']
            if dt_txt.endswith('12:00:00'):
                day_1 = i
                day_2 = i + 8
                day_3 = i + 16

        dt_txt = data['list'][day_1]['dt_txt']
        description = data['list'][day_1]['weather'][0]['description']
        wind_speed = data['list'][day_1]['wind']['speed']
        feels_like = data['list'][day_1]['main']['feels_like']
        temp = data['list'][day_1]['main']['temp']
        humidity = data['list'][day_1]['main']['humidity']
        temp_smile = temp_to_smile(temp)

        dt_txt_2 = data['list'][day_2]['dt_txt']
        description_2 = data['list'][day_2]['weather'][0]['description']
        wind_speed_2 = data['list'][day_2]['wind']['speed']
        feels_like_2 = data['list'][day_2]['main']['feels_like']
        temp_2 = data['list'][day_2]['main']['temp']
        humidity_2 = data['list'][day_2]['main']['humidity']
        temp_smile_2 = temp_to_smile(temp_2)

        dt_txt_3 = data['list'][day_3]['dt_txt']
        description_3 = data['list'][day_3]['weather'][0]['description']
        wind_speed_3 = data['list'][day_3]['wind']['speed']
        feels_like_3 = data['list'][day_3]['main']['feels_like']
        temp_3 = data['list'][day_3]['main']['temp']
        humidity_3 = data['list'][day_3]['main']['humidity']
        temp_smile_3 = temp_to_smile(temp_3)

        message_date = (
                    f'Город: {city} 🏢\n'
                    f'Рассвет: {right_sunrise}\n'
                    f'Закат: {right_sunset}\n\n'

                    f'Дата: {dt_txt}\n'
                    f'Температура: {temp}C° {temp_smile}\n'
                    f'Ощущается как {feels_like}C°{temp_smile}\n'
                    f'Погода: {description} \nВлажность: {humidity}% 💧\n'
                    f'Ветер: {wind_speed} м/с\n\n'

                    f'Дата: {dt_txt_2}\n'
                    f'Температура: {temp_2}C° {temp_smile_2}\n'
                    f'Ощущается как {feels_like_2}C° {temp_smile_2}\n'
                    f'Погода: {description_2} \nВлажность: {humidity_2}% 💧\n'
                    f'Ветер: {wind_speed_2} м/с\n\n'

                    f'Дата: {dt_txt_3}\n'
                    f'Температура: {temp_3}C° {temp_smile_3}\n'
                    f'Ощущается как {feels_like_3}C°{temp_smile_3}\n'
                    f'Погода: {description_3} \nВлажность: {humidity_3}% 💧\n'
                    f'Ветер: {wind_speed_3} м/с\n'
                )
        return message_date
    except Exception as error:
        logging.error(f'Произошла ошибка: {error}')
        print(f'Проверьте название города. Ошибка: {error}')
