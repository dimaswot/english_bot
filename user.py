import json
import os
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import datetime;

class Settings():
    def __init__(self, theme='Crime', word_number=1, count_words=5, sheduller_off=0):
            self.theme = theme
            self.word_number = word_number
            self.count_words = count_words
            self.sheduller_off = sheduller_off

    def serialize(self):
        return {
            "theme": self.theme,
            "word_number":self.word_number,
            "count_words": self.count_words,
            "sheduller_off": self.sheduller_off,
        }

    def deserialize(self, obj: dict):
        if obj is None:
            return False
        self.theme= obj['theme']
        self.word_number = obj['word_number']
        self.count_words = obj['count_words']
        self.sheduller_off = obj['sheduller_off']
        return True

class Statistics():
    def __init__(self, themes=0, count_words=0, last_words=None, last_repetition=None,  words_list: dict = None):
        if words_list is None:
            words_list = {}
        self.themes = themes
        self.count_words = count_words
        self.last_words = last_words
        self.last_repetition = last_repetition
        self.words_list = words_list

    def serialize(self):
        res = {
            "themes": self.themes,
            "count_words": self.count_words,
            "last_words": self.last_words,
            "last_repetition": self.last_repetition,
            "words_list": {},
        }
        for word in self.words_list:
            res["words_list"].setdefault(word, self.words_list[word])
        return res

    def deserialize(self, obj: dict):
        if obj is None:
            return False
        self.themes = obj['themes']
        self.count_words = obj['count_words']
        self.last_words = obj['last_words']
        self.last_repetition = obj['last_repetition']
        self.words_list = {}
        for word in obj['words_list']:
            self.words_list.setdefault(word, obj['words_list'][word])
        return True
class User:
    def __init__(self, user_id=None, settings: Settings = None, statistics: Statistics = None):
        self.user_id = user_id
        self.settings = settings
        self.statistics = statistics


    def refresh(self):
        # Получаем путь до папки с юзерами
        filepath = os.path.sep.join([os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1]), 'data', 'users', f'{self.user_id}.json'])
        # Сохраняем
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(self.serialize(), file, indent=4)


    def check_in_bd(self, user_id: str):
        # Получаем путь до папки с юзерами
        filepath = os.path.sep.join([os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1]), 'data', 'users', f'{user_id}.json'])
        # Загружаем в словарь
        path = Path(filepath)
        obj = None
        if (path.exists() and path.is_file()):
            with open(filepath, 'r', encoding='utf-8') as file:
                obj = json.load(file)

        # Спокойненько десериализуем объект
        success = self.deserialize(obj)
        # Создаем новый если не получилось
        if not success:
            self.user_id = user_id
            self.settings = Settings()
            self.statistics = Statistics()
            self.refresh()
        return success

    def serialize(self):
        settings = None
        if self.settings is not None:
            settings = self.settings.serialize()
        statistics = None
        if self.statistics is not None:
            statistics = self.statistics.serialize()
        return {
            "user_id": self.user_id,
            "settings": settings,
            "statistics": statistics,
        }

    def deserialize(self, obj: dict):
        if obj is None:
            return False
        self.user_id = obj['user_id']

        self.settings = Settings()
        self.settings.deserialize(obj['settings'])

        self.statistics = Statistics()
        self.statistics.deserialize(obj['statistics'])
        return True
