__author__ = 'fut33v'

import time
import json

import bot_novgorod_weather
import bot_util


BOT_TOKEN = bot_novgorod_weather.BOT_TOKEN
URL_BOT_COMMON = "https://api.telegram.org/bot%s/" % BOT_TOKEN
URL_GET_UPDATES = URL_BOT_COMMON + "getUpdates"


if __name__ == "__main__":
    last = 0
    previous_update_date = bot_util.read_previous_update_date()

    while True:
        r = bot_util.urlopen(URL_GET_UPDATES + "?offset=%s" % (last + 1))
        r = json.loads(r)
        print r["result"]
        for message in r["result"]:
            print message
            if previous_update_date >= int(message["message"]["date"]):
                continue
            last = int(message["update_id"])
            data = json.dumps(message)
            bot_novgorod_weather.process_update(message)
            previous_update_date = int(message["message"]["date"])
            bot_util.write_previous_update_date(previous_update_date)

        time.sleep(3)
