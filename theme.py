import json

class Words:
    def __init__(self, filename):
        self.words = None
        with open(filename, 'rt', encoding='utf-8') as f:
            self.words = json.load(f)

    def get_word_count_theme(self, theme):
        word_count = 0
        for w in self.words:
            if theme == w["Theme"]:
                word_count += 1
        return word_count

    def get_translation(self, number, theme):
        for w in self.words:
            if number == w["Number"] and theme == w["Theme"]:
                return w["Translate"]
        return None

    def get_words(self, number, theme):
        for w in self.words:
            if number == w["Number"]  and theme == w["Theme"]:
                return w["List"]
        return None

    def get_word(self, number,theme):
        for w in self.words:
            if number == w["Number"] and theme == w["Theme"]:
                return  w["Word"]
        return None

    def get_description(self, number, theme):
        for w in self.words:
            if number == w["Number"] and theme == w["Theme"]:
                return  w["Description"]
        return None