
import requests


def get_weather_from_yandex(city_name, api_key):
    url = f'https://api.weather.yandex.ru/v2/informers'
    headers = {
        'X-Yandex-API-Key': api_key,
    }
    params = {
        'lat': '55.75396',
        'lon': '37.620393',
        'lang': 'ru_RU',
        'limit': '1',
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        fact = data['fact']
        temperature = fact['temp']
        pressure = fact['pressure_mm']
        wind_speed = fact['wind_speed']
        return {
            'temperature': temperature,
            'pressure': pressure,
            'wind_speed': wind_speed,
        }
    else:
        # Обработка ошибок
        return None