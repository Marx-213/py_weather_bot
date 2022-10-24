import requests
from pprint import pprint
from config import CODE_TO_SMILE, TEMP_TO_SMILE_DICT
import datetime as dt


city_name = 'pavlodar'
APIkey = '6576114cc454fa857b821f49c2e70be6'
# url = f'http://api.openweathermap.org/data/2.5/forecast/daily?q={city_name}&cnt={cnt}&appid={APIkey}'
url = f'https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={APIkey}&units=metric&lang=ru'
response = requests.get(url)
data = response.json()
main = data['city']
city = data['city']['name']
timezone = data['city']['timezone']
sunrise = data['city']['sunrise']
sunset = data['city']['sunset']
print(main)
pprint(data)
print(sunrise)
print(sunset)
right_sunrise = dt.datetime.fromtimestamp(sunrise)
right_sunset = dt.datetime.fromtimestamp(sunset)
print(right_sunrise)
print(right_sunset)
print()


def temp_to_smile(temp: str) -> str:
    if int(temp) >= 28:
        temp_smile = TEMP_TO_SMILE_DICT['Heat']
    elif 10 < int(temp) < 28:
        temp_smile = TEMP_TO_SMILE_DICT['Norm']
    else:
        temp_smile = TEMP_TO_SMILE_DICT['Cold']
    return temp_smile


main = data['list'][8]
dt_txt = data['list'][8]['dt_txt']
weather = data['list'][8]['weather']
description = data['list'][8]['weather'][0]['description']
wind_speed = data['list'][8]['wind']['speed']
pprint(dt_txt)
pprint(description)
pprint(wind_speed)
main = data['list'][8]['main']
feels_like = data['list'][8]['main']['feels_like']
temp = data['list'][8]['main']['temp']
humidity = data['list'][8]['main']['humidity']
print(timezone, 'timezone')
print(temp, 'temp')
print(humidity)
print(feels_like)
print()
temp_smile = temp_to_smile(temp)
print(description, 'dfaafdfad')
if description in CODE_TO_SMILE:
    weather_description = CODE_TO_SMILE[description]
else:
    weather_description = ''

message_date = (
            f'Дата{dt_txt}'
            f'Город: {city}, {weather_description}\n'
            f'Температура: {temp} C° {temp_smile}\n'
            f'Ощущается как {feels_like} C°{temp_smile}\n'
            f'Погода: {description} \nВлажность: {humidity}% 💧\n'
            f'Ветер: {wind_speed} м/с \nРассвет: {right_sunrise}\n'
            f'Закат: {right_sunset}'
        )
print(message_date)

# main = data['list'][10]
# date = data['list'][10]['dt_txt']
# print(date)
# print()
# main = data['list'][10]['main']
# temp = data['list'][10]['main']['temp']
# humidity = data['list'][10]['main']['humidity']
# print()
# pprint(main)
# print()

# main = data['list'][12]
# date = data['list'][12]['dt']
# date = data['list'][12]['dt_txt']
# print(date)
# print()
# main = data['list'][12]['main']
# temp = data['list'][12]['main']['temp']
# humidity = data['list'][12]['main']['humidity']
# print()
# pprint(main)
# print()

# main = data['list'][14]
# date = data['list'][14]['dt']
# date = data['list'][14]['dt_txt']
# print(date)
# print()
# main = data['list'][14]['main']
# temp = data['list'][14]['main']['temp']
# humidity = data['list'][14]['main']['humidity']
# print()
# pprint(main)
# print()
