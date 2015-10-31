# coding=utf-8
import bot_util
import novgorod_forecast
import novgorod_weather
from telegram_bot import TelegramBot

__author__ = 'fut33v'


class NovgorodWeatherBot(TelegramBot):
    COMMAND_GET_WEATHER = "/getweather"
    COMMAND_GET_TEMPERATURE = "/gettemperature"
    COMMAND_GET_HUMIDITY = "/gethumidity"
    COMMAND_GET_PRESSURE = "/getpressure"
    COMMAND_GET_WIND = "/getwind"

    COMMAND_ADD_TIMER = "/addtimer"

    COMMAND_GET_FORECAST = "/getforecast"

    def __init__(self, token, name, botan_token=None):
        TelegramBot.__init__(self, token, name, botan_token)

        self.add_command_with_parameter(self.COMMAND_ADD_TIMER)

        self.add_command_no_parameter(self.COMMAND_GET_WEATHER)
        self.add_command_no_parameter(self.COMMAND_GET_TEMPERATURE)
        self.add_command_no_parameter(self.COMMAND_GET_HUMIDITY)
        self.add_command_no_parameter(self.COMMAND_GET_PRESSURE)
        self.add_command_no_parameter(self.COMMAND_GET_WIND)

        self.add_command_no_parameter(self.COMMAND_GET_FORECAST)

    def _process_message(self, chat_id, text):
        if text in self._commands_no_parameter:
            response = self.process_command_no_parameters(text)
            if response:
                success = self._send_response(chat_id, response=response, markdown=True)
                return success
            return False
        else:
            pass

    def process_command_no_parameters(self, text):
        if self._check_message_for_command(text, self._COMMAND_START):
            return self._get_start_message()
        if self._check_message_for_command(text, self.COMMAND_GET_HUMIDITY):
            h = novgorod_weather.get_humidity()
            if h:
                return novgorod_weather.build_humidity_string(h)
        if self._check_message_for_command(text, self.COMMAND_GET_PRESSURE):
            p = novgorod_weather.get_pressure()
            if p:
                return novgorod_weather.build_pressure_string(p)
        if self._check_message_for_command(text, self.COMMAND_GET_WIND):
            w = novgorod_weather.get_wind()
            if w:
                return novgorod_weather.build_wind_string(w)
        if self._check_message_for_command(text, self.COMMAND_GET_TEMPERATURE):
            temperature = novgorod_weather.get_temperature()
            if temperature:
                return novgorod_weather.build_temperature_string(temperature)
        if self._check_message_for_command(text, self.COMMAND_GET_WEATHER):
            w = novgorod_weather.get_weather()
            if w:
                return w
        if self._check_message_for_command(text, self.COMMAND_GET_FORECAST):
            f = novgorod_forecast.get_forecast()
            if f:
                return f
            else:
                return u"Проблемы при получении прогноза погоды"
        return False

    def _get_start_message(self):
        return """
        Погода в великом Новгороде,
        Получена с сайта novgorod.ru
        http://novgorod.ru/weather
        Логотип бота: https://vk.com/mzzaxixart

        Команды:
        /start — Информация о боте
        /getweather — Погода в Великом Новгороде
        /gettemperature — Температура
        /gethumidity - Влажность
        /getpressure - Давление
        /getwind - Ветер

        """


if __name__ == "__main__":
    t = bot_util.read_one_string_file("token")
    botan_t = bot_util.read_one_string_file("botan_token")
    bot = NovgorodWeatherBot(t, name="NovgorodWeatherBot", botan_token=botan_t)
    bot.start_poll()
