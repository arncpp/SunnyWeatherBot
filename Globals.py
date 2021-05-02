import telebot
from telebot import types
import requests

from db_subsc import SQL_db



class Globals(object):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    TOKEN = ""
    wthr_now = False
    wthr_5days = False
    default_keyboard = types.ReplyKeyboardMarkup(row_width=1,
                                                 resize_keyboard=True)
    start_message = "Привет! Если хочешь узнать cписок команд, введи команду /help"
    btn_weather_text = "Погода"
    btn_mailing_text = "Рассылка"
    btn_news_text = "Новости"
    default_menu_text = "Что ты хочешь узнать?"
    help_message = "Здравствуй! Меня зовут Sunny 🥰\n" \
                   "Я могу тебе рассказать про погоду, а также про последние новости!\n" \
                   "Список команд: /start - начать работу с ботом, главное меню\n" \
                   "/subscribe - подписаться на рассылку новостей\n" \
                   "/unsubdcribe - отписаться от рассылки новостей\n" \
                   "/weather - узнать погоду\n" \
                   "/news -  узнать последние новости\n" \
                   "/help - помощь\n" \
                   "Мой создатель: @arncpp"
    does_not_understand_message = "Я не понимаю твоё сообщение 🥺"
    mailing_question_text = "Что Вас интересует?"
    subscription_is_true = "Вы успешно подписались на рассылку!"
    subscription_is_true_now = "Вы подписались на рассылку!"
    subscription_activated = "Вы уже подписаны на рассылку!"
    true_status = "(1,)"
    false_status = "(0,)"
    subscription_is_false = "Вы итак не подписаны :("
    subscription_is_false_now = "Вы успешно отписались от рассылки!"
    subscription_not_activated = "Вы уже отписались"
    html_pars = "html.parser"
    news_class = "span"
    news_item_class = "cell-list__item-title"
    news_text_cut = -21
    choose_option_text = "На сколько дней вы хотите узнать погоду?"
    default_option = "no_option"
    message_text_now = "Сейчас"
    message_text_5days = "На 5 дней"
    option_now = "now"
    option_5days = "5days"

bot = telebot.TeleBot(Globals.TOKEN)
api_key = ""
url_openweather = "http://api.openweathermap.org/data/2.5/weather"
url_forecast = "http://api.openweathermap.org/data/2.5/forecast"
db = SQL_db("db_users.db")
news_url = "https://ria.ru/world/"
news_def_url = "https://ria.ru/"


