DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
regexp_for_check="[n]ovgorod_weather_bot.py"
check_bot=`ps aux | grep $regexp_for_check | wc -l`
if [ $check_bot -gt 1 ] 
    then
        echo Found $check_bot process\[es\] with regexp: \"$regexp_for_check\"
    exit 0
fi
echo Not found bot process with regexp $regexp_for_check
screen -d -m python $DIR/../novgorod_weather_bot.py
