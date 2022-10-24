from pprint import pprint
import requests
import datetime as dt

CURRENT_SECONDS = 21600
city = 'pavlodar'
city = 'london'
WEATHER_TOKEN = '69f40d825b265b547e6f29f85c6937b8'
response = requests.get(
        f'https://api.openweathermap.org/data/2.5/'
        f'weather?q={city}&appid={WEATHER_TOKEN}&units=metric&lang=ru'
    )

pprint(response.json())
data = response.json()
timezone = data['timezone']
sunrise = data['sys']['sunrise']
sunset = data['sys']['sunset']
print(type(sunrise))

message_date = (
    f'Рассвет: {sunrise}\n'
    f'Закат: {sunset}\n'
    f'timezone: {timezone}'
)
sunrise = dt.datetime.fromtimestamp(sunrise)
sunset = dt.datetime.fromtimestamp(sunset)
message_date2 = (
    f'Рассвет2: {sunrise}\n'
    f'Закат2: {sunset}\n'
    f'timezone2: {timezone}'

)
print(message_date)
print(message_date2)
timezone = data['timezone']
sunrise = data['sys']['sunrise']
sunset = data['sys']['sunset']

def calculate_right_timezone(timezone: int, sunrise: int) -> int:
    if CURRENT_SECONDS <= timezone:
        a = sunrise - (timezone - CURRENT_SECONDS)
    else:
        a = sunrise - (CURRENT_SECONDS - timezone)
    sunrise = dt.datetime.fromtimestamp(a)
    return sunrise


right_sunrise = calculate_right_timezone(timezone, sunrise)
right_sunset = calculate_right_timezone(timezone, sunset)


message_date2 = (
    f'Рассвет3: {right_sunrise}\n'
    f'Закат3: {right_sunset}\n'
    f'timezone3: {timezone}'
)
print(message_date2)
print(dt.datetime.now())