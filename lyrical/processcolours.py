
from colours.colour import Colour

from colours.coloursCollection import ColoursCollection
# from nltk.corpus import wordnet
import logging

collection = ColoursCollection()
count = 0
with open("literary_resources/colours.txt", "r") as filestream:
    for line in filestream:
        currentline = line.split(":")
        sections = len(currentline)
        if(sections == 3):
            targetColour = currentline[0].strip()
            rgbValue = currentline[1].strip()
            classification = currentline[2].strip()  # this is a list
            if(classification.isspace()):
                classification = ["Unknown Classification"]
            else:
                classification = classification.replace(
                    '\n', '', 1).split(',')

            tags = []
            newColour = Colour(
                targetColour, rgbValue, classification, tags)
            collection.add(newColour)
            count = count + 1
        else:
            logging.debug("processcolours:Error: Not enough or too many fields: " +
                          str(sections) + " to create a word entry for entry " + str(count))
            logging.debug("processcolours: {}".format(currentline))
            break

        if __name__ == '__main__':
            collection.save()
            collection.dump()
            logging.debug("processcolours: Processed " + str(count) + " words")
