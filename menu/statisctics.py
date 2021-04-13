from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from menu import start
import states
from user_bd import User, init_user, session, Word, Theme


def statistics(update: Update, context: CallbackContext):
    user = init_user(update.callback_query.message.chat_id)


    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Назад', callback_data=str(states.EXIT))],
    ])
    update.callback_query.message.edit_text(f'\n Последнее выученное слово: {user.last_word}, \n Последнее изучение: { user.last_repetition }', reply_markup=keyboard_markup)
    start.menu(update)
    return states.BEGIN