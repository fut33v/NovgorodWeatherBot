#!/bin/sh

sudo cp NovgorodWeatherBot /etc/init.d
sudo chmod +x /etc/init.d/NovgorodWeatherBot
sudo update-rc.d NovgorodWeatherBot defaults
