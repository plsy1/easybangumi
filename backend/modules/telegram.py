import telebot
from core.config import conf


class TGBOT:
    
    config = conf.get_telegram_config()

    bot = telebot.TeleBot(token=config.get('token'))

    @staticmethod
    def Send_Message(message, chat_id=config.get('chat_id')):
        TGBOT.bot.send_message(chat_id, message)
