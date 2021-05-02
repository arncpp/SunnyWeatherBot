from Globals import Globals, bot
from telebot import types


def buttons_in_default_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_weather_now = types.KeyboardButton(text=Globals.btn_weather_text)
    btn_mailing = types.KeyboardButton(text=Globals.btn_mailing_text)
    btn_news = types.KeyboardButton(text=Globals.btn_news_text)
    keyboard.add(button_weather_now, btn_mailing, btn_news)
    return keyboard


def button_in_mailing():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_sub = types.KeyboardButton(text="Подписаться на рассылку")
    btn_unsub = types.KeyboardButton(text="Отписаться от рассылки")
    btn_back = types.KeyboardButton(text="Назад")
    keyboard.add(btn_sub, btn_unsub, btn_back)
    return keyboard


def buttons_in_choose_option():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    option_now = types.KeyboardButton(text="Сейчас")
    option_5_days = types.KeyboardButton(text="На 5 дней")
    keyboard.add(option_now, option_5_days)
    return keyboard


def buttons_in_weather():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    cont_weather = types.KeyboardButton(text="Продолжить узнавать погоду")
    stop_weather = types.KeyboardButton(text="Меню")
    keyboard.add(cont_weather, stop_weather)
    return keyboard


def print_weather(city, city_temperature, city_temp_feels, city_pressure,
                  city_humidity, city_wind, city_descr):
    return (f" {city}:\nтемпература {city_temperature} ℃\n"
            f"ощущается как {city_temp_feels} ℃\n"
            f"давление {city_pressure} кПа"
            f"\nвлажность {city_humidity} %\n"
            f"скорость ветра {city_wind} м/c\n"
            f"{city_descr}")
