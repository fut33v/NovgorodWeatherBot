import json
import re
import time
import bot_util
import botan
import telegram_bot_protocol

__author__ = 'fut33v'


class TelegramBot:
    PREVIOUS_UPDATE_DATE_FILENAME = 'previous_update_date'
    _URL_COMMON_TEMPLATE = "https://api.telegram.org/bot%s/"
    _COMMAND_START = "/start"

    def __init__(self, token, name, botan_token=None):
        self._token = token
        self.name = name

        self._commands_no_parameter = []
        self.add_command_no_parameter(self._COMMAND_START)

        self._commands_with_parameter = []
        self._commands_with_parameters_regexps_dict = {}

        self._previous_update_date = self._read_previous_update_date()

        self._url_common = self._URL_COMMON_TEMPLATE % token
        self._url_get_updates = self._url_common + "getUpdates"
        self._url_send_message = self._url_common + "sendMessage"
        self._botan_token = botan_token

    def start_poll(self):
        last = 0
        while True:
            r = bot_util.urlopen(self._url_get_updates + "?offset=%s" % (last + 1))
            if r:
                r = json.loads(r)
                print r["result"]
                for update in r["result"]:
                    print update
                    if self._previous_update_date >= int(update["message"]["date"]):
                        continue
                    last = int(update["update_id"])
                    self._process_update(update)
                    previous_update_date = int(update["message"]["date"])
                    self._write_previous_update_date(previous_update_date)
            time.sleep(3)

    def _process_update(self, update):
        if update is None:
            return
        message = telegram_bot_protocol.get_message(update)
        if message:

            chat_id = telegram_bot_protocol.get_chat_id(message)
            text = telegram_bot_protocol.get_text(message)

            if chat_id and text:
                success = self._process_message(chat_id, text)
                if self._botan_token and success:
                    user_id = telegram_bot_protocol.get_user_id(message)
                    if user_id:
                        self._botan_track(user_id, message, text)

    def _process_message(self, chat_id, text):
        raise NotImplemented

    def _botan_track(self, user_id, message, text):
        botan.track(self._botan_token, user_id, message, text)

    def _send_response(self, chat_id, response, markdown=False):
        if response is None or chat_id is None or response == '':
            return False
        print 'chat_id:', chat_id
        #print 'response', response
        if isinstance(response, unicode):
            response = response.encode('utf-8')
        d = {
            'chat_id': chat_id,
            'text': response,
        }
        if markdown is True:
            d['parse_mode'] = "Markdown"
        return bot_util.urlopen(self._url_send_message, data=d)

    def _read_previous_update_date(self):
        u = bot_util.read_one_string_file(self.PREVIOUS_UPDATE_DATE_FILENAME)
        if u == '' or None == u:
            return 0
        return int(u)

    def _write_previous_update_date(self, d):
        open(self.PREVIOUS_UPDATE_DATE_FILENAME, 'w').write(str(d))

    def _get_command_name_in_group(self, command_name):
        command_name_in_group = command_name + "@" + self.name
        return command_name_in_group

    def _check_message_for_command(self, text, command_name):
        return text == command_name or text == self._get_command_name_in_group(command_name)

    def add_command_no_parameter(self, command_name):
        command_name_in_group = self._get_command_name_in_group(command_name)
        self._commands_no_parameter.append(command_name)
        self._commands_no_parameter.append(command_name_in_group)

    def add_command_with_parameter(self, command_name):
        command_name_in_group = self._get_command_name_in_group(command_name)
        self._commands_with_parameter.append(command_name)
        self._commands_with_parameter.append(command_name_in_group)
        self._commands_with_parameters_regexps_dict[command_name] = re.compile(command_name + " (.*)")
        self._commands_with_parameters_regexps_dict[command_name_in_group] = re.compile(command_name_in_group + " (.*)")

    def _get_command_parameter(self, command_name, text):
        if command_name not in self._commands_with_parameters_regexps_dict:
            print "Command with name", command_name, "not command with parameters"
            return None
        r = self._commands_with_parameters_regexps_dict[command_name]
        m = r.match(text)
        if m is None:
            return None
        if m.group(1) != '':
            return m.group(1)
        else:
            return None

    def _get_start_message(self):
        return "Default /start message"


if __name__ == "__main__":
    t = TelegramBot("", "name")
    t.add_command_with_parameter("/lox")
    ret = t._get_command_parameter("/lox", "/lox abcd")
    print ret
    ret = t._get_command_parameter("/lox@name", "/lox@name abcd")
    print ret
