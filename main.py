from bs4 import BeautifulSoup
import requests
import schedule
import telebot
from telebot import types
from time import sleep
from threading import Thread

from Functions import buttons_in_default_menu, button_in_mailing, \
    buttons_in_choose_option, buttons_in_weather, print_weather
from Globals import api_key, bot, Globals, db, news_url, news_def_url, \
    url_openweather, url_forecast


@bot.message_handler(commands=[Globals.start_com])
def start(message):
    """
    Сообщение от бота при команде /start
    """
    start_message = bot.send_message(message.chat.id, Globals.start_message)
    default_menu(start_message)


@bot.message_handler(command=[Globals.menu_com])
def default_menu(message):
    """
    Отрисовывает кнопки в меню, сообщение при команде /menu
    """
    keyboard = buttons_in_default_menu()
    menu_question = bot.send_message(message.chat.id,
                                     Globals.default_menu_text,
                                     reply_markup=keyboard)
    bot.register_next_step_handler(menu_question, menu)


@bot.message_handler(content_types=[Globals.content_type_menu])
def menu(message):
    """
    Основное меню, обработка текста
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


def bot_does_not_understand(message):
    """
    Неизвестное сообщение от пользователя
    """
    bot.send_message(message.chat.id, Globals.does_not_understand_message)
    default_menu(message)


def mailing_buttons(message):
    """
    Отрисовывает кнопки в рассылке
    """
    keyboard = button_in_mailing()
    mailing_message = bot.send_message(message.chat.id,
                                       Globals.mailing_question_text,
                                       reply_markup=keyboard)
    bot.register_next_step_handler(mailing_message, mailing)


def mailing(message):
    """
    Обработка сообщение от пользователя в рассылку
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


@bot.message_handler(commands=[Globals.subscribe_com])
def subscribe(message):
    """
    Подписка на рассылку, проверяет, есть ли пользователь в БД
    Если нет, то добавляет
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
    print("------sub---------")
    db.print_info()
    print("------sub---------")
    default_menu(message)


@bot.message_handler(commands=[Globals.unsubscribe_com])
def unsubscribe(message):
    """
    Отписка от рассылки
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
    print("------unsub---------")
    db.print_info()
    print("------unsub---------")
    default_menu(message)


@bot.message_handler(commands=[Globals.help_com])
def help(message):
    """
    Бот пишет соощение со списком команд
    """
    bot.send_message(message.chat.id, Globals.help_message)


@bot.message_handler(commands=[Globals.news_com])
def last_news(message):
    """
    Парсинг сайта с новостями, вывод пользователю
    """
    response = requests.get(news_def_url, headers=Globals.header)
    soup = BeautifulSoup(response.content, Globals.html_pars)
    news_text = soup.findAll(Globals.news_class,
                             class_=Globals.news_item_class)
    for number in range(0, len(news_text[:Globals.news_text_cut])):
        txt = f"{number + 1}) {news_text[number].text}"
        bot.send_message(message.chat.id, txt)
    default_menu(message)


@bot.message_handler(commands=[Globals.weather_com])
def choose_option(message):
    """
    Выбор опции в погоде (на 5 дней или сейчас)
    """
    keyboard = buttons_in_choose_option()
    option_days = bot.send_message(message.chat.id,
                                   Globals.choose_option_text,
                                   reply_markup=keyboard)
    bot.register_next_step_handler(option_days, choose_option_date)


def choose_option_date(message):
    """
    Обработка опции
    """
    option = Globals.default_option
    if message.text == Globals.message_text_now:
        option = Globals.option_now
    elif message.text == Globals.message_text_5days:
        option = Globals.option_5days
    choose_city(message, option)


def choose_city(message, option):
    """
    Выбор города
    """
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    msc = types.KeyboardButton(text=Globals.default_btn_1)
    minsk = types.KeyboardButton(text=Globals.default_btn_2)
    keyboard.add(msc, minsk)

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


