from typing import Callable
from spellchecker import SpellChecker
from PyQt5.QtCore import QTemporaryFile


class SpellCheckWord:
    def __init__(
        self, personal_word_list: list[str], addToDictionary: Callable[[str], None]
    ):
        # Creating temporary file
        self.file = QTemporaryFile()
        self.file.open()
 # DictWithPWL() is an inbuilt method of enchant module. It is used to combine a language dictionary and a custom dictionary also known as Personal Word List(PSL).
        self.dictionary = SpellChecker()

        self.addToDictionary = addToDictionary
        self.word_list = set(personal_word_list)
        self.load_words()  # we can load a customised dictionary

    def load_words(self):
        for word in self.word_list:
            self.dictionary.word_frequency.add(word)

    def suggestions(self, word: str) -> list[str]:
        if word is not None:
            candidates_s = self.dictionary.candidates(word)
            if(candidates_s):
                candidates = list(candidates_s)
                candidates.insert(0, self.correction(word))
                return candidates
            else:
                return []
        else:
            return []

    def correction(self, word: str) -> str:
        return self.dictionary.correction(word)

    def add(self, new_word: str) -> bool:
        if self.check(new_word):
            return False
        self.word_list.add(new_word)
        self.addToDictionary(new_word)
        self.dictionary.word_frequency.add(new_word)
        return True

    def check(self, word: str) -> bool:
        if(word is not None):
            result = self.dictionary.known([word])
            if len(result):
                return True
        else:
            return False

    # sets are unordered, has no duplicates and its items are unchangeable
    def getNewWords(self) -> set[str]:
        return self.word_list
