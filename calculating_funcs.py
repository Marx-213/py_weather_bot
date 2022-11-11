from config import TEMP_TO_SMILE_DICT, CURRENT_SECONDS
import datetime as dt


def temp_to_smile(temp: str) -> str:
    '''Возвращает смайлик в зависимости от температуры'''
    if int(temp) >= 28:
        temp_smile = TEMP_TO_SMILE_DICT['Heat']
    elif 10 < int(temp) < 28:
        temp_smile = TEMP_TO_SMILE_DICT['Norm']
    else:
        temp_smile = TEMP_TO_SMILE_DICT['Cold']
    return temp_smile


def calculate_right_timezone(timezone: int, sunrise: int) -> int:
    '''Считает правильное время рассвета или заката'''
    if CURRENT_SECONDS <= timezone:
        a = sunrise - (timezone - CURRENT_SECONDS)
    else:
        a = sunrise - (CURRENT_SECONDS - timezone)
    sunrise = dt.datetime.fromtimestamp(a)
    return sunrise
