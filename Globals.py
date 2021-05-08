import telebot
from telebot import types

from PostgreSQL import PostgresDb


class Globals(object):
    # --------------Погода----------------
    wthr_now = False
    wthr_5days = False
    btn_weather_text = "Погода ✨"
    default_option = "no_option"
    message_text_now = "Сейчас"
    message_text_5days = "На 5 дней"
    option_now = "now"
    option_5days = "5days"
    default_btn_1 = "Москва"
    default_btn_2 = "Минск"
    weather_continue = "Продолжить узнавать погоду 🌤"
    weather_menu = "Меню"

    # --------------Клавиатура------------
    default_keyboard = types.ReplyKeyboardMarkup(row_width=1,
                                                 resize_keyboard=True)
    # --------------Тесты-----------------
    user_id_test = 11
    user_id_test_1 = 1
    first_name = "test"
    content_type = "text"
    # --------------Кнопки----------------
    btn_mailing_text = "Рассылка ✨"
    btn_news_text = "Новости ✨"
    btn_subscribe_text = "Подписаться на рассылку 🙃"
    btn_unsubscribe_text = "Отписаться от рассылки 😒"
    btn_back = "Назад"
    btn_now = "Сейчас"
    btn_5days = "На 5 дней"
    btn_continue = "Продолжить узнавать погоду 🌤"
    btn_menu = "Меню"

    # --------------Сообщения-------------
    start_message = "Привет! Если хочешь узнать cписок команд, введи команду /help"
    default_menu_text = "Что ты хочешь узнать? 🤓"
    help_message = "Здравствуй! Меня зовут Sunny 🥰\n" \
                   "Я могу тебе рассказать про погоду, а также про последние новости!\n" \
                   "Список команд: /start - начать работу с ботом, главное меню\n" \
                   "/subscribe - подписаться на рассылку новостей\n" \
                   "/unsubscribe - отписаться от рассылки новостей\n" \
                   "/weather - узнать погоду\n" \
                   "/news -  узнать последние новости\n" \
                   "/help - помощь\n" \
                   "Мой создатель: @arncpp"
    does_not_understand_message = "Я не понимаю твоё сообщение 🥺"
    mailing_question_text = "Что Вас интересует? 🧐"
    choose_option_text = "На сколько дней вы хотите узнать погоду? 🌤"
    does_not_understand_in_mailing = "Я не понимаю 🌝"
    does_not_understand_in_option = "Я не понимаю :( Выбери опцию. 🌚"
    choose_city_text = "Выберите или введите название любой страны или города 🌍"
    city_not_found = "Я ничего не нашел по вашему запросу"
    weather_continue_text = "Я не понимаю, что ты хочешь сказать 😞"

    # -----Запрос погоды через API------
    api_id = "APPID"
    city_name_api = "q"
    units_settings = "units"
    units_measuring = "metric"
    language = "lang"
    rus_language = "ru"
    city_name_for_search = "name"
    json_main = "main"
    json_temperature = "temp"
    json_weather = "weather"
    json_weather_description = "description"
    json_temp_feels = "feels_like"
    json_pressure = "pressure"
    json_humidity = "humidity"
    json_wind = "wind"
    json_wind_speed = "speed"
    json_weather_list = "list"
    json_weather_city = "city"
    json_dt_txt = "dt_txt"

    # --------------Команды-------------
    start_com = "start"
    menu_com = "menu"
    content_type_menu = "text"
    weather_slash_com = "Погода ✨"
    mailing_com = "Рассылка ✨"
    text_news_com = "Новости ✨"
    last_news_com = "/lastnews"
    news_slash_com = "/news"
    help_slash_com = "/help"
    subscribe_slash_com = "/subscribe"
    unsubscribe_slash_com = "/unsubscribe"
    choose_option_weather_com = "/weather"
    subscribe_com = "subscribe"
    unsubscribe_com = "unsubscribe"
    help_com = "help"
    news_com = "news"
    weather_com = "weather"
    lastnews_com = "lastnews"

    # --------------Подписка------------
    true_status = "(True,)"
    false_status = "(False,)"
    subscription_is_true = "Вы успешно подписались на рассылку! 🥰"
    subscription_is_true_now = "Вы подписались на рассылку! 🥰"
    subscription_activated = "Вы уже подписаны на рассылку! 😉"
    subscription_is_false = "Вы итак не подписаны 😟"
    subscription_is_false_now = "Вы успешно отписались от рассылки! 😒"
    subscription_not_activated = "Вы уже отписались 🥺"
    subscribe_mailing_text = "Подписаться на рассылку 🙃"
    unsubscribe_mailing_text = "Отписаться от рассылки 😒"
    mailing_back = "Назад"
    mailing_time = "06:00"

    # --------------Парсинг-------------
    html_pars = "html.parser"
    html_pars_mode = "html"
    news_class = "span"
    last_news_class = "a"
    last_news_item_class = "list-item__title"
    news_item_class = "cell-list__item-title"
    text_to_link = "<a href='{}'>{}</a>"
    link_format = "href"
    news_text_cut = -21
    news_crop = -15
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}


# --------------Бот-------------
TOKEN = "-------------------"
bot = telebot.TeleBot(TOKEN)

# --------------API-------------
api_key = "-----------------"

# --------------Ссылки----------
url_openweather = "http://api.openweathermap.org/data/2.5/weather"
url_forecast = "http://api.openweathermap.org/data/2.5/forecast"
news_url = "https://ria.ru/world/"
news_def_url = "https://ria.ru/"

# --------------База данных-----
db = PostgresDb()
