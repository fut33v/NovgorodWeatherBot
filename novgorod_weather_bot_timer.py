# coding=utf-8
from datetime import datetime
import os

from novgorod_forecast import novgorod_forecast
import novgorod_weather_bot
from util import bot_util

__author__ = 'fut33v'

t = bot_util.read_one_string_file(novgorod_weather_bot.TOKEN_FILENAME)
botan_t = bot_util.read_one_string_file(novgorod_weather_bot.BOTAN_TOKEN_FILENAME)
bot = novgorod_weather_bot.NovgorodWeatherBot(t, name="NovgorodWeatherBot", botan_token=botan_t)

while True:
    now = datetime.datetime.now()
    if now.hour == 6 and now.minute == 0:
        f = novgorod_forecast.get_forecast()
        if f:
            if os.path.exists(bot.chats_file):
                chats_file = open(bot.chats_file, 'r')
                if chats_file:
                    lines = chats_file.readlines()
                    for chat_id in lines
                        bot.send_response(chat_id, u"Здарова бандиты", True)
