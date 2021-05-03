from telebot import types

from Globals import Globals


def buttons_in_default_menu():
    """
    Функция для отрисовки кнопок в меню
    :return: keyboard
    """
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_weather_now = types.KeyboardButton(text=Globals.btn_weather_text)
    btn_mailing = types.KeyboardButton(text=Globals.btn_mailing_text)
    btn_news = types.KeyboardButton(text=Globals.btn_news_text)
    keyboard.add(button_weather_now, btn_mailing, btn_news)
    return keyboard


def button_in_mailing():
    """
    Функция для отрисовки конпок в рассылке
    :return: keyboard
    """
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_sub = types.KeyboardButton(text=Globals.btn_subscribe_text)
    btn_unsub = types.KeyboardButton(text=Globals.btn_unsubscribe_text)
    btn_back = types.KeyboardButton(text=Globals.btn_back)
    keyboard.add(btn_sub, btn_unsub, btn_back)
    return keyboard


def buttons_in_choose_option():
    """
    Функция для отрисовки кнопок в выборе погоды
    :return: keyboard
    """
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    option_now = types.KeyboardButton(text=Globals.btn_now)
    option_5_days = types.KeyboardButton(text=Globals.btn_5days)
    keyboard.add(option_now, option_5_days)
    return keyboard


def buttons_in_weather():
    """
    Функция для отрисовки кнопок после запроса о погоде
    :return: keyboard
    """
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    cont_weather = types.KeyboardButton(text=Globals.btn_continue)
    stop_weather = types.KeyboardButton(text=Globals.btn_menu)
    keyboard.add(cont_weather, stop_weather)
    return keyboard


def print_weather(city, city_temperature, city_temp_feels, city_pressure,
                  city_humidity, city_wind, city_descr):
    """

    :param city: город
    :param city_temperature: температура
    :param city_temp_feels: температура, как ощущается
    :param city_pressure: давление
    :param city_humidity: влажность
    :param city_wind: скорость ветра
    :param city_descr: описание
    :return: возвращает текст для печати
    """
    return (f" {city}:\nтемпература {city_temperature} ℃\n"
            f"ощущается как {city_temp_feels} ℃\n"
            f"давление {city_pressure} кПа"
            f"\nвлажность {city_humidity} %\n"
            f"скорость ветра {city_wind} м/c\n"
            f"{city_descr}")
