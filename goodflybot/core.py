from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                        ConversationHandler)
from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from goodflybot.config import Config
from goodflybot.DataWorker import FSWorker

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [['Microphones', 'Preamps', 'Compressors', 'Contacts'],
                  ['/Start', 'Done']]
keyboard = [[
    InlineKeyboardButton('Microphones', url='http://goodflymicrophones.com/mikrofony/'),
    InlineKeyboardButton('Preamps', url='http://goodflymicrophones.com/goodfly-mp312-2/')],
    [InlineKeyboardButton('Compressors', url='http://goodflymicrophones.com/kompressory/'),
    InlineKeyboardButton('Contacts', url='http://goodflymicrophones.com/kontakty/')]
    ]


reply_markup = InlineKeyboardMarkup(keyboard)

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)

mapping = {'Microphones': 'http://goodflymicrophones.com/mikrofony/',
            'Preamps': 'http://goodflymicrophones.com/goodfly-mp312-2/',
            'Compressors': 'http://goodflymicrophones.com/kompressory/',
            'Contacts': 'http://goodflymicrophones.com/kontakty/'
}

"""
class GFBot(object):
    # class contains main bots methods.
    def __init__(self, token):
        self.__token = token
        self.__updater = Updater(token=token)
        self.__dispatcher = self.__updater.dispatcher
        self.__int_params = {}
        self.__collect_keyboard()


    def __add_handlers(self):



    def __collect_keyboard(self):

        self.set_param('reply_keyboard',[['Microphones', 'Preamps', 'Compressors', 'Contacts'],
                          ['/Start', 'Done']])

        self.set_param('mapping', {'Microphones': 'http://goodflymicrophones.com/mikrofony/',
                   'Preamps': 'http://goodflymicrophones.com/goodfly-mp312-2/',
                   'Compressors': 'http://goodflymicrophones.com/kompressory/',
                   'Contacts': 'http://goodflymicrophones.com/kontakty/'
                   })

    def set_param(self, key, value):
        self.__int_params(key) = value


    def get_param(self, key):

        tmp = self.__int_params.get(key)
        if tmp is None:
            FSWorker.log('key "{}" not found in params'.format(key))
        return tmp

"""

def append_m_id(update, user_data):
    m_id = update.message.message_id
    if user_data.get('message') is None:
        user_data['messages'] = [m_id, ]
    else:
        user_data.get('message').append(m_id)

def clear_msgs(update, user_data):
    for item in user_data.get('message').items():
        bot.deleteMessage(chat_id=update.message.chat.id, message_id=item)

def start(bot, update, user_data): # when it starts

    append_m_id(update, user_data)


    update.message.reply_text('Menu', reply_markup=reply_markup)
#     update.message.reply_text(
#         "Hi! What about you want to know?",
#         reply_markup=reply_markup)

    return CHOOSING

def regular_choice(bot, update, user_data): #some stupid answer for regular choice
    append_m_id(update, user_data)

    text = update.message.text

    update.message.reply_text(mapping.get(text))

    return CHOOSING

def done(bot, update, user_data):# here is nothing needs/ clear and make goodbye

    update.message.reply_text("Thank you! Goodbye!")
    clear_msgs(update, user_data)
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
        entry_points=[CommandHandler('start', start, pass_user_data=True)],       #list of hndlers

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