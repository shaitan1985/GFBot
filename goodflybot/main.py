from telegram.ext import Updater
from .config import Config

from telegram.ext import CommandHandler, MessageHandler, Filters



class TelegramBot(object):
    def __init__(self, config):
        self.config = config
        self.updater = Updater(token=config.get('token'))


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def begin():
    #точка входа в программу
    config = Config()
    token = config.get('token')

    updater = Updater(token='TOKEN')
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start) #start command
    dispatcher.add_handler(start_handler)
    updater.start_polling()

    echo_handler = MessageHandler(Filters.text, echo) # echo filter and answer
    dispatcher.add_handler(echo_handler)

    updater.stop()