from typing import Callable
from PyQt5.QtCore import QTemporaryFile
from nltk.corpus import wordnet as wn


class ThesaurusWordnet:

    def __init__(
        self
    ):
        self.synonyms = []
        # self.antonyms = []

    def suggestions(self, word: str) -> list[str]:
        self.synonyms = []
        if word is not None:

            print("Check Thesaurus for [" + word + "]")
            # self.antonyms = []
            for syn in wn.synsets(word, lang="eng"):
                for l in syn.lemmas():
                    self.synonyms.append(l.name())
                    # if l.antonyms():
                    #     self.antonyms.append(l.antonyms()[0].name())
            print(set(self.synonyms))
            # print(set(self.antonyms))
        return list(set(self.synonyms))

    # def correction(self, word: str) -> str:
    #     return self.dictionary.suggest(word)[0]

    # def check(self, word: str) -> bool:
    #     return self.dictionary.check(word)
