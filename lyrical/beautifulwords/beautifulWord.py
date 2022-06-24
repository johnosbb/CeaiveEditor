import json


class BeautifulWord():
    def __init__(self, word, meaning, pos=[], wordClass=[], tags=[]):
        self.__word = word
        self.__meaning = meaning
        self.__tags = tags
        self.__partOfSpeech = pos
        self.__classification = wordClass

    # def toJSON(self):
    #     return json.dumps(self, default=lambda o: o.__dict__,
    #                       sort_keys=True, indent=4)


    @property
    def partOfSpeech(self):
        return self.__partOfSpeech

    @partOfSpeech.setter
    def partOfSpeech(self, pos):
        self.__partOfSpeech = pos
        
    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags(self, wordClass):
        self.__tags = wordClass 
    
    @property
    def classification(self):
        return self.__classification

    @classification.setter
    def classification(self, wordClass):
        self.__classification = wordClass    
        
    @property
    def word(self):
        return self.__word

    @word.setter
    def word(self, word):
        self.__word = word
        
    @property
    def meaning(self):
        return self.__meaning

    @meaning.setter
    def meaning(self, meaning):
        self.__meaning = meaning
        
    def __str__(self):
        return f'{self.word} : {self.meaning}'

    def __repr__(self):
        return f'BeautifulWord(word={self.word}, meaning={self.meaning}, tags=[{",".join([(str(item)) for item in self.tags])}])'
    