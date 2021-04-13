from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from menu import start
from states import BEGIN, THEME, TEST, SETTINGS, REDACT_KOL_VO, STOP_SCHEDULLER, STATISTICS, EXIT
from user_bd import User, init_user, session, Word, Theme

def settings(update: Update, context: CallbackContext):
    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Выбор темы', callback_data=str(THEME))],
        [InlineKeyboardButton('Изменение повторенией слов', callback_data=str(REDACT_KOL_VO))],
        [InlineKeyboardButton('Выбрать количество слов в тесте', callback_data=str(STOP_SCHEDULLER))],
        [InlineKeyboardButton('Назад', callback_data=str(EXIT))],
    ])
    update.callback_query.message.edit_text('Настройки: ', reply_markup=keyboard_markup)
    return SETTINGS

def redact_kol_vo(update: Update, context: CallbackContext):
    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('3', callback_data='3')],
        [InlineKeyboardButton('6', callback_data='6')],
        [InlineKeyboardButton('9', callback_data='9')],
        [InlineKeyboardButton('Назад', callback_data=str(EXIT))],
    ])
    update.callback_query.message.edit_text('Изменить кол-во повторений одного слова: ', reply_markup=keyboard_markup)
    return REDACT_KOL_VO


def test_count(update: Update, context: CallbackContext):
    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('5', callback_data=5)],
        [InlineKeyboardButton('10', callback_data=10)],
        [InlineKeyboardButton('Назад', callback_data=str(EXIT))],

    ])
    update.callback_query.message.edit_text('Выберите колиество вопросов в тесте? ', reply_markup=keyboard_markup)
    return STOP_SCHEDULLER


def theme(update: Update, context: CallbackContext):
    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Crime', callback_data='Crime')],
        [InlineKeyboardButton('Kitchen', callback_data='Kitchen')],
        [InlineKeyboardButton('Назад', callback_data=str(EXIT))],

    ])
    update.callback_query.message.edit_text('Выберите тему, которую хотите изучить?', reply_markup=keyboard_markup)
    return THEME


def set_theme(update: Update, context: CallbackContext):
    user = init_user(update.callback_query.message.chat_id)
    user.theme = update.callback_query.data
    user.refresh()
    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Главное меню', callback_data=str(EXIT))],
    ])
    update.callback_query.message.edit_text(f'Выбрана тема {update.callback_query.data}', reply_markup=keyboard_markup)
    return BEGIN

def set_test_count(update: Update, context: CallbackContext):
    user = init_user(update.callback_query.message.chat_id)
    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Главное меню', callback_data=str(EXIT))],
    ])
    user.test_count = int(update.callback_query.data)
    user.refresh()
    update.callback_query.message.edit_text(f'Установлено количество вопросов в тесте:  {update.callback_query.data}', reply_markup=keyboard_markup)
    return BEGIN


def set_kol_vo(update: Update, context: CallbackContext):
    user = init_user(update.callback_query.message.chat_id)
    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Главное меню', callback_data=str(EXIT))],
    ])
    user.count_words = int(update.callback_query.data)
    user.refresh()
    update.callback_query.message.edit_text(f'Установлено количество {update.callback_query.data}: ', reply_markup=keyboard_markup)
    return BEGIN