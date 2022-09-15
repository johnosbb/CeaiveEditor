
from sounds.sound import Sound

from sounds.soundsCollections import SoundsCollection

import thesaurusWordnet
from nltk.corpus import wordnet

collection = SoundsCollection()
count = 0
with open("literary_resources/sounds.txt", "r") as filestream:
    for line in filestream:
        currentline = line.split(":")
        sections = len(currentline)
        if(sections == 3):
            targetSound = currentline[0].strip()
            rgbValue = currentline[1].strip()
            classification = currentline[2].strip()  # this is a list
            if(classification.isspace()):
                classification = ["Unknown Classification"]
            else:
                classification = classification.replace(
                    '\n', '', 1).split(',')

            tags = []
            newSound = Sound(
                targetSound, rgbValue, classification, tags)
            collection.add(newSound)
            count = count + 1
        else:
            print(
                "Error: Not enough or too many fields: " + str(sections) + " to create a word entry for entry " + str(count))
            print(currentline)
            break

        if __name__ == '__main__':
            collection.save()
            collection.dump()
            print("Processed " + str(count) + " words")
