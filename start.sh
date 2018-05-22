#!/bin/sh
until python ./novgorod_weather_bot.py; do
    echo "NovgorodWeatherBot crashed with exit code $?. Respawning.." >&2
    sleep 1
done

