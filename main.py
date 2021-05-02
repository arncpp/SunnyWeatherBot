import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
from Globals import Globals, bot, api_key, url_openweather, url_forecast, db, \
    news_url, news_def_url
from threading import Thread
from db_subsc import SQL_db
from time import sleep
import schedule
from Functions import buttons_in_default_menu, button_in_mailing, \
    buttons_in_choose_option, buttons_in_weather, print_weather


@bot.message_handler(commands=["start"])
def start(message):
    start_message = bot.send_message(message.chat.id, Globals.start_message)
    default_menu(start_message)


@bot.message_handler(command=["menu"])
def default_menu(message):
    keyboard = buttons_in_default_menu()
    menu_question = bot.send_message(message.chat.id,
                                     Globals.default_menu_text,
                                     reply_markup=keyboard)
    bot.register_next_step_handler(menu_question, menu)


@bot.message_handler(content_types=["text"])
def menu(message):
    commands_list = {"Погода": choose_option, "Рассылка": mailing_buttons,
                     "Новости": last_news, "/news": last_news,
                     "/help": help, "/subscribe": subscribe,
                     "/unsubscribe": unsubscribe, "/weather": choose_option,
                     "/lastnews": for_subscribers}
    if message.text in commands_list.keys():
        commands_list[message.text](message)
    else:
        bot_does_not_understand(message)


def bot_does_not_understand(message):
    bot.send_message(message.chat.id, Globals.does_not_understand_message)
    default_menu(message)


def mailing_buttons(message):
    keyboard = button_in_mailing()
    mailing_message = bot.send_message(message.chat.id,
                                       Globals.mailing_question_text,
                                       reply_markup=keyboard)
    bot.register_next_step_handler(mailing_message, mailing)


def mailing(message):
    if message.text == "Подписаться на рассылку":
        subscribe(message)
    elif message.text == "Отписаться от рассылки":
        unsubscribe(message)
    elif message.text == "Назад":
        default_menu(message)
    else:
        bot.send_message(message.chat.id, "Я не понимаю :(")
        default_menu(message)


@bot.message_handler(commands=["subscribe"])
def subscribe(message):
    user_id = message.chat.id
    if not db.subscriber_exists(user_id):
        db.add_subscriber(user_id, True)
        bot.send_message(user_id, Globals.subscription_is_true)
    elif db.check_status(user_id) == Globals.false_status:
        db.update_subscription(user_id, True)
        bot.send_message(user_id, Globals.subscription_is_true_now)
    elif db.check_status(user_id) == Globals.true_status:
        bot.send_message(user_id, Globals.subscription_activated)
    default_menu(message)


@bot.message_handler(commands=["unsubscribe"])
def unsubscribe(message):
    user_id = message.chat.id
    if not db.subscriber_exists(user_id):
        db.add_subscriber(user_id, False)
        bot.send_message(user_id, Globals.subscription_is_false)
    elif db.check_status(user_id) == Globals.true_status:
        db.update_subscription(user_id, False)
        bot.send_message(user_id, Globals.subscription_is_false_now)
    elif db.check_status(user_id) == Globals.false_status:
        bot.send_message(user_id, Globals.subscription_not_activated)
    default_menu(message)


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, Globals.help_message)


@bot.message_handler(commands=["news"])
def last_news(message):
    response = requests.get(news_def_url, headers=Globals.header)
    soup = BeautifulSoup(response.content, Globals.html_pars)
    news_text = soup.findAll(Globals.news_class,
                             class_=Globals.news_item_class)
    for number in range(0, len(news_text[:Globals.news_text_cut])):
        txt = f"{number + 1}) {news_text[number].text}"
        bot.send_message(message.chat.id, txt)
    default_menu(message)


@bot.message_handler(commands=["weather"])
def choose_option(message):
    keyboard = buttons_in_choose_option()
    option_days = bot.send_message(message.chat.id,
                                   Globals.choose_option_text,
                                   reply_markup=keyboard)
    bot.register_next_step_handler(option_days, choose_option_date)


def choose_option_date(message):
    option = Globals.default_option
    if message.text == Globals.message_text_now:
        option = Globals.option_now
    elif message.text == Globals.message_text_5days:
        option = Globals.option_5days
    choose_city(message, option)


def choose_city(message, option):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    msc = types.KeyboardButton(text="Москва")
    minsk = types.KeyboardButton(text="Минск")
    keyboard.add(msc, minsk)

    if option == Globals.default_option:
        bot.send_message(message.chat.id, "Я не понимаю :( Выбери опцию.")
        choose_option(message)
    else:
        city = bot.send_message(message.chat.id,
                                "Выберите или введите название любой страны или города.",
                                reply_markup=keyboard)
        if option == Globals.option_now:
            bot.register_next_step_handler(city, weather_now)
        elif option == Globals.option_5days:
            bot.register_next_step_handler(city, weather_5days)


def weather_now(message):
    keyboard = buttons_in_weather()
    city_name = message.text
    try:
        params = {"APPID": api_key, "q": city_name, "units": "metric",
                  "lang": "ru"}
        result = requests.get(url_openweather, params=params)
        weather = result.json()
        print(weather)
        city = weather["name"]
        city_temperature = float(weather["main"]["temp"])
        city_descr = weather["weather"][0]["description"]
        city_temp_feels = float(weather["main"]["feels_like"])
        city_pressure = weather["main"]["pressure"]
        city_humidity = weather["main"]["humidity"]
        city_wind = weather["wind"]["speed"]
        weather_text = bot.send_message(message.chat.id,
                                        print_weather(city, city_temperature,
                                                      city_temp_feels,
                                                      city_pressure,
                                                      city_humidity, city_wind,
                                                      city_descr),
                                        reply_markup=keyboard)

    except KeyError:
        weather_text = bot.send_message(message.chat.id,
                                        f"Я ничего не нашел по вашему запросу: {city_name} :(",
                                        reply_markup=keyboard)
    bot.register_next_step_handler(weather_text, continue_or_stop)


def weather_5days(message):
    city_name = message.text
    keyboard = buttons_in_weather()
    try:
        params = {'APPID': api_key, 'q': city_name, 'units': 'metric',
                  'lang': 'ru'}
        result = requests.get(url_forecast, params=params)
        weather = result.json()
        for i in weather["list"]:
            print(i["dt_txt"])
        city = weather["city"]["name"]
        text = ""
        for num, i in enumerate(weather["list"]):
            if num % 2 == 0:
                text += f"{i['dt_txt'][5:10]} \t\t\t {i['dt_txt'][10:16]} \t\t\t {float(i['main']['temp'])} ℃\n"
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
    if message.text == "Продолжить узнавать погоду":
        choose_option(message)
    elif message.text == "Меню":
        default_menu(message)
    else:
        bot.message_handler("Я не понимаю, что ты хочешь сказать :(")
        default_menu(message)


@bot.message_handler(commands=["lastnews"])
def for_subscribers(message):
    subscribers = db.get_subscriptions()
    response = requests.get(news_url, headers=Globals.header)
    soup = BeautifulSoup(response.content, Globals.html_pars)
    title = soup.findAll("a", class_="list-item__title")
    for i in range(0, len(title[:-15])):
        txt = str(i + 1) + ") " + title[i].text
        for id in subscribers:
            print(id[1])
            bot.send_message(id[1],
                             "<a href='{}'>{}</a>".format(title[i]['href'],
                                                          txt),
                             parse_mode='html')


def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == '__main__':
    schedule.every().day.at("06:00").do(for_subscribers)
    Thread(target=schedule_checker).start()
    try:
        bot.polling(none_stop=True, interval=0)
    except:
        pass
