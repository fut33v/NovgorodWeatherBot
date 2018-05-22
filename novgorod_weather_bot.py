# coding=utf-8
from util import bot_util
from novgorod_weather import novgorod_weather
from telegram_bot.telegram_bot import TelegramBot

__author__ = 'fut33v'

TOKEN_FILENAME = "data/token"
BOTAN_TOKEN_FILENAME = "data/botan_token"
WEATHER_COM_TOKEN_FILENAME = "data/weather_com_token"


class NovgorodWeatherBot(TelegramBot):
    COMMAND_GET_WEATHER = "/getweather"
    COMMAND_GET_TEMPERATURE = "/gettemperature"
    COMMAND_GET_RAIN = "/getrain"
    COMMAND_GET_PRESSURE = "/getpressure"
    COMMAND_GET_WIND = "/getwind"

    def __init__(self, token, name):
        TelegramBot.__init__(self, token, name)

        self.add_command_no_parameter(self.COMMAND_GET_WEATHER)
        self.add_command_no_parameter(self.COMMAND_GET_TEMPERATURE)
        self.add_command_no_parameter(self.COMMAND_GET_RAIN)
        self.add_command_no_parameter(self.COMMAND_GET_PRESSURE)
        self.add_command_no_parameter(self.COMMAND_GET_WIND)

    def _process_message(self, chat_id, text):
        if text in self._commands_no_parameter:
            response = self.process_command_no_parameters(text)
            if response:
                success = self.send_response(chat_id, response=response, markdown=True)
                return success
            return False
        else:
            pass

    def process_command_no_parameters(self, text):
        if self._check_message_for_command(text, self._COMMAND_START) or \
                self._check_message_for_command(text, self._COMMAND_HELP):
            return self._get_start_message()
        if self._check_message_for_command(text, self.COMMAND_GET_PRESSURE):
            p = novgorod_weather.get_pressure()
            if p:
                return novgorod_weather.build_pressure_string(p)
        if self._check_message_for_command(text, self.COMMAND_GET_RAIN):
            w = novgorod_weather.get_rain()
            if w:
                return novgorod_weather.build_rain_string(w)
        if self._check_message_for_command(text, self.COMMAND_GET_TEMPERATURE):
            temperature = novgorod_weather.get_temperature()
            if temperature:
                return novgorod_weather.build_temperature_string(temperature)
        if self._check_message_for_command(text, self.COMMAND_GET_WEATHER):
            w = novgorod_weather.get_weather()
            if w:
                return w
        return False

    def _get_start_message(self):
        return """
        Погода в великом Новгороде
        Команды:
        /start, /help
        /getweather — Погода

        Погода — [Новгород.ру](http://novgorod.ru/weather)
        [Логотип бота](vk.com/mzzaxixart)
        [Автор бота] @fut33v

        [Оценить в Store Bot](https://telegram.me/storebot?start=novgorodweatherbot)
        [Github](https://github.com/fut33v/NovgorodWeatherBot)
        """


if __name__ == "__main__":
    t = bot_util.read_one_string_file(TOKEN_FILENAME)
    bot = NovgorodWeatherBot(t, name="NovgorodWeatherBot")
    bot.start_poll()
