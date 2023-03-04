import json
import jsonpickle
from colours.colour import Colour
import os
import logging
COLOURS = "literary_resources/colours.json"


class ColoursCollection():
    def __init__(self, resourcePath):
        self.__colourList = []
        self.__resourcePath = os.path.join(resourcePath, COLOURS)

    @property
    def colourList(self):
        return self.__colourList

    @colourList.setter
    def colourList(self, colours):
        self.__colourList = colours

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def add(self, word: Colour):
        self.colourList.append(word)

    def save(self):
        # saves the colours to a file
        with open(self.__resourcePath, "w") as outfile:
            jsonObj = jsonpickle.encode(self.colourList, keys=True)
            outfile.write(jsonObj)

    def load(self):
        # loads the colours from a file
        # Opening JSON file
        with open(self.__resourcePath, 'r') as infile:
            colours = infile.read()
            self.colourList = jsonpickle.decode(colours, keys=True)
        return len(self.colourList)

    def filter_by_tag(self):
        # only return colours that conform to the filter
        logging.debug("Tag Filtering has not been implemented")

    def dump(self):
        with open('Colour_dump.txt', 'w') as file:
            for aColour in self.__colourList:
                file.write(aColour.colour + " : " + aColour.rgbValue + " : ")
                file.write(','.join(aColour.classification))
                file.write(" : ")
                file.write(','.join(aColour.tags))
                file.write("\n")
