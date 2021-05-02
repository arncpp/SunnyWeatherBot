import time
from Globals import bot
from telebot import types


class TestTeleBot:
    def test_message_handler(self):
        msg = self.create_text_message('/help')

        @bot.message_handler(commands=['help', 'start'])
        def command_handler(message):
            message.text = 'get'

        bot.process_new_messages([msg])
        time.sleep(1)
        assert msg.text == 'get'

    @staticmethod
    def create_text_message(text):
        params = {'text': text}
        chat = types.User(11, False, 'test')
        print(types.Message(1, None, None, chat, 'text', params, ""))
        return types.Message(1, None, None, chat, 'text', params, "")


TestTeleBot().test_message_handler()
