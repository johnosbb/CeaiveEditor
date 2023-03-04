import json
import jsonpickle
from smells.smell import Smell
import logging
import os

SMELLS = "literary_resources/smells.json"


class SmellsCollection():
    def __init__(self, resourcePath=""):
        self.__smellList = []
        self.__resourcePath = os.path.join(resourcePath, SMELLS)

    @property
    def smellList(self):
        return self.__smellList

    @smellList.setter
    def smellList(self, smells):
        self.__smellList = smells

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def add(self, word: Smell):
        self.smellList.append(word)

    def save(self):
        # saves the smells to a file
        with open(self.__resourcePath, "w") as outfile:
            jsonObj = jsonpickle.encode(self.smellList, keys=True)
            outfile.write(jsonObj)

    def load(self):
        # loads the smells from a file
        # Opening JSON file
        with open(self.__resourcePath, 'r') as infile:
            smells = infile.read()
            self.smellList = jsonpickle.decode(smells, keys=True)
        return len(self.smellList)

    def filter_by_tag(self):
        # only return smells that conform to the filter
        logging.debug("Tag Filtering has not been implemented")

    def dump(self):
        with open('Smell_dump.txt', 'w') as file:
            for aSmell in self.__smellList:
                file.write(aSmell.smell + " : ")
                file.write(','.join(aSmell.description))
                file.write(" : ")
                file.write(','.join(aSmell.classification))
                file.write(" : ")
                file.write(','.join(aSmell.tags))
                file.write("\n")
