#/!bin/bash

sudo docker run -d --restart unless-stopped --env-file .env --name novgorod_weather_bot novgorod_weather_bot
