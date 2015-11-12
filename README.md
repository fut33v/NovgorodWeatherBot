# NovgorodWeatherBot : HELLO WORLD FOR TELEGRAM BOT API

Telegram Bot, which allows you get current weather and forecast for city Velikiy Novgorod, RUSSIA

http://telegram.me/NovgorodWeatherBot

Parsing current weather data from site *Novgorod.ru* (http://novgorod.ru/weather)

Getting forecast with Yandex.Weather and Weather.com API

Uses long-polling model (method getUpdates of Telegram Bot API)

##Run:

- Get *token* Telegram Bot API and write it to data/token
- Get *token* for botan.io (Yandex.Appmetrica) and write it to data/botan_token
- Get *token* for Weather.com API and write it to data/weather_com_token
- Run *novgorod_weather_bot.py*

# NovgorodWeatherBot : HELLO WORLD ДЛЯ TELEGRAM BOT API

Telegram Bot, который позволяет узнать текущую погоду в Великом Новгороде.

http://telegram.me/NovgorodWeatherBot

Парсит погоду с сайта *Новгород.ру* (http://novgorod.ru/weather)

Получает прогноз с Яндекс.Погоды и Weather.com API

Использует long-polling модель (метод getUpdates, для использования которого не нужен https сертификат,
http://habrahabr.ru/post/262247/ пункт 7)

##Запуск:

- Получите *token* Telegram Bot API и запишите его в файл data/token
- Получите *token* для botan.io (Yandex.Appmetrica) и запишите его в файл data/botan_token
- Получите *token* для Weather.com API и запишите его в файл data/weather_com_token
- Запустите *novgorod_weather_bot.py*
