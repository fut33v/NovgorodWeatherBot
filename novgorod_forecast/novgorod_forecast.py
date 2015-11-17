# coding=utf-8
import json
import xml.etree.ElementTree as ET

from util import bot_util

__author__ = 'fut33v'


OVERCAST_EMOJI = u"\u2601\ufe0f"
RAIN_EMOJI = u"\u2614\ufe0f"
DROPS_EMOJI = u"\U0001f4a6"
SNOW_EMOJI = u"\u2744\ufe0f"
CLOUDY_EMOJI = u"\u26c5\ufe0f"
CLEAR_EMOJI = u"\u2600\ufe0f"
MOON_PART_EMOJI = u"\U0001f319"


# noinspection PyClassHasNoInit
class YandexForecaster:
    _URL_FORECAST_YANDEX = "https://export.yandex.ru/weather-ng/forecasts/26179.xml"
    # id=26179 region=10904

    @staticmethod
    def get_forecast():
        p = bot_util.urlopen(YandexForecaster._URL_FORECAST_YANDEX)
        if not p:
            return False

        root = ET.fromstring(p)
        if root is None:
            return False

        NUMBER_OF_DAYS = 2
        days_list = []
        i = 0
        for child in root:
            if child.tag == YandexForecaster._build_tag_name("day"):
                days_list.append(child)
                i += 1
            if i == NUMBER_OF_DAYS:
                break

        if len(days_list) != 2:
            return False

        today = days_list[0]
        tomorrow = days_list[1]
        today_forecast = YandexForecaster._get_day_forecast_string(today)
        tomorrow_forecast = YandexForecaster._get_day_forecast_string(tomorrow)
        if not today_forecast or not tomorrow_forecast:
            return False

        forecast = u"*Сегодня:*\n" + today_forecast + u"\n*Завтра*:\n" + tomorrow_forecast

        return forecast

    @staticmethod
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
        morning_forecast = YandexForecaster._get_day_part_forecast_string(morning_forecast)
        forecast += u"Утро: " + morning_forecast + u"\n"
        day_forecast = YandexForecaster._get_day_part_forecast_string(day_forecast)
        forecast += u"День: " + day_forecast + u"\n"
        evening_forecast = YandexForecaster._get_day_part_forecast_string(evening_forecast)
        forecast += u"Вечер: " + evening_forecast + u"\n"
        night_forecast = YandexForecaster._get_day_part_forecast_string(night_forecast)
        forecast += u"Ночь: " + night_forecast + u"\n"
        return forecast

    @staticmethod
    def _build_tag_name(tag_name):
        return "{http://weather.yandex.ru/forecast}" + tag_name

    @staticmethod
    def _get_day_part_forecast_string(day_part):
        if not isinstance(day_part, ET.Element):
            return False
        temperature_range = False
        temp_from = u"??"
        temp_to = u"??"
        weather_type = u"??"
        temp = u"??"
        emoji = u""
        for child in day_part:
            if child.tag == YandexForecaster._build_tag_name("temperature"):
                temperature_range = False
                temp = child.text
            if child.tag == YandexForecaster._build_tag_name("temperature_from"):
                temperature_range = True
                temp_from = child.text
            if child.tag == YandexForecaster._build_tag_name("temperature_to"):
                temperature_range = True
                temp_to = child.text
            if child.tag == YandexForecaster._build_tag_name("weather_type"):
                weather_type = child.text
            if child.tag == YandexForecaster._build_tag_name("weather_condition"):
                if 'code' in child.attrib:
                    weather_condition = child.attrib['code']
                    if weather_condition == "overcast":
                        emoji = OVERCAST_EMOJI
                    elif weather_condition == "cloudy-and-rain":
                        emoji = CLOUDY_EMOJI + RAIN_EMOJI
                    elif weather_condition == "overcast-and-light-rain":
                        emoji = OVERCAST_EMOJI + DROPS_EMOJI
                    elif weather_condition == "cloudy":
                        emoji = CLOUDY_EMOJI
                    elif weather_condition == "overcast-and-rain":
                        emoji = CLOUDY_EMOJI + RAIN_EMOJI
                    elif weather_condition == "clear":
                        type = day_part.attrib['type']
                        if type == "night":
                            emoji = MOON_PART_EMOJI
                        else:
                            emoji = CLEAR_EMOJI
                    elif weather_condition == "cloudy-and-light-rain":
                        emoji = CLOUDY_EMOJI + DROPS_EMOJI

        if temperature_range:
            return u"" + temp_from + u"°C ... " + temp_to + u"°C, " + weather_type + " " + emoji
        else:
            return u"" + temp + u"°C, " + weather_type + " " + emoji


class WeatherComForecaster:
    _URL_FORECAST_WEATHER_COM_FIRST_PART = "http://api.wunderground.com/api/"
    _URL_FORECAST_WEATHER_COM_SECOND_PART = "/geolookup/conditions/forecast/q/Russia/Velikiy_Novgorod.json"

    def __init__(self, token):
        self._token = token
        self._url_get_forecast = (
            self._URL_FORECAST_WEATHER_COM_FIRST_PART + token + self._URL_FORECAST_WEATHER_COM_SECOND_PART
        )

    def get_forecast(self):
        forecast = bot_util.urlopen(self._url_get_forecast)
        if forecast:
            forecast = json.loads(forecast)
            if 'forecast' in forecast:
                forecast = forecast['forecast']
                if 'simpleforecast' in forecast:
                    simple_forecast = forecast['simpleforecast']
                    if 'forecastday' in simple_forecast:
                        forecastday = simple_forecast['forecastday']
                        if len(forecastday) >= 4:
                            forecast = u""

                            forecast_today = forecastday[0]
                            forecast_today = self._get_day_forecast(forecast_today)
                            forecast += u"*Today:*\n" + forecast_today

                            forecast_tomorrow = forecastday[1]
                            forecast_tomorrow = self._get_day_forecast(forecast_tomorrow)
                            forecast += u"\n*Tomorrow:*\n" + forecast_tomorrow

                            return forecast
        return False

    @staticmethod
    def _get_day_forecast(forecastday):
        if not isinstance(forecastday, dict):
            return False
        high = forecastday['high']['celsius']
        low = forecastday['low']['celsius']
        conditions = forecastday['conditions']
        icon = forecastday['icon']
        avewind = forecastday['avewind']
        wind_speed = unicode(avewind['kph'])
        wind_direction = avewind['dir']
        emoji = u""
        print icon
        if icon == 'chancerain':
            emoji = DROPS_EMOJI
        if icon == 'cloudy':
            emoji = OVERCAST_EMOJI
        return (
            low + u"°C ... " +
            high + u"°C, " +
            conditions + u" " + emoji +
            u", Wind: " + wind_direction + u" " + wind_speed + u" kp/h\n"
        )


if __name__ == "__main__":
    f = YandexForecaster.get_forecast()
    t = bot_util.read_one_string_file("../data/weather_com_token")
    f = WeatherComForecaster(t)
    f = f.get_forecast()
    if f:
        print "OK"
