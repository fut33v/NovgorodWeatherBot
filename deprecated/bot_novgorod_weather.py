# coding=utf-8

import re
import urllib

from util import bot_util, botan
from util.bot_util import urlopen

__author__ = 'fut33v'


TIMERS_DIR = "timers/"
bot_util.create_dir_if_not_exists(TIMERS_DIR)



URL_WEATHER = "http://novgorod.ru/weather"

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


def build_humidity_string(humidity):
    return "*Влажность:* " + humidity + "\n"


def build_pressure_string(pressure):
    return "*Давление:* %s мм. рт. ст.\n" % pressure


def build_wind_string(wind):
    return "*Ветер:* %s " % wind


def get_weather():
    page = urlopen(URL_WEATHER)
    temperature_center = get_temperature_center(page)
    humidity = get_humidity(page)
    pressure = get_pressure(page)
    wind = get_wind(page)
    weather = build_temperature_string(temperature_center)
    if humidity is not None:
        weather += build_humidity_string(humidity)
    if pressure is not None:
        weather += build_pressure_string(pressure)
    if wind is not None:
        weather += build_wind_string(wind)
    return weather


def send_response(chat_id, response, markdown=False):
    if response is None or chat_id is None or response == '':
        return False
    print 'chat_id:', chat_id
    print 'response', response
    d = {
        'chat_id': chat_id,
        'text': response,
    }
    if markdown is True:
        d['parse_mode'] = "Markdown"
    d = urllib.urlencode(d)
    return urlopen(URL_SEND_MESSAGE, data=d)


def get_start():
    start = """
    Погода в великом Новгороде,
    Получена с сайта novgorod.ru
    http://novgorod.ru/weather
    Логотип бота: https://vk.com/mzzaxixart

    Команды:
    /start — Информация о боте

    /getweather — Текущая погода в Великом Новгороде
    /gettemperature — Температура
    /gethumidity - Влажность
    /getpressure - Давление
    /getwind - Ветер

    """
    return start


timer_regexp = re.compile('/addtimer (.*)', re.DOTALL)
timer_regexp_group = re.compile("addtimer@NovgorodWeatherBot (.*?)", re.DOTALL)

def add_timer(message):
    message_text = message['text']
    chat_id = message['chat']['id']
    timer_filename = TIMERS_DIR + str(chat_id)
    # if os.path.exists(timer_filename) and os.path.isfile(timer_filename):
    #     data = bot_util.load_json_file(timer_filename)
    #     if 'timers' in data:
    #         timers = data['timers']
    #         timers.append(message_text)
    #         ret = ""
    #         for t in timers:
    #             ret += " " + t
    #         data = {'timers': timers}
    #         bot_util.save_json_file(timer_filename, data)
    #         return ret
    #else:
    time = ""
    m = timer_regexp.search(message_text)
    if m is not None:
        time = m.group(1)
    m = timer_regexp_group.search(message_text)
    if m is not None:
        time = m.group(1)

    m = re.search("([0-9]{2}):([0-9]{2})", time)
    if m is not None:
        print m.group(1)
        print m.group(2)

    timers = [time]
    data = {'timers': timers}
    bot_util.save_json_file(timer_filename, data)
    return "New timer added!"
    # return timers[0] + str(chat_id)


def add_timer_help():
    return """
    Введите время в формате
    17:30
    17-30
    для того, чтобы я отсылал Вам погоду по таймеру
    """
    pass


def process_command(command):
    """ Process bot command (starts with / e.g. /start) """
    if not isinstance(command, basestring):
        return None
    response = None
    if command == START or START_GROUP:
        response = get_start()
    if command == GET_WEATHER or command == GET_WEATHER_GROUP:
        response = get_weather()
    if command == GET_TEMPERATURE or command == GET_TEMPERATURE_GROUP:
        response = build_temperature_string(get_temperature_center(urlopen(URL_WEATHER)))
    if command == GET_HUMIDITY or command == GET_HUMIDITY_GROUP:
        response = build_humidity_string(get_humidity(urlopen(URL_WEATHER)))
    if command == GET_PRESSURE or command == GET_PRESSURE_GROUP:
        response = build_pressure_string(get_pressure(urlopen(URL_WEATHER)))
    if command == GET_WIND or command == GET_WIND_GROUP:
        response = build_wind_string(get_wind(urlopen(URL_WEATHER)))
    if command == ADD_TIMER or command == ADD_TIMER_GROUP:
        response = add_timer_help()
    return response


def check_parameter_command(message_text):
    m = re.match(ADD_TIMER, message_text)
    if m is not None:
        return True
    m = re.match(ADD_TIMER_GROUP, message_text)
    if m is not None:
        return True
    return False


def process_update(update):
    """
    :param update: update message from Telegram Bot API
    :return:
    """
    if update is None:
        return None
    if not isinstance(update, dict):
        return None
    if "message" in update:
        user_id = 0
        if 'from' in update['message']:
            if 'id' in update['message']['from']:
                user_id = update['message']['from']['id']
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
                s = send_response(chat_id, response, markdown=True)
                if s is True and None != BOTAN_TOKEN:
                    botan.track(BOTAN_TOKEN, user_id, message, message_text)
                # send shit to user
                print message_text
        elif check_parameter_command(message_text):
            response = add_timer(message)
            send_response(chat_id, response)



if __name__ == "__main__":
    # w = get_weather()
    # print w
    r = re.compile('/addtimer (.*)', re.DOTALL)
    m1 = r.search(u"/addtimer asf")
    if m1 is not None:
        print 0, m1.group(0), 0
        print 1, m1.group(1), 1
