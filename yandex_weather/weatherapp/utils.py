
from .models import Weather
from external_services.views import get_weather_data


def update_weather_data(city):
    weather_data = get_weather_data(city)

    try:
        # Проверяем есть ли в базе записи о погоде для города
        weather_object = Weather.objects.get(city=city, time_of_day='current')

    except Weather.DoesNotExist:
        for time_of_day in weather_data.keys():
            weather_object = Weather.objects.create(city=city, time_of_day=time_of_day, **weather_data.get(time_of_day))
            weather_object.save()
    else:
        for time_of_day, values in weather_data.items():
            weather_object = Weather.objects.get(city=city, time_of_day=time_of_day)
            weather_object.temperature = values.get('temperature')
            weather_object.pressure = values.get('pressure')
            weather_object.wind_speed = values.get('wind_speed')
            weather_object.humidity = values.get('humidity')
            weather_object.precipitation = values.get('precipitation')
            weather_object.save()
