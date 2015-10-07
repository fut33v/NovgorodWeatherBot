# NovgorodWeatherBot

Telegram Бот, который позволяет узнать текущую погоду в Великом Новгороде.

http://telegram.me/NovgorodWeatherBot

Парсит погоду с сайта *Novgorod.ru* (http://novgorod.ru/weather)

Использует long-polling модель (метод getUpdates, для использования которого не обязательно иметь https сертификат,
http://habrahabr.ru/post/262247/ пункт 7)

##Запуск:

- Получите token и запишите его в файл token в той же директории что и скрипты бота

- Зупустите bot_poll.py