def weather_now(message):
    """
    Погода сейчас в выбранном городе
    """
    keyboard = buttons_in_weather()
    city_name = message.text
    try:
        params = {Globals.api_id: api_key, Globals.city_name_api: city_name,
                  Globals.units_settings: Globals.units_measuring,
                  Globals.language: Globals.rus_language}
        result = requests.get(url_openweather, params=params)
        weather = result.json()
        print(weather)
        city = weather[Globals.city_name_for_search]
        city_temperature = float(
            weather[Globals.json_main][Globals.json_temperature])
        city_descr = weather[Globals.json_weather][0][
            Globals.json_weather_description]
        city_temp_feels = float(
            weather[Globals.json_main][Globals.json_temp_feels])
        city_pressure = weather[Globals.json_main][Globals.json_pressure]
        city_humidity = weather[Globals.json_main][Globals.json_humidity]
        city_wind = weather[Globals.json_wind][Globals.json_wind_speed]
        weather_text = bot.send_message(message.chat.id,
                                        print_weather(city, city_temperature,
                                                      city_temp_feels,
                                                      city_pressure,
                                                      city_humidity, city_wind,
                                                      city_descr),
                                        reply_markup=keyboard)

    except KeyError:
        weather_text = bot.send_message(message.chat.id,
                                        f"{Globals.city_not_found}: {city_name} :(",
                                        reply_markup=keyboard)
    bot.register_next_step_handler(weather_text, continue_or_stop)


def weather_5days(message):
    """
    Погода на 5 дней в выбранном городе
    """
    city_name = message.text
    keyboard = buttons_in_weather()
    try:
        params = {Globals.api_id: api_key, Globals.city_name_api: city_name,
                  Globals.units_settings: Globals.units_measuring,
                  Globals.language: Globals.rus_language}
        result = requests.get(url_forecast, params=params)
        weather = result.json()
        for i in weather[Globals.json_weather_list]:
            print(i[Globals.json_dt_txt])
        city = weather[Globals.json_weather_city][Globals.city_name_for_search]
        text = ""
        for num, i in enumerate(weather[Globals.json_weather_list]):
            if num % 2 == 0:
                text += f"{i[Globals.json_dt_txt][5:10]}" \
                        f"\t\t\t {i[Globals.json_dt_txt][10:16]} " \
                        f"\t\t\t {float(i[Globals.json_main][Globals.json_temperature])} ℃\n"
            if (num + 1) % 8 == 0:
                text += "\n"
        weather_text = bot.send_message(message.chat.id, f" {city}:\n{text}",
                                        reply_markup=keyboard)
    except KeyError:
        weather_text = bot.send_message(message.chat.id,
                                        f"Город {city_name} не найден :(",
                                        reply_markup=keyboard)
    bot.register_next_step_handler(weather_text, continue_or_stop)


def continue_or_stop(message):
    """
    Продолжить узнавать погоду или выйти в меню
    """
    if message.text == Globals.weather_continue:
        choose_option(message)
    elif message.text == Globals.weather_menu:
        default_menu(message)
    else:
        bot.message_handler(Globals.weather_continue_text)
        default_menu(message)


@bot.message_handler(commands=[Globals.lastnews_com])
def for_subscribers():
    """
    Рассылка новостей для подписчиков
    """
    subscribers = db.get_subscriptions()
    response = requests.get(news_url, headers=Globals.header)
    soup = BeautifulSoup(response.content, Globals.html_pars)
    title = soup.findAll(Globals.last_news_class,
                         class_=Globals.last_news_item_class)
    for i in range(0, len(title[:Globals.news_crop])):
        txt = f"{str(i + 1)} ) {title[i].text}"
        for id in subscribers:
            print(id[1])
            bot.send_message(id[1],
                             Globals.text_to_link.format(
                                 title[i][Globals.link_format],
                                 txt),
                             parse_mode=Globals.html_pars_mode)


def schedule_checker():
    """
    Проверка времени
    """
    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == "__main__":
    schedule.every().day.at(Globals.mailing_time).do(for_subscribers)
    Thread(target=schedule_checker).start()
    try:
        bot.polling(none_stop=True, interval=0)
    except:
        pass
