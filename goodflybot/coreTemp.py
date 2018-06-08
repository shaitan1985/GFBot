from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                        ConversationHandler)
from telegram import ReplyKeyboardMarkup
from config import Config
from DataWorker import FSWorker
from telegram.ext import CommandHandler, MessageHandler, Filters


CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [['Microphones', 'Preamps'],
                  ['Compressors', 'Contacts'],
                  ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)



def facts_to_str(user_data): # we don't need it
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(bot, update): # when it starts
    update.message.reply_text(
        "Hi! What about you want to know?",
        reply_markup=markup)

    return CHOOSING


def regular_choice(bot, update, user_data): #some stupid answer for regular choice
    text = update.message.text
    user_data['choice'] = text
    update.message.reply_text(
        'Your {}? Yes, I would love to hear about that!'.format(text.lower()))

    return TYPING_REPLY


def custom_choice(bot, update): # i think here is some deadend must be
    update.message.reply_text('Alright, please send me the category first, '
                              'for example "Most impressive skill"')

    return TYPING_CHOICE


def received_information(bot, update, user_data):
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text("Neat! Just so you know, this is what you already told me:"
                              "{}"
                              "You can tell me more, or change your opinion on something.".format(
                                  facts_to_str(user_data)), reply_markup=markup)

    return CHOOSING


def done(bot, update, user_data):# here is nothing needs/ clear and make goodbye
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("I learned these facts about you:"
                              "{}"
                              "Until next time!".format(facts_to_str(user_data)))

    user_data.clear()
    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)





def main():
    #точка входа в программу
    config = Config()
    token = config.token

    updater = Updater(token=token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [RegexHandler('^(Microphones|Preamps|Compressors|Contacts)$',
                                    regular_choice,
                                    pass_user_data=True)
                       ],

            TYPING_CHOICE: [MessageHandler(Filters.text,
                                           regular_choice,
                                           pass_user_data=True),
                            ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information,
                                          pass_user_data=True),
                           ],
        },

        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.


    updater.idle()








    # dispatcher = updater.dispatcher
    #
    # start_handler = CommandHandler('start', start) #start command
    # dispatcher.add_handler(start_handler)
    #
    #
    # echo_handler = MessageHandler(Filters.text, echo) # echo filter and answer
    # dispatcher.add_handler(echo_handler)
    #
    # updater.start_polling()
    #
    # updater.idle()

if __name__ == '__main__':
    main()