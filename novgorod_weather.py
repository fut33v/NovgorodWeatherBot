# coding=utf-8
import re
import bot_util

__author__ = 'fut33v'

_URL_WEATHER = "http://novgorod.ru/weather"

_regexp_colortable = re.compile("<table class=\"colortable\".*?/table>", re.DOTALL)

_regexp_temperature_center_row = re.compile("<tr><td>Центр.*?</td></tr>", re.DOTALL)
_regexp_common_for_temperature_from_row = re.compile("<td style.*?>(.*?)</td>")

_regexp_humidity = re.compile("<td>Влажность</td><td.*?>(.*)</td>")

_regexp_pressure = re.compile("<td>Давление</td><td>.*?>(.*?)</span>")

_regexp_wind = re.compile("<td>Направление</td><td><img.*?>(.*?)</td>")
_regexp_wind_speed = re.compile("<td>Скорость</td><td>(.*?)<span.*?>(.*?)</span></td>")


def get_first_table(weather_page):
    first_table = _regexp_colortable.findall(weather_page)[0]
    return first_table


def _get_temperature_from_page(weather_page):
    temperature_center_row = _regexp_temperature_center_row.findall(weather_page)[0]
    m = _regexp_common_for_temperature_from_row.search(temperature_center_row)
    if m is not None:
        temperature_center_string = m.group(1)
        tmp = temperature_center_string.split(' ')
        if len(tmp) > 1:
            temperature_center = tmp[0]
            return temperature_center
    return None


def _get_humidity_from_page(weather_page):
    t = get_first_table(weather_page)
    m = _regexp_humidity.search(t)
    if m is not None:
        humidity = m.group(1)
        return humidity


def _get_pressure_from_page(weather_page):
    # t = get_first_table(weather_page)
    m = _regexp_pressure.search(weather_page)
    if m is not None:
        pressure = m.group(1)
        return pressure


def _get_wind_from_page(weather_page):
    t = get_first_table(weather_page)
    m = _regexp_wind.search(t)
    if m is not None:
        wind = m.group(1)
        m = _regexp_wind_speed.search(t)
        if m is not None:
            wind += " " + m.group(1)
            wind += " " + m.group(2)
            wind = wind[1:]
        return wind


def get_temperature():
    page = bot_util.urlopen(_URL_WEATHER)
    if not page:
        return None
    return _get_temperature_from_page(page)


def get_humidity():
    page = bot_util.urlopen(_URL_WEATHER)
    if not page:
        return None
    return _get_humidity_from_page(page)


def get_pressure():
    page = bot_util.urlopen(_URL_WEATHER)
    if not page:
        return None
    return _get_pressure_from_page(page)


def get_wind():
    page = bot_util.urlopen(_URL_WEATHER)
    if not page:
        return None
    return _get_wind_from_page(page)


def get_weather():
    page = bot_util.urlopen(_URL_WEATHER)
    if not page:
        return None
    temperature = _get_temperature_from_page(page)
    humidity = _get_humidity_from_page(page)
    pressure = _get_pressure_from_page(page)
    wind = _get_wind_from_page(page)
    weather = ""
    if temperature is not None:
        weather += build_temperature_string(temperature)
    if humidity is not None:
        weather += build_humidity_string(humidity)
    if pressure is not None:
        weather += build_pressure_string(pressure)
    if wind is not None:
        weather += build_wind_string(wind)
    return weather


def build_temperature_string(temperature):
    return "*Температура:* %s°C\n" % temperature


def build_humidity_string(humidity):
    return "*Влажность:* " + humidity + "\n"


def build_pressure_string(pressure):
    return "*Давление:* %s мм. рт. ст.\n" % pressure


def build_wind_string(wind):
    return "*Ветер:* %s " % wind


if __name__ == "__main__":
    print "temperature", get_temperature()
    print "weather", get_weather()
