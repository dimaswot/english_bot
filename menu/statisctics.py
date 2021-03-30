from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from menu import start
import states
from user import User, Settings, Statistics


def statistics(update: Update, context: CallbackContext):
    user = User()
    user_id = update.callback_query.message.chat.id

    if not user.check_in_bd(update.callback_query.message.chat.id):
        user.user_id = update.callback_query.message.chat_id
        user.settings = Settings()
        user.statistics = Statistics()
        user.refresh()

    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Назад', callback_data=str(states.EXIT))],
    ])
    update.callback_query.message.edit_text(f'Изученные темы: {user.statistics.themes} , \n Кол-во выученных слов: {user.statistics.count_words}, \n Последнее выученное слово: {user.statistics.last_words}, \n Последнее изучение: { user.statistics.last_repetition } ', reply_markup=keyboard_markup)
    start.menu(update)
    return states.BEGIN