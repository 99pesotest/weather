#!/bin/bash

echo "Установка пакетов..."
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv nginx

echo "Создание и активация виртуального окружения..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "Создание файла .env..."
cp .env.example .env
nano .env

echo "Применение миграций..."

python yandex_weather/manage.py migrate

echo "Установка и настройка Gunicorn..."
pip install wheel uwsgi

deactivate
