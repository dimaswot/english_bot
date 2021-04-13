from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from datetime import datetime
import json
from states import BEGIN, THEME, TEST, SETTINGS, REDACT_KOL_VO, STOP_SCHEDULLER, STATISTICS, REPIT
from theme import Words
from user_bd import User, init_user, Session, Word, Theme, Statistics
from typing import List

def start(update: Update, context: CallbackContext):
    session = Session()
    user = init_user(update.message.chat_id)
    user.first_name = update.message.chat.first_name
    user.telegram_id = update.message.chat.id
    user.refresh()

    session.query(Statistics).filter(Statistics.user_id == user.id).delete()
    theme_id = user.theme_id
    all_words = session.query(Word).all()
    for word in all_words:
        word_statistics = Statistics()
        word_statistics.theme_id = word.id
        word_statistics.count = 0
        word_statistics.user_id = user.id
        session.add(word_statistics)
        session.commit()

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

def shed(update, user:User):
    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Повторить', callback_data=str(REPIT))],
    ])
    update.send_message(user.telegram_id, 'Пора бы наверное и повторить', reply_markup=keyboard_markup)
    return BEGIN
