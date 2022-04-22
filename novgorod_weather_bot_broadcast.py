# coding=utf-8
from datetime import datetime
import os

import novgorod_weather_bot
from util import bot_util

__author__ = 'fut33v'

def broadcast_message(message):
    t = bot_util.read_one_string_file(novgorod_weather_bot.TOKEN_FILENAME)
    botan_t = bot_util.read_one_string_file(novgorod_weather_bot.BOTAN_TOKEN_FILENAME)
    bot = novgorod_weather_bot.NovgorodWeatherBot(t, name="NovgorodWeatherBot")
    lines = open(bot.chats_file, 'r').readlines()
    for l in lines:
        l = int(l)
        bot.send_response(l, message)

if __name__ == "__main__":
    while (True):
        m = raw_input ("> ")
        print type(m)
        broadcast_message(m)


