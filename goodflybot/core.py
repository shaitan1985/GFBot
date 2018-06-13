from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                        ConversationHandler)
from telegram import ReplyKeyboardMarkup
from goodflybot.config import Config
from goodflybot.DataWorker import FSWorker
from telegram.ext import CommandHandler, MessageHandler, Filters

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [['Microphones1', 'Preamps'],
                  ['Compressors', 'Contacts'],
                  ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

mapping = {'Microphones': 'http://goodflymicrophones.com/mikrofony/',
            'Preamps': 'http://goodflymicrophones.com/goodfly-mp312-2/',
            'Compressors': 'http://goodflymicrophones.com/kompressory/',
            'Contacts': 'http://goodflymicrophones.com/kontakty/'
}


def start(bot, update): # when it starts
    update.message.reply_text(
        "Hi! What about you want to know?",
        reply_markup=markup)

    return CHOOSING

def regular_choice(bot, update, user_data): #some stupid answer for regular choice
    text = update.message.text

    update.message.reply_text(mapping.get(text))

    return TYPING_REPLY

def done(bot, update, user_data):# here is nothing needs/ clear and make goodbye

    update.message.reply_text("Thank you! Goodbye!")

    user_data.clear()
    return ConversationHandler.END

def error(bot, update, error):
    """Log Errors caused by Updates."""
    FSWorker.log('Update "{}" caused error "{}"'.format(update, error))




def main():
    #точка входа в программу
    config = Config()
    token = config.token

    updater = Updater(token=token)

    dispatcher = updater.dispatcher

    #Add conversation handler - named params

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],       #list of hndlers

        states={
            CHOOSING: [RegexHandler('^(Microphones|Preamps|Compressors|Contacts)$',
                                    regular_choice,
                                    pass_user_data=True),
                       ],
        }, #dict of handlers which will be chosen by key from return

        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]   #list of handlers
    )

    dispatcher.add_handler(conv_handler)

    # log all errors
    dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()