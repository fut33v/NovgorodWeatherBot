# coding=utf-8

import httplib
import re
import urllib2
import urllib
import bot_util

__author__ = 'fut33v'


BOT_TOKEN = bot_util.read_token()
URL = "https://api.telegram.org/bot%s/" % BOT_TOKEN
URL_SEND_MESSAGE = URL + "sendMessage"


# Commands
START = "/start"
GET_WEATHER = "/getweather"
GET_WEATHER_GROUP = "/getweather@NovgorodWeatherBot"
GET_TEMPERATURE = "/gettemperature"
GET_TEMPERATURE_GROUP = "/gettemperature@NovgorodWeatherBot"

BOT_COMMANDS = [START, GET_WEATHER, GET_WEATHER_GROUP, GET_TEMPERATURE, GET_TEMPERATURE_GROUP]

def urlopen(url, data=None):
    try:
        if data is not None:
            urllib2.urlopen(url, data)
        else:
            return urllib2.urlopen(url, data).read()
    except urllib2.HTTPError, e:
        print "HTTPError", e
    except urllib2.URLError, e:
        print "URLError",  e
    except httplib.HTTPException, e:
        print "HTTPException", e
    return None

# URLS
URL_WEATHER = "http://novgorod.ru/weather"
# Patterns
REGEX_TEMPERATURE_CENTER_ROW = "<tr><td>Центр.*?</td></tr>"
REGEX_TEMPERATURE_WHITE_TOWN_ROW = "<tr><td>&laquo;Белый город&raquo;.*?</td></tr>"
REGEX_COMMON_FOR_TEMPERATURE_FROM_ROW = "<td style.*?>(.*?)</td>"

regexp_colortable = re.compile("<table class=\"colortable\".*?/table>", re.DOTALL)
regexp_temperature_center = re.compile("<tr><td>Центр</td><td.*?>(.*?)</td></tr>", re.DOTALL)
regexp_humidity = re.compile("<td>Влажность</td><td.*?>(.*)</td>")
regexp_pressure = re.compile("<td>Давление</td><td>.*?>(.*?)</span>")
regexp_wind = re.compile("<td>Направление</td><td><img.*?>(.*?)</td>")
regexp_wind_speed = re.compile("<td>Скорость</td><td>(.*?)<span.*?>(.*?)</span></td>")


def get_first_table(weather_page):
    first_table = regexp_colortable.findall(weather_page)[0]
    return first_table


def get_temperature_center(weather_page):
    temperature_center_row = re.findall(REGEX_TEMPERATURE_CENTER_ROW, weather_page, re.DOTALL)[0]
    m = re.search(REGEX_COMMON_FOR_TEMPERATURE_FROM_ROW, temperature_center_row)
    if m is not None:
        temperature_center_string = m.group(1)
        tmp = temperature_center_string.split(' ')
        if len(tmp) > 1:
            temperature_center = tmp[0]
            return temperature_center
    return None


def get_humidity(weather_page):
    t = get_first_table(weather_page)
    m = regexp_humidity.search(t)
    if m is not None:
        humidity = m.group(1)
        return humidity


def get_pressure(weather_page):
    # t = get_first_table(weather_page)
    m = regexp_pressure.search(weather_page)
    if m is not None:
        pressure = m.group(1)
        return pressure


def get_wind(weather_page):
    t = get_first_table(weather_page)
    m = regexp_wind.search(t)
    if m is not None:
        wind = m.group(1)
        m = regexp_wind_speed.search(t)
        if m is not None:
            wind += " " + m.group(1)
            wind += " " + m.group(2)
        return wind


def build_temperature_string(temperature):
    return "*Температура:* %s°C\n" % temperature


def get_weather():
    page = urlopen(URL_WEATHER)
    temperature_center = get_temperature_center(page)
    humidity = get_humidity(page)
    pressure = get_pressure(page)
    wind = get_wind(page)
    weather = build_temperature_string(temperature_center)
    if humidity is not None:
        weather += ("*Влажность:* " + humidity + "\n")
    if pressure is not None:
        weather += ("*Давление:* %s мм. рт. ст.\n" % pressure)
    if wind is not None:
        weather += ("*Ветер:* %s " % wind)
    return weather


def send_response(chat_id, response, markdown=False):
    if response is None or chat_id is None:
        return None
    print 'chat_id:', chat_id
    print 'response', response
    d = {
        'chat_id': chat_id,
        'text': response,
    }
    if markdown is True:
        d['parse_mode'] = "Markdown"
    d = urllib.urlencode(d)
    urlopen(URL_SEND_MESSAGE, data=d)


def get_start():
    start = """
    Погода в великом Новгороде,
    Получена с сайта novgorod.ru
    http://novgorod.ru/weather
    Логотип бота: https://vk.com/mzzaxixart

    Команды:
    /start
    /getweather — Текущая погода в Великом Новгороде
    /gettemperature — Температура в Великом Новгороде
    """
    return start


def process_command(command):
    """ Process bot command (starts with / e.g. /start) """
    if not isinstance(command, basestring):
        return None
    response = None
    if command == START:
        response = get_start()
    if command == GET_WEATHER or command == GET_WEATHER_GROUP:
        response = get_weather()
    if command == GET_TEMPERATURE or command == GET_TEMPERATURE_GROUP:
        response = build_temperature_string(get_temperature_center(urlopen(URL_WEATHER)))
    return response


def process_update(update):
    if update is None:
        return None
    if not isinstance(update, dict):
        return None
    if "message" in update:
        message = update['message']
        if 'chat' not in message or 'text' not in message:
            return None
        chat = message['chat']
        if 'id' not in chat:
            return None
        chat_id = chat['id']
        message_text = message['text']
        if message_text in BOT_COMMANDS:
            response = process_command(message_text)
            if response is not None:
                send_response(chat_id, response, markdown=True)
                # send shit to user
                print message_text


if __name__ == "__main__":
    w = get_weather()
    print w
