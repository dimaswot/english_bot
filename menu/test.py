from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from user import Settings, Statistics
import json

from states import BEGIN, TEST, EXIT
from user import User
from theme import Words
import random
from datetime import datetime


def test_first(update: Update, context: CallbackContext):
    user = User()
    words = Words('request.json')

    if not user.check_in_bd(update.callback_query.message.chat.id):
        user.user_id = update.callback_query.message.chat_id
        user.settings = Settings()
        user.statistics = Statistics()
        user.refresh()

    list = words.get_words(user.settings.word_number, user.settings.theme)
    random.shuffle(list)

    keyboard_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('1', callback_data=f'{list[0]}'),
            InlineKeyboardButton('2', callback_data=f'{list[1]}'),
            InlineKeyboardButton('3', callback_data=f'{list[2]}'),
            InlineKeyboardButton('4', callback_data=f'{list[3]}'),
        ],
        [InlineKeyboardButton('Главное меню', callback_data=str(EXIT))],
    ])
    update.callback_query.message.edit_text(f'Тема: {user.settings.theme},\nОписание: {words.get_description(user.settings.word_number, user.settings.theme)}, \nСлово: {words.get_word(user.settings.word_number, user.settings.theme)} \n Варианты ответов: \n 1. {list[0]} \n 2. {list[1]} \n 3. {list[2] } \n 4. {list[3]} \n  ', reply_markup=keyboard_markup)
    return TEST

def test(update: Update, context: CallbackContext):

    result = 'Ответ на прошлый вопрос был НЕ верным, будьте внимательнее!'
    user = User()
    words = Words('request.json')

    if not user.check_in_bd(update.callback_query.message.chat.id):
        user.user_id = update.callback_query.message.chat_id
        user.settings = Settings()
        user.statistics = Statistics()
        user.refresh()

    if words.get_translation(user.settings.word_number, user.settings.theme) == update.callback_query.data:
        user.settings.word_number += 1
        user.statistics.count_words += 1
        user.statistics.last_words = words.get_word(user.settings.word_number, user.settings.theme)
        user.statistics.last_repetition = str(datetime.utcnow())
        result = 'Ответ на прошлый вопрос был верным'
        user.refresh()

    if user.settings.word_number > words.get_word_count_theme(user.settings.theme):
        user.settings.word_number = 1
        user.refresh()

    list = words.get_words(user.settings.word_number, user.settings.theme)
    random.shuffle(list)

    keyboard_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('1', callback_data=f'{list[0]}'),
            InlineKeyboardButton('2', callback_data=f'{list[1]}'),
            InlineKeyboardButton('3', callback_data=f'{list[2]}'),
            InlineKeyboardButton('4', callback_data=f'{list[3]}'),
        ],
        [InlineKeyboardButton('Главное меню', callback_data=str(EXIT))],
    ])
    update.callback_query.message.edit_text(f'{result}, \nТема: {user.settings.theme},\nОписание: {words.get_description(user.settings.word_number, user.settings.theme)}, \nСлово: {words.get_word(user.settings.word_number, user.settings.theme)} \n Варианты ответов: \n 1. {list[0]} \n 2. {list[1]} \n 3. {list[2] } \n 4. {list[3]} \n  ', reply_markup=keyboard_markup)


    return TEST