import requests

from MainFile.config import tg_bot_token, open_weather_token
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from telebot import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import math
import datetime


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)
# Клавиатура

geo = KeyboardButton(text="Определить по геопозиции", request_location=True)
Markup = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(geo)




@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет напиши город!", reply_markup=Markup)







@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await message.answer("👋Привет!,\n 🤖Я бот🤖. Я могу определить погоду в твоем городе😦, "
                         "для этого тебе надо просто ввести название города, дальше я все сделаю сам🤔")


# смайлики
@dp.message_handler(content_types=['location', 'text'])
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно ☀",
        "Clouds": "Облачно ☁",
        "Rain": "Дождь 🌧",
        "Thunderstorm": "Гроза 🌩⛈",
        "Snow": "Снег ☃",
        "Mist": "Туман 🌫"
    }

    try:



        if not message.location == None:
            r = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?lat={message.location.latitude}&lon={message.location.longitude}&appid={open_weather_token}&units=metric"
            )
            data = r.json()
            city = data["name"]
        else:
            r = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
            )
            data = r.json()
            city = data["name"]

        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        weather_discription = data["weather"][0]["main"]
        if weather_discription in code_to_smile:
            wd = code_to_smile[weather_discription]
        else:
            wd = "🧐посмотри в окно🤳🏻"
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        lenght_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        wheather = math.floor(cur_weather)

        await message.answer(f"***{datetime.datetime.now().strftime(' %Y-%m-%d || %H:%M ')}***\n"
                             f"Погода в городе: {city}\nТемпература: {wheather}°,  {wd} \n"
                             f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.cт\nВетер: {wind} м/c\n"
                             f"Восход солнца🌞: {sunrise_timestamp}\nЗаход солнца: {sunset_timestamp}\n"
                             f"Продолжительность дня🌎:  {lenght_of_the_day}\n "
                             f"🤜🏼🤜🏼🤜🏼Хорошего дня!🤛🏼🤛🏼🤛🏼")
    except:
        return()


if __name__ == '__main__':
    executor.start_polling(dp)
