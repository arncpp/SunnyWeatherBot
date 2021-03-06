import time
from telebot import types

from Globals import bot, Globals


class TestTeleBot:
    def test_message_handler(self):
        msg_help = self.create_text_message(Globals.help_slash_com)
        msg_weather = self.create_text_message(
            Globals.choose_option_weather_com)

        @bot.message_handler(commands=[Globals.help_com])
        def help_handler(message):
            """
            Тест команды /help
            :param message: входное сообщение
            """
            message.text = Globals.help_message

        bot.process_new_messages([msg_help])
        time.sleep(1)
        assert msg_help.text == Globals.help_message

        @bot.message_handler(commands=[Globals.weather_com])
        def weather_handler(message):
            """
            Тест команды /weather
            :param message: входное сообщение
            """
            message.text = Globals.choose_option_text

        bot.process_new_messages([msg_weather])
        time.sleep(1)
        assert msg_weather.text == Globals.choose_option_text

    @staticmethod
    def create_text_message(text):
        params = {Globals.content_type: text}
        chat = types.User(Globals.user_id_test, False, Globals.first_name)
        print(types.Message(Globals.user_id_test_1, None, None, chat, Globals.content_type, params, ""))
        return types.Message(Globals.user_id_test_1, None, None, chat, Globals.content_type, params, "")


TestTeleBot().test_message_handler()
