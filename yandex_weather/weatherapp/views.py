
from django.http import JsonResponse
from django.utils import timezone
from .models import City, Weather
from .utils import update_weather_data
from datetime import timedelta


def get_city(request):
    city_name = request.GET.get('city', '')

    try:
        city_object = City.objects.get(name__iexact=city_name)
    except City.DoesNotExist:
        error_response = {'error': f'City not found: {city_name}',
                          'data': dict()}
        return JsonResponse(error_response, status=404)

    return city_object


def weather_detail(request):
    city_object = get_city(request)

    # Возвращаем ошибку, если в базе нет запрашиваемого города
    if isinstance(city_object, JsonResponse):
        return city_object

    try:
        weather_object = Weather.objects.get(city=city_object, time_of_day='current')
        time_since_update = timezone.now() - weather_object.last_update_time

        if time_since_update > timedelta(minutes=30):
            update_weather_data(city_object)
            weather_object = Weather.objects.get(city=city_object, time_of_day='current')

    except Weather.DoesNotExist:
        update_weather_data(city_object)
        weather_object = Weather.objects.get(city=city_object, time_of_day='current')

    return JsonResponse({'data': {'temperature': weather_object.temperature,
                                 'pressure': weather_object.pressure,
                                 'wind_speed': weather_object.wind_speed},
                         'error': None})
