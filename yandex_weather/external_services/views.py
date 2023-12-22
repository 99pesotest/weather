
from django.conf import settings
import requests


def format_data(raw_data):
    result_data = dict()
    fact = raw_data.get('fact')
    result_data['current'] = {'temperature': fact.get('temp'),
                              'pressure': fact.get('pressure_mm'),
                              'wind_speed': fact.get('wind_speed'),
                              'humidity': fact.get('humidity'),
                              'precipitation': fact.get('prec_strength'),
                              }

    parts = raw_data.get('forecasts')[0].get('parts')
    parts_keys = ('night', 'morning', 'day', 'evening')
    for key in parts_keys:
        data = parts.get(key)
        result_data[key] = {'temperature': data.get('temp_avg'),
                            'pressure': data.get('pressure_mm'),
                            'wind_speed': data.get('wind_speed'),
                            'humidity': data.get('humidity'),
                            'precipitation': data.get('prec_strength'),
                            }

    return result_data


def get_weather_data(city):
    yandex_url = f"{settings.YANDEX_API_URL}?lat={city.latitude}&lon={city.longitude}"

    headers = {'X-Yandex-API-Key': settings.YANDEX_WEATHER_API_KEY,}

    response = requests.get(yandex_url, headers=headers, timeout=5)

    weather_data = format_data(response.json())
    return weather_data
