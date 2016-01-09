regexp_for_check="[n]ovgorod_weather_bot.py"
check_bot=`ps aux | grep "[n]ovgorod_weather_bot.py" | wc -l`
# echo kek: $check_bot
if [ $check_bot -gt 1 ] 
    then
        echo Found $check_bot process\[es\] with regexp: \"$regexp_for_check\"
    exit 0
fi

screen -d -m python novgorod_weather_bot.py
