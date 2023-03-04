import json
import jsonpickle
from sounds.sound import Sound
import os
import logging

SOUNDS = "literary_resources/sounds.json"


class SoundsCollection():
    def __init__(self, resourcePath=""):
        self.__soundList = []
        self.__resourcePath = os.path.join(resourcePath, SOUNDS)

    @property
    def soundList(self):
        return self.__soundList

    @soundList.setter
    def soundList(self, sounds):
        self.__soundList = sounds

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def add(self, word: Sound):
        self.soundList.append(word)

    def save(self):
        # saves the sounds to a file
        with open(self.__resourcePath, "w") as outfile:
            jsonObj = jsonpickle.encode(self.soundList, keys=True)
            outfile.write(jsonObj)

    def load(self):
        # loads the sounds from a file
        # Opening JSON file
        with open(self.__resourcePath, 'r') as infile:
            sounds = infile.read()
            self.soundList = jsonpickle.decode(sounds, keys=True)
        return len(self.soundList)

    def filter_by_tag(self):
        # only return sounds that conform to the filter
        logging.debug("Tag Filtering has not been implemented")

    def dump(self):
        with open('Sound_dump.txt', 'w') as file:
            for aSound in self.__soundList:
                file.write(aSound.sound + " : " + aSound.description + " : ")
                file.write(','.join(aSound.classification))
                file.write(" : ")
                file.write(','.join(aSound.tags))
                file.write("\n")
