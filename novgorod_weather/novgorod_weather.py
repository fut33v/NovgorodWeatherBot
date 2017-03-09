# coding=utf-8

import json
from util import bot_util

__author__ = 'fut33v'

_URL_WEATHER = "https://www.novgorod.ru/weather/extensions/GoogleChrome/json.php"


def get_temperature():
    page = bot_util.urlopen(_URL_WEATHER)
    if not page:
        return None
    try:
        j = json.loads(page)
        if 'outsideTemp' in j:
            return j['outsideTemp']
    except Exception as e:
        print e
    return None


def get_pressure():
    page = bot_util.urlopen(_URL_WEATHER)
    if not page:
        return None
    try:
        j = json.loads(page)
        if 'barometer' in j:
            return j['barometer']
    except Exception as e:
        print e
    return None


def get_rain():
    page = bot_util.urlopen(_URL_WEATHER)
    if not page:
        return None
    try:
        j = json.loads(page)
        if 'rain' in j:
            return j['rain']
    except Exception as e:
        print e
    return None


def get_weather():
    page = bot_util.urlopen(_URL_WEATHER)
    if not page:
        return None
    temperature = None
    pressure = None
    rain = None
    weather = ""
    try:
        j = json.loads(page)
        if 'outsideTemp' in j:
            temperature = j['outsideTemp']
        if 'barometer' in j:
            pressure = j['barometer']
        if 'rain' in j:
            rain = j['rain']
    except Exception as e:
        print e
    if temperature is not None:
        weather += build_temperature_string(temperature)
    if pressure is not None:
        weather += build_pressure_string(pressure)
    if rain is not None:
        weather += build_rain_string(rain)

    return weather


def build_temperature_string(temperature):
    return u"*Температура:* %s°C\n" % temperature


def build_pressure_string(pressure):
    return u"*Давление:* %s мм. рт. ст.\n" % pressure


def build_rain_string(rain):
    if rain == "no":
        rain = u"нет"
    return u"*Дождь:* %s.\n" % rain


if __name__ == "__main__":
    print "temperature", get_temperature()
    print "barometer", get_pressure()
    print "rain", get_rain()
    print "weather", get_weather()
