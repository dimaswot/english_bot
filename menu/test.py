from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import json
from typing import List

from states import BEGIN, TEST, EXIT
from theme import Words
import random
from datetime import datetime
from user_bd import User, init_user, session, Word, Theme, Statistics

def test_first(update: Update, context: CallbackContext):
    user = init_user(update.callback_query.message.chat_id)
    user.last_repetition = datetime.utcnow()
    user.refresh()

    theme_id = user.theme_id
    current_theme = session.get(Theme, theme_id)
    all_words:List[Word] = []
    new_list = session.query(Statistics).filter((Statistics.count <= user.repeat_word) & (Theme.id == theme_id) & (Statistics.user_id == user.id))
    pustoy = []
    for word in new_list:
        pustoy.append(word.theme_id)
    if pustoy:
        all_words = session.query(Word).filter(Word.id.in_(pustoy)).all()
    random.shuffle(all_words)
    print(f'Получили слова: {len(all_words)}')

    # Номер вопроса
    number = 0
    question_count = int(user.test_count)
    print(f'Количество вопросов: {question_count}')
    current_word = all_words[number]

    # Формируем слова для вопроса
    random.shuffle(all_words)
    if len(all_words) < user.test_count:
        keyboard_markup = InlineKeyboardMarkup([[InlineKeyboardButton(f'Главное меню', callback_data=str(EXIT))]])
        update.callback_query.message.edit_text(f'К сожалению, слова для изучения закончились. Попробуйте вернуться завтра, либо увеличьте повторение слов в настройке.', reply_markup=keyboard_markup)
        return BEGIN
    list = all_words[0:3]

    list.append(current_word)
    print(f'Должно быть 4 слова: {len(list)}')
    random.shuffle(list)

    keyboard_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('1', callback_data=f'@_{number}_{current_word.word}_{list[0].word}_{question_count}_{theme_id}_{0}'),
            InlineKeyboardButton('2', callback_data=f'@_{number}_{current_word.word}_{list[1].word}_{question_count}_{theme_id}_{0}'),
            InlineKeyboardButton('3', callback_data=f'@_{number}_{current_word.word}_{list[2].word}_{question_count}_{theme_id}_{0}'),
            InlineKeyboardButton('4', callback_data=f'@_{number}_{current_word.word}_{list[3].word}_{question_count}_{theme_id}_{0}'),
        ],
        [InlineKeyboardButton('Главное меню', callback_data=str(EXIT))],
    ])
    update.callback_query.message.edit_text(f'Тема: {user.theme_id}, \nПример: {current_word.example} \nСлово: {current_word.word} \n Варианты ответов: \n 1. {list[0].translation} \n 2. {list[1].translation} \n 3. {list[2].translation} \n 4. {list[3].translation} \n  ', reply_markup=keyboard_markup)
    return TEST

def test(update: Update, context: CallbackContext):
    raw_data = update.callback_query.data
    query_data = raw_data.split('_')


    number = int(query_data[1]) + 1
    word = query_data[2]
    word_on_list = query_data[3]
    test_count = query_data[4]
    theme_id = query_data[5]
    result = int(query_data[6])


    user = init_user(update.callback_query.message.chat_id)


    word_model = session.query(Word).where(Word.word == word).one_or_none()

    if word == word_on_list:
        word_statistics = session.query(Statistics).where(
            (Statistics.theme_id == word_model.id) & (Statistics.user_id == user.id)).one_or_none()
        word_statistics.count += 1
        session.add(word_statistics)
        session.commit()
        result += 1
        pass

    else:
        word_statistics = session.query(Statistics).where(
            (Statistics.theme_id == word_model.id) & (Statistics.user_id == user.id)).one_or_none()
        word_statistics.count = 0
        session.add(word_statistics)
        session.commit()

    if number >= int(test_count):
        good = ''
        if result == int(test_count):
            good = 'ОТЛИЧНЫЙ РЕЗУЛЬТАТ\n'
        keyboard_markup = InlineKeyboardMarkup([[InlineKeyboardButton(f'Главное меню', callback_data=str(EXIT))]])
        update.callback_query.message.edit_text(f'{good}Тест заверщен. \n Result: {result} из {test_count}', reply_markup=keyboard_markup)
        return BEGIN
    else:

        current_theme = session.get(Theme, theme_id)

        all_words: List[Word] = []
        new_list = session.query(Statistics).filter(
            (Statistics.count <= user.repeat_word) & (Theme.id == theme_id) & (Statistics.user_id == user.id))
        pustoy = []
        for word in new_list:
            pustoy.append(word.theme_id)
        if pustoy:
            all_words = session.query(Word).filter(Word.id.in_(pustoy)).all()
        random.shuffle(all_words)
        print(f'Получили слова: {len(all_words)}')

        # Выбираем текущее слово и слова для показа
        current_word = all_words[0]
        list = all_words[1:4]
        list.append(current_word)
        random.shuffle(list)

    keyboard_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('1',
                                 callback_data=f'@_{number}_{current_word.word}_{list[0].word}_{test_count}_{theme_id}_{result}'),
            InlineKeyboardButton('2',
                                 callback_data=f'@_{number}_{current_word.word}_{list[1].word}_{test_count}_{theme_id}_{result}'),
            InlineKeyboardButton('3',
                                 callback_data=f'@_{number}_{current_word.word}_{list[2].word}_{test_count}_{theme_id}_{result}'),
            InlineKeyboardButton('4',
                                 callback_data=f'@_{number}_{current_word.word}_{list[3].word}_{test_count}_{theme_id}_{result}'),
        ],
        [InlineKeyboardButton('Главное меню', callback_data=str(EXIT))],
    ])
    update.callback_query.message.edit_text(
        f'Тема: {user.theme_id}, \nПример: {current_word.example} \nСлово: {current_word.word} \n Варианты ответов: \n 1. {list[0].translation} \n 2. {list[1].translation} \n 3. {list[2].translation} \n 4. {list[3].translation} \n  ',
        reply_markup=keyboard_markup)
    return TEST