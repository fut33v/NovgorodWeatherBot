# coding=utf-8
from util import bot_util
#from novgorod_forecast import novgorod_forecast
from novgorod_forecast.novgorod_forecast import YandexForecaster
from novgorod_forecast.novgorod_forecast import WeatherComForecaster
from novgorod_weather import novgorod_weather
from telegram_bot.telegram_bot import TelegramBot

__author__ = 'fut33v'

TOKEN_FILENAME = "data/token"
BOTAN_TOKEN_FILENAME = "data/botan_token"
WEATHER_COM_TOKEN_FILENAME = "data/weather_com_token"

class NovgorodWeatherBot(TelegramBot):
    COMMAND_GET_WEATHER = "/getweather"
    COMMAND_GET_TEMPERATURE = "/gettemperature"
    COMMAND_GET_HUMIDITY = "/gethumidity"
    COMMAND_GET_PRESSURE = "/getpressure"
    COMMAND_GET_WIND = "/getwind"

    COMMAND_ADD_TIMER = "/addtimer"

    COMMAND_GET_FORECAST = "/getforecast"
    COMMAND_GET_FORECAST_WEATHER_COM = "/getforecastweathercom"

    def __init__(self, token, name, weather_com_token=None, botan_token=None):
        TelegramBot.__init__(self, token, name, botan_token)

        self.add_command_with_parameter(self.COMMAND_ADD_TIMER)

        self.add_command_no_parameter(self.COMMAND_GET_WEATHER)
        self.add_command_no_parameter(self.COMMAND_GET_TEMPERATURE)
        self.add_command_no_parameter(self.COMMAND_GET_HUMIDITY)
        self.add_command_no_parameter(self.COMMAND_GET_PRESSURE)
        self.add_command_no_parameter(self.COMMAND_GET_WIND)

        self.add_command_no_parameter(self.COMMAND_GET_FORECAST)
        self.add_command_no_parameter(self.COMMAND_GET_FORECAST_WEATHER_COM)

        if weather_com_token is not None:
            self._weather_com_forecaster = WeatherComForecaster(weather_com_token)
        else:
            self._weather_com_forecaster = None

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
            f = YandexForecaster.get_forecast()
            if f:
                return f
            else:
                return u"Проблемы при получении прогноза погоды"
        if self._check_message_for_command(text, self.COMMAND_GET_FORECAST_WEATHER_COM):
            if self._weather_com_forecaster is not None:
                f = self._weather_com_forecaster.get_forecast()
                if f:
                    return f
                else:
                    return u"Проблемы при получении прогноза погоды"
        return False

    def _get_start_message(self):
        return """
        Погода в великом Новгороде
        Команды:
        /start, /help
        /getweather — Погода
        /getforecast — Прогноз

        Погода — [Новгород.ру](http://novgorod.ru/weather)
        Прогноз — Яндекс.Погода, Weather.com
        [Логотип бота](vk.com/mzzaxixart)
        [Автор бота](ilya.fut33v.ru/contacts), Telegram: @fut33v

        [Оценить в Store Bot](https://telegram.me/storebot?start=novgorodweatherbot)
        [Github](https://github.com/fut33v/NovgorodWeatherBot)
        """


if __name__ == "__main__":
    t = bot_util.read_one_string_file(TOKEN_FILENAME)
    botan_t = bot_util.read_one_string_file(BOTAN_TOKEN_FILENAME)
    weather_com_t = bot_util.read_one_string_file(WEATHER_COM_TOKEN_FILENAME)
    bot = NovgorodWeatherBot(t, name="NovgorodWeatherBot", botan_token=botan_t, weather_com_token=weather_com_t)
    bot.start_poll()
