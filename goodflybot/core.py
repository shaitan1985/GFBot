from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                        ConversationHandler)
from telegram import ReplyKeyboardMarkup
from config import Config
from DataWorker import FSWorker
from telegram.ext import CommandHandler, MessageHandler, Filters





def main():
    #точка входа в программу
    config = Config()
    token = config.token

    updater = Updater(token=token)

    dispatcher = updater.dispatcher

    #Add conversation handler - named params

    conv_handler = ConversationHandler(
        entry_points=..., #list of hndlers
        states=..., #dict of handlers
        fallbacks=...   #list of handlers


    )







    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()