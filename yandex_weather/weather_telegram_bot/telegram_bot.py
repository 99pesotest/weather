
import sys
sys.path.append('.')
import os
from django import setup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yandex_weather.settings")
setup()

from django.utils import timezone
from django.conf import settings
from weatherapp.models import City, Weather
from weatherapp.utils import update_weather_data
from datetime import timedelta

from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def get_city(city_name):

    try:
        city_object = City.objects.get(name__iexact=city_name)
    except City.DoesNotExist:
        error_response = {'error': f'Город {city_name} не найден',
                          'data': dict()}
        return error_response

    return city_object


def weather_detail(city_object):

    weather_objects = Weather.objects.filter(city=city_object)
    if weather_objects:
        time_since_update = timezone.now() - weather_objects[0].last_update_time

        if time_since_update > timedelta(minutes=30):
            update_weather_data(city_object)
            weather_objects = Weather.objects.filter(city=city_object)

    else:
        update_weather_data(city_object)
        weather_objects = Weather.objects.filter(city=city_object)

    data = dict()
    for forecast in weather_objects:
        data[forecast.time_of_day] = {'temperature': forecast.temperature,
                                      'pressure': forecast.pressure,
                                      'wind_speed': forecast.wind_speed}

    return {'data': data, 'error': None}


def start(update, context):
    keyboard = [[KeyboardButton("Узнать погоду")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    context.bot.send_message(chat_id=update.message.chat_id,
                             text='Привет! Нажми кнопку и потом отправь название города.',
                             reply_markup=reply_markup)


def help(update, context):
    text = "Чтобы узнать погоду, запустите бота командой /start."
    context.bot.send_message(chat_id=update.message.chat_id, text=text)


def format_message(city_name, data):
    message = f"Погода в городе {city_name} сегодня:\n"
    russian_dict_time = {"night": "Ночь", "morning": "Утро", "day": "День", "evening": "Вечер"}
    time_of_day_typle = ("night", "morning", "day", "evening")
    for time_of_day in time_of_day_typle:
        forecast = data.get(time_of_day)
        message += "\n".join((f"{russian_dict_time.get(time_of_day)}:",
                             f"\tТемпература: {forecast.get('temperature')}°C",
                             f"\tДавление: {forecast.get('pressure')} мм рт. ст.",
                             f"\tСкорость ветра: {forecast.get('wind_speed')} м/с\n\n"))
    return message


def weather(update, context):
    try:
        city_name = update.message.text
        city_object = get_city(city_name)

        if isinstance(city_object, dict):
            update.message.reply_text(city_object.get("error"))

        weather_data = weather_detail(city_object)
        data = weather_data.get("data")
        response_text = format_message(city_name, data)

        update.message.reply_text(response_text)
    except ValueError as e:
        update.message.reply_text(str(e))


def button_click(update, context):
    text = update.message.text
    context.bot.send_message(chat_id=update.message.chat_id, text=f'Вы нажали кнопку "{text}".')


def main():

    updater = Updater(token=settings.TELEGRAM_BOT_API_KEY, use_context=True)

    application = updater.dispatcher

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(MessageHandler(Filters.text & ~Filters.command, weather))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
