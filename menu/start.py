from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from datetime import datetime

from states import BEGIN, THEME, TEST, SETTINGS, REDACT_KOL_VO, STOP_SCHEDULLER, STATISTICS
from user import User

def start(update: Update, context: CallbackContext):
    user = User()
    print('Я ТУУУУУУУУУУУУУУУУУУУТ')
    if (user.check_in_bd(update.message.chat.id)):
        print('NEW USER')
    else:
        print('Я хуй знает')


    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Тест', callback_data=str(TEST))],
        [InlineKeyboardButton('Статистика', callback_data=str(STATISTICS))],
        [InlineKeyboardButton('Настройки', callback_data=str(SETTINGS))],
    ])
    update.message.reply_text('Привет! Я бот, для изучения Английского. Начнем?', reply_markup=keyboard_markup)
    return BEGIN


def menu(update: Update, context: CallbackContext):
    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Тест', callback_data=str(TEST))],
        [InlineKeyboardButton('Статистика', callback_data=str(STATISTICS))],
        [InlineKeyboardButton('Настройки', callback_data=str(SETTINGS))],
    ])
    update.callback_query.message.edit_text('Выберите пункт меню', reply_markup=keyboard_markup)
    return BEGIN