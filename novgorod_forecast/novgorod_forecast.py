# coding=utf-8
import xml.etree.ElementTree as ET

from util import bot_util

__author__ = 'fut33v'

_URL_FORECAST_GISMETEO = "http://www.weather.com/weather/today/l/RSXX7553:1:RS"

"id=26179 region=10904"
_URL_FORECAST_YANDEX = "https://export.yandex.ru/weather-ng/forecasts/26179.xml"


def get_forecast():
    p = bot_util.urlopen(_URL_FORECAST_YANDEX)
    if not p:
        return False

    root = ET.fromstring(p)
    if root is None:
        return False

    NUMBER_OF_DAYS = 2
    days_list = []
    i = 0
    for child in root:
        if child.tag == _build_tag_name("day"):
            days_list.append(child)
            i += 1
            if i == NUMBER_OF_DAYS:
                break

    if len(days_list) != 2:
        return False

    today = days_list[0]
    tomorrow = days_list[1]
    today_forecast = _get_day_forecast_string(today)
    tomorrow_forecast = _get_day_forecast_string(tomorrow)
    if not today_forecast or not tomorrow_forecast:
        return False

    forecast = u"**Сегодня:**\n" + today_forecast + u"\n**Завтра**:\n" + tomorrow_forecast

    return forecast


def _get_day_forecast_string(day):
    if not isinstance(day, ET.Element):
        return False
    morning_forecast = "morning"
    day_forecast = "day"
    evening_forecast = "evening"
    night_forecast = "night"
    for child in day:
        if child.tag == "{http://weather.yandex.ru/forecast}day_part":
            if 'type' not in child.attrib:
                return False
            day_part_type = child.attrib['type']
            if day_part_type == morning_forecast:
                morning_forecast = child
            if day_part_type == day_forecast:
                day_forecast = child
            if day_part_type == evening_forecast:
                evening_forecast = child
            if day_part_type == night_forecast:
                night_forecast = child
    forecast = u""
    morning_forecast = _get_day_part_forecast_string(morning_forecast)
    forecast += u"Утро: " + morning_forecast + u"\n"
    day_forecast = _get_day_part_forecast_string(day_forecast)
    forecast += u"День: " + day_forecast + u"\n"
    evening_forecast = _get_day_part_forecast_string(evening_forecast)
    forecast += u"Вечер: " + evening_forecast + u"\n"
    night_forecast = _get_day_part_forecast_string(night_forecast)
    forecast += u"Ночь: " + night_forecast + u"\n"
    return forecast

def _build_tag_name(tag_name):
    return "{http://weather.yandex.ru/forecast}" + tag_name

def _get_day_part_forecast_string(day_part):
    temperature_range = False
    temp_from = u"??"
    temp_to = u"??"
    weather_type = u"??"
    temp = u"??"
    overcast_emoji = u"\u2601\ufe0f"
    rain_emoji = u"\u2614\ufe0f"
    drops_emoji = u"\U0001f4a6"
    snow_emoji = u"\u2744\ufe0f"
    cloudy_emoji = u"\u26c5\ufe0f"
    clear_emoji = u"\u2600\ufe0f"
    emoji = u""
    for child in day_part:
        if child.tag == _build_tag_name("temperature"):
            temperature_range = False
            temp = child.text
        if child.tag == _build_tag_name("temperature_from"):
            temperature_range = True
            temp_from = child.text
        if child.tag == _build_tag_name("temperature_to"):
            temperature_range = True
            temp_to = child.text
        if child.tag == _build_tag_name("weather_type"):
            weather_type = child.text
        if child.tag == _build_tag_name("weather_condition"):
            if 'code' in child.attrib:
                weather_condition = child.attrib['code']
                if weather_condition == "overcast":
                    emoji = overcast_emoji
                elif weather_condition == "cloudy-and-rain":
                    emoji = cloudy_emoji + rain_emoji
                elif weather_condition == "overcast-and-light-rain":
                    emoji = overcast_emoji + drops_emoji
                elif weather_condition == "cloudy":
                    emoji = cloudy_emoji
                elif weather_condition == "clear":
                    emoji = clear_emoji
                elif weather_condition == "cloudy-and-light-rain":
                    emoji = cloudy_emoji + drops_emoji

    if temperature_range:
        return u"" + temp_from + u"°C ... " + temp_to + u"°C, " + weather_type + " " + emoji
    else:
        return u"" + temp + u"°C, " + weather_type + " " + emoji



if __name__ == "__main__":
    get_forecast()
