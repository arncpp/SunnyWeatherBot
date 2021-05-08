import schedule
from threading import Thread

from api_request import weather_now_api, weather_5days_api
from Functions import buttons_in_default_menu, button_in_mailing, \
    buttons_in_choose_option, \
    schedule_checker, check_user_unsubscribe, \
    check_user_subscribe, parsing_news_for_sub, parsing_last_news, \
    processing_in_menu, processing_in_mailing, \
    processing_in_choose_option_date, \
    processing_in_choose_city, processing_in_continue_or_stop
from Globals import bot, Globals


@bot.message_handler(commands=[Globals.start_com])
def start(message):
    """
    Команда /start. Бот отправляет сообщение и переходит в основное меню
    :param message: сообщение пользователя
    """
    start_message = bot.send_message(message.chat.id, Globals.start_message)
    default_menu(start_message)


@bot.message_handler(command=[Globals.menu_com])
def default_menu(message):
    """
    Отрисовывает кнопки в меню, сообщение при команде /menu
    :param message: сообщение пользователя
    """
    keyboard = buttons_in_default_menu()
    menu_question = bot.send_message(message.chat.id,
                                     Globals.default_menu_text,
                                     reply_markup=keyboard)
    bot.register_next_step_handler(menu_question, menu)


@bot.message_handler(content_types=[Globals.content_type_menu])
def menu(message):
    """
    Основное меню, обрабатывает текст
    :param message: сообщение пользователя
    """
    processing_in_menu(message, choose_option, mailing_buttons, last_news,
                       help, subscribe, unsubscribe, for_subscribers,
                       bot_does_not_understand)


def bot_does_not_understand(message):
    """
    Вызывается, если пользователь ввел неизвестное сообщение
    :param message: сообщение пользователя
    """
    bot.send_message(message.chat.id, Globals.does_not_understand_message)
    default_menu(message)


def mailing_buttons(message):
    """
    Отрисовывает кнопки в рассылке
    :param message: сообщение пользователя
    """
    keyboard = button_in_mailing()
    mailing_message = bot.send_message(message.chat.id,
                                       Globals.mailing_question_text,
                                       reply_markup=keyboard)
    bot.register_next_step_handler(mailing_message, mailing)


def mailing(message):
    """
    Обработка сообщение от пользователя в рассылке
    :param message: сообщение пользователя
    """
    processing_in_mailing(message, subscribe, unsubscribe, default_menu)


@bot.message_handler(commands=[Globals.subscribe_com])
def subscribe(message):
    """
    Подписка на рассылку, проверяет, есть ли пользователь в БД
    Если нет, то добавляет
    :param message: сообщение пользователя
    """
    check_user_subscribe(message)
    default_menu(message)


@bot.message_handler(commands=[Globals.unsubscribe_com])
def unsubscribe(message):
    """
    Отписка от рассылки
    :param message: сообщение пользователя
    """
    check_user_unsubscribe(message)
    default_menu(message)


@bot.message_handler(commands=[Globals.help_com])
def help(message):
    """
    Бот пишет соощение со списком команд
    :param message: сообщение пользователя
    """
    bot.send_message(message.chat.id, Globals.help_message)


@bot.message_handler(commands=[Globals.news_com])
def last_news(message):
    """
    Парсинг сайта с новостями, вывод пользователю
    :param message: сообщение пользователя
    """
    parsing_last_news(message)
    default_menu(message)


@bot.message_handler(commands=[Globals.weather_com])
def choose_option(message):
    """
    Выбор опции в погоде (на 5 дней или сейчас)
    :param message: сообщение пользователя
    """
    keyboard = buttons_in_choose_option()
    option_days = bot.send_message(message.chat.id,
                                   Globals.choose_option_text,
                                   reply_markup=keyboard)
    bot.register_next_step_handler(option_days, choose_option_date)


def choose_option_date(message):
    """
    Обработка опции, которую выбрал пользователь
    :param message: сообщение пользователя
    """
    processing_in_choose_option_date(message, choose_city)


def choose_city(message, option):
    """
    Обработка опции, выбранной пользователем, выбор города
    :param message: сообщение пользователя
    :param option: опция
    """
    processing_in_choose_city(message, option, choose_option, weather_now,
                              weather_5days)


def weather_now(message):
    """
    Погода сейчас в выбранном городе
    :param message: сообщение пользователя
    """
    weather_text = weather_now_api(message)
    bot.register_next_step_handler(weather_text, continue_or_stop)


def weather_5days(message):
    """
    Погода на 5 дней в выбранном городе
    :param message: сообщение пользователя
    """
    weather_text = weather_5days_api(message)
    bot.register_next_step_handler(weather_text, continue_or_stop)


def continue_or_stop(message):
    """
    Продолжить узнавать погоду или выйти в меню
    :param message: сообщение пользователя
    """
    processing_in_continue_or_stop(message, choose_option, default_menu)


@bot.message_handler(commands=[Globals.lastnews_com])
def for_subscribers():
    """
    Рассылка новостей для подписчиков
    """
    parsing_news_for_sub()


if __name__ == "__main__":
    schedule.every().day.at(Globals.mailing_time).do(for_subscribers)
    Thread(target=schedule_checker).start()
    bot.polling(none_stop=True, interval=0)
