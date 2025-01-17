import json
import jsonpickle
import logging
from touchDescriptors.touchWord import TouchWord
import os

TOUCH_WORDS = "literary_resources/touch_words.json"


class TouchWordsCollection():
    def __init__(self, resourcePath=""):
        self.__wordList = []
        self.__resourcePath = os.path.join(resourcePath, TOUCH_WORDS)

    @property
    def wordList(self):
        return self.__wordList

    @wordList.setter
    def wordList(self, words):
        self.__wordList = words

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def add(self, word: TouchWord):
        self.wordList.append(word)

    def save(self):
        # saves the words to a file
        with open(self.__resourcePath, "w") as outfile:
            jsonObj = jsonpickle.encode(self.wordList, keys=True)
            outfile.write(jsonObj)

    def load(self):
        # loads the words from a file
        # Opening JSON file
        with open(self.__resourcePath, 'r') as infile:
            words = infile.read()
            self.wordList = jsonpickle.decode(words, keys=True)
        return len(self.wordList)

    def filter_by_tag(self):
        # only return words that conform to the filter
        logging.debug("Tag Filtering has not been implemented")

    def dump(self):
        with open('word_dump.txt', 'w') as file:
            for word in self.__wordList:
                file.write(word.word + " : " + word.meaning + " : ")
                # for classification in word.classification:
                #     if classification.isspace() is False:
                #         file.write(classification + " ")
                file.write(','.join(word.classification))
                file.write(" : ")
                file.write(','.join(word.partOfSpeech))
                # for pos in word.partOfSpeech:
                #     if pos.isspace() is False:
                #         file.write(pos + " ")
                file.write(" : ")
                file.write(','.join(word.tags))
                # for tag in word.tags:
                #     if tag.isspace() is False:
                #         file.write(tag + ",")
                file.write("\n")
