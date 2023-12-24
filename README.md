## test yandex weather

[Telegram bot](https://t.me/my_test_yandex_weather_bot)

[Пример API](http://34.118.86.83/weather/?city=омск)

#### Пример настройки для запуска в Ubuntu + Django + uWsgi + Nginx + Mysql:

Создать MySQL базу, логин/пароль/имя базы нужены будут дальше, а так же получить у [@BotFather](https://t.me/BotFather) API-key для бота.

Клонировать репозиторий и перейти в рабочую директорию
```bash
$ git clone https://github.com/99pesotest/weather.git
$ cd weather
```

Запустить deploy.sh который установит библиотеки и зависимости
```shell
$ ./deploy.sh
```
В процессе установки будет вызван **.env** файл для редактирования.

Дальше по инструкции:
[Простая настройка uWsgi + Nginx + Django](https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-uwsgi-and-nginx-on-ubuntu-16-04)