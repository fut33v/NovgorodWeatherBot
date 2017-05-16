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
    wind = None
    weather = ""
    try:
        j = json.loads(page)
        if 'outsideTemp' in j:
            temperature = j['outsideTemp']
        if 'barometer' in j:
            pressure = j['barometer']
        if 'rain' in j:
            rain = j['rain']
        if 'windDirectionDegrees' in j and 'windSpeed' in j and 'windBeaufortScale':
            wind = (j['windDirectionDegrees'], j['windSpeed'], j['windBeaufortScale'])
    except Exception as e:
        print e
    if temperature is not None:
        weather += build_temperature_string(temperature)
    if pressure is not None:
        weather += build_pressure_string(pressure)
    if rain is not None:
        weather += build_rain_string(rain)
    if wind is not None:
        wind = build_wind_string(wind[0], wind[1], wind[2])
        if wind is not None:
            weather += wind

    return weather


def build_temperature_string(temperature):
    return u"*Температура:* %s°C\n" % temperature


def build_pressure_string(pressure):
    return u"*Давление:* %s мм. рт. ст.\n" % pressure


def build_rain_string(rain):
    if rain == "no":
        rain = u"нет"
    return u"*Дождь:* %s.\n" % rain


def build_wind_string(direction, speed, scale):
    try:
        direction = int(direction)
        speed = float(speed)
        scale = int(scale)
    except Exception:
        return None
    direction_string = u""
    if 330 < direction < 360 or 0 <= direction < 30:
        direction_string = u"Северный"
    if 60 < direction < 120:
        direction_string = u"Восточный"
    if 150 < direction < 210:
        direction_string = u"Южный"
    if 240 < direction < 300:
        direction_string = u"Западный"
    if 30 < direction < 60:
        direction_string = u"Северо-Восточный"
    if 120 < direction < 150:
        direction_string = u"Юго-Восточный"
    if 210 < direction < 240:
        direction_string = u"Юго-Западный"
    if 300 < direction < 330:
        direction_string = u"Северо-Западный"

    return u"*Ветер:* %.1f м/с, %d балл(а/ов) %s.\n" % (speed, scale, direction_string)


if __name__ == "__main__":
    print "temperature", get_temperature()
    print "barometer", get_pressure()
    print "rain", get_rain()
    print "weather", get_weather()
