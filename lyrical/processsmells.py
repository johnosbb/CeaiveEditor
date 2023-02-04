
from smells.smell import Smell

from smells.smellsCollections import SmellsCollection

# from nltk.corpus import wordnet
import logging

collection = SmellsCollection()
count = 0
with open("literary_resources/words_to_describe_smell.txt", "r") as filestream:
    for line in filestream:
        currentline = line.split(":")
        sections = len(currentline)
        if(sections == 3):
            targetSmell = currentline[0].strip()
            description = currentline[1].strip()
            classification = currentline[2].strip()  # this is a list
            if(classification.isspace()):
                classification = ["Unknown Classification"]
            else:
                classification = classification.replace(
                    '\n', '', 1).split(',')

            tags = []
            newSmell = Smell(
                targetSmell, description, classification, tags)
            collection.add(newSmell)
            count = count + 1
        else:
            logging.debug("processsmells: Error: Not enough or too many fields: " +
                          str(sections) + " to create a word entry for entry " + str(count))
            logging.debug("processsmells: {}".format(currentline))
            break

        if __name__ == '__main__':
            collection.save()
            collection.dump()
            logging.debug("processsmells: Processed " + str(count) + " words")
