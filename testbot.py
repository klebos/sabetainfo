import datetime

import requests
from destup import tokenkey as tok
import telebot
from yandexWeatherKey import openweatherkey as key
import json




def telega (token, weather,ostatok):
    bot = telebot.TeleBot(token)

    nowtime = 'Время'

    @bot.message_handler(commands=["start"])
    def hello (message):
        bot.send_message(message.chat.id, weather + ostatok)
    bot.polling()


def pogoda (api):
    res = requests.get(f'http://api.openweathermap.org/data/2.5/weather?appid={api}&q=Delhi')
    res2 = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat=71.2717700&lon=72.0742600&appid={api}")
    data = json.loads ( res2.text )
    weather = data['weather']

    temp = data['main']
    facttemp = float(temp['temp'])-273.15
    feeltemp = float(temp['feels_like'])-273.15
    wind = data['wind']['speed']
    def what (whatnowweather):
        if whatnowweather == 'broken clouds':
            weather = 'рассеянная облачность'
        elif whatnowweather == 'snow':
            weather = 'снег идёт'
        elif whatnowweather == 'clear sky':
            weather = 'чистое небо'
        elif whatnowweather == 'few clouds':
            weather = 'небольшая облачность'
        elif whatnowweather == 'scattered clouds':
            weather =  'облачка'
        elif whatnowweather == 'shower rain':
            weather = 'проливной дождь'
        elif whatnowweather == 'rain':
            weather = 'дождь'
        elif whatnowweather == 'thunderstorm':
            weather = 'ураган'
        elif whatnowweather == 'mist':
            weather = 'туман'

        return weather

    def winddetector(direct):
        if direct > 350 and direct < 10:
            text = 'С'
        elif direct > 10 and direct < 30:
            text = 'ССВ'
        elif direct >30 and direct < 50:
            text = 'СВ'
        elif direct >50 and direct < 75:
            text = 'ВСВ'
        elif direct > 75 and direct < 100:
            text = 'В'
        elif direct > 100 and direct < 120:
            text = 'ВЮВ'
        elif direct > 120 and direct < 145:
            text = 'ЮВ'
        elif direct > 145 and direct < 165:
            text = 'ЮЮВ'
        elif direct > 165 and direct < 190:
            text = 'Ю'
        elif direct > 190 and direct < 210:
            text = 'ЮЮЗ'
        elif direct > 210 and direct < 235:
            text = 'ЮЗ'
        elif direct > 235 and direct < 260:
            text = 'ЗЮЗ'
        elif direct > 260 and direct < 280:
            text = 'З'
        elif direct > 280 and direct < 305:
            text = 'ЗСЗ'
        elif direct > 305 and direct < 330:
            text = 'СЗ'
        elif direct > 330 and direct < 350:
            text = 'ССЗ'

        return text
    whatnow = what((weather [ 0 ] [ 'description' ]))
    winddirect = winddetector(int(data['wind']['deg']))



    result = f'Марина! Сейчас на терминале Утренний {whatnow}, температура {round(facttemp,1)} град. , а ощущается как {round(feeltemp,1)} град. Ветер {int(wind)} м/c, направление {winddirect}. '
    if result == None:
        result = 'У бота нихуя нет интернета'
    return result

def ostatok ():
    nowtime = datetime.datetime.now()
    endtime = datetime.datetime(2021,10,20)
    delta = str (endtime - nowtime)
    days = delta.split(',')[0].split()[0]+' дн.'
    message = f'До официального запрета навигации на территории терминала - {days}'
    return message



ostatok = ostatok()
weather = pogoda(key)
telega(tok,weather,ostatok)

