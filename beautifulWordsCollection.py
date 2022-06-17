import json
import jsonpickle

from beautifulWord import BeautifulWord

BEAUTIFUL_WORDS = "literary_resources/beautiful_words.json"


class BeautifulWordsCollection():
    def __init__(self):
        self.__wordList = []

    @property
    def wordList(self):
        return self.__wordList

    @wordList.setter
    def wordList(self, words):
        self.__wordList = words

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def add(self, word: BeautifulWord):
        self.wordList.append(word)

    def save(self):
        # saves the words to a file
        with open(BEAUTIFUL_WORDS, "w") as outfile:
            jsonObj = jsonpickle.encode(self.wordList, keys=True)
            outfile.write(jsonObj)

    def load(self):
        # loads the words from a file
        # Opening JSON file
        with open(BEAUTIFUL_WORDS, 'r') as infile:
            words = infile.read()
            self.wordList = jsonpickle.decode(words, keys=True)
        return len(self.wordList)

    def filter_by_tag(self):
        # only return words that conform to the filter
        print("---")

    def dump(self):
        with open('word_dump.txt', 'w') as file:
            for word in self.__wordList:
                file.write(word.word + " : " + word.meaning + " : ")
                for classification in word.classification:
                    if classification.isspace() is False:
                        file.write(classification + " ")
                file.write(" : ")
                for pos in word.partOfSpeech:
                    if pos.isspace() is False:
                        file.write(pos + " ")
                file.write(" : ")
                for tag in word.tags:
                    if tag.isspace() is False:
                        file.write(tag + " ")
                file.write("\n")
