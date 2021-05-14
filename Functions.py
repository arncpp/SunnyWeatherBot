from bs4 import BeautifulSoup
import requests
import schedule
from telebot import types
from time import sleep

from Globals import bot, db, Globals, news_url, news_def_url


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


def buttons_in_choose_city():
    """
    Функция для отрисовки кнопок в выборе погоды
    :return: keyboard
    """
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    msc = types.KeyboardButton(text=Globals.default_btn_1)
    minsk = types.KeyboardButton(text=Globals.default_btn_2)
    keyboard.add(msc, minsk)
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


def check_user_unsubscribe(message):
    """
    Проверяет есть ли пользователь в базе данных, если нет, то добавляет его
    Если есть, то проверяет статус подписки
    Если пользователь отписан и хочет отписаться, то выводит сообщение
    "Вы уже отписаны", если пользователь подписан и хочет подписаться, то
    выводит сообщение "Вы уже подписаны"
    :param message: сообщение от пользователя
    """
    user_id = message.chat.id
    if not db.subscriber_exists(user_id):
        db.add_subscriber(user_id, False)
        bot.send_message(user_id, Globals.subscription_is_false)
    elif db.check_status(user_id) == Globals.true_status:
        db.update_subscription(user_id, False)
        bot.send_message(user_id, Globals.subscription_is_false_now)
    elif db.check_status(user_id) == Globals.false_status:
        bot.send_message(user_id, Globals.subscription_not_activated)


def check_user_subscribe(message):
    """
    Проверяет есть ли пользователь в базе данных, если нет, то добавляет его
    Если есть, то проверяет статус подписки
    Если пользователь подписан и хочет подписаться, то
    выводит сообщение "Вы уже подписаны"
    :param message: сообщение от пользователя
    """
    user_id = message.chat.id
    if not db.subscriber_exists(user_id):
        db.add_subscriber(user_id, True)
        bot.send_message(user_id, Globals.subscription_is_true)
    elif db.check_status(user_id) == Globals.false_status:
        db.update_subscription(user_id, True)
        bot.send_message(user_id, Globals.subscription_is_true_now)
    elif db.check_status(user_id) == Globals.true_status:
        bot.send_message(user_id, Globals.subscription_activated)


def parsing_news_for_sub():
    """
    Парсит сайт с новостями для подписчиков, функция используется в рассылке
    Новости высылаются в виде ссылки
    """
    subscribers = db.get_subscriptions()
    response = requests.get(news_url, headers=Globals.header)
    soup = BeautifulSoup(response.content, Globals.html_pars)
    title = soup.findAll(Globals.last_news_class,
                         class_=Globals.last_news_item_class)
    for i in range(0, len(title[:Globals.news_crop])):
        txt = f"{str(i + 1)} ) {title[i].text}"
        bot.send_message(subscribers[1],
                         Globals.text_to_link.format(
                             title[i][Globals.link_format],
                             txt),
                         parse_mode=Globals.html_pars_mode)


def parsing_last_news(message):
    """
    Парсит сайт с новостями, высылает текстом основную информацию
    :param message: сообщение от пользователя
    :return:
    """
    response = requests.get(news_def_url, headers=Globals.header)
    soup = BeautifulSoup(response.content, Globals.html_pars)
    news_text = soup.findAll(Globals.news_class,
                             class_=Globals.news_item_class)
    for number in range(0, len(news_text[:Globals.news_text_cut])):
        txt = f"{number + 1}) {news_text[number].text}"
        bot.send_message(message.chat.id, txt)


def processing_in_menu(message, choose_option, mailing_buttons, last_news,
                       help, subscribe, unsubscribe, for_subscribers,
                       bot_does_not_understand):
    """
    Обработка сообщение в основном меню
    :param message: сообщение от пользователя
    :param choose_option: выбор опции в погоде
    :param mailing_buttons: переход в рассылку
    :param last_news: последние новости
    :param help: помощь
    :param subscribe: подписаться на рассылку
    :param unsubscribe: отписаться от рассылки
    :param for_subscribers: рассылка для подписчиков
    :param bot_does_not_understand: неправильный ввод
    """
    commands_list = {Globals.weather_slash_com: choose_option,
                     Globals.mailing_com: mailing_buttons,
                     Globals.text_news_com: last_news,
                     Globals.news_slash_com: last_news,
                     Globals.help_slash_com: help,
                     Globals.subscribe_slash_com: subscribe,
                     Globals.unsubscribe_slash_com: unsubscribe,
                     Globals.choose_option_weather_com: choose_option}
    if message.text in commands_list.keys():
        commands_list[message.text](message)
    elif message.text == Globals.last_news_com:
        for_subscribers()
    else:
        bot_does_not_understand(message)


def processing_in_mailing(message, subscribe, unsubscribe, default_menu):
    """
    Обработка сообщений в рассылке
    :param message: сообщение от пользователя
    :param subscribe: подписаться на рассылку
    :param unsubscribe: отписаться от рассылки
    :param default_menu: переход в основное меню
    """
    if message.text == Globals.subscribe_mailing_text:
        subscribe(message)
    elif message.text == Globals.unsubscribe_mailing_text:
        unsubscribe(message)
    elif message.text == Globals.mailing_back:
        default_menu(message)
    else:
        bot.send_message(message.chat.id,
                         Globals.does_not_understand_in_mailing)
        default_menu(message)


def processing_in_choose_option_date(message, choose_city):
    """
    Обработка сообщений в выборе опции для погоды
    :param message: сообщение от пользователя
    :param choose_city: переходит в эту функцию после выбора опции
    """
    option = Globals.default_option
    if message.text == Globals.message_text_now:
        option = Globals.option_now
    elif message.text == Globals.message_text_5days:
        option = Globals.option_5days
    choose_city(message, option)


def processing_in_choose_city(message, option, choose_option, weather_now,
                              weather_5days):
    """
    Обработка сообщений в выборе города для погодв
    :param message:  сообщение от пользователя
    :param option: опция
    :param choose_option: выбор опции, если неправильный ввод
    :param weather_now: погода сейчас
    :param weather_5days: погода на 5 дней
    """
    keyboard = buttons_in_choose_city()
    if option == Globals.default_option:
        bot.send_message(message.chat.id,
                         Globals.does_not_understand_in_option)
        choose_option(message)
    else:
        city = bot.send_message(message.chat.id,
                                Globals.choose_city_text,
                                reply_markup=keyboard)
        if option == Globals.option_now:
            bot.register_next_step_handler(city, weather_now)
        elif option == Globals.option_5days:
            bot.register_next_step_handler(city, weather_5days)


def processing_in_continue_or_stop(message, choose_option, default_menu):
    """
    После того, как пользователь выберет погоду, ему будет предложено
    продолжить выбирать погоду или перейти в основное меню
    обработка сообщений
    :param message: сообщение от пользователя
    :param choose_option: выбор опции, если пользователь хочет продолжить
    узнавать погоду
    :param default_menu: основное меню
    :return:
    """
    if message.text == Globals.weather_continue:
        choose_option(message)
    elif message.text == Globals.weather_menu:
        default_menu(message)
    else:
        bot.message_handler(Globals.weather_continue_text)
        default_menu(message)


def schedule_checker():
    """
    Проверка времени для рассылки
    """
    while True:
        schedule.run_pending()
        sleep(1)
