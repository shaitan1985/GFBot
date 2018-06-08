from telegram.ext import Updater
from config import Config
from DataWorker import FSWorker
from telegram.ext import CommandHandler, MessageHandler, Filters



def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def main():
    #точка входа в программу
    config = Config()
    token = config.token

    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start) #start command
    dispatcher.add_handler(start_handler)


    echo_handler = MessageHandler(Filters.text, echo) # echo filter and answer
    dispatcher.add_handler(echo_handler)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()