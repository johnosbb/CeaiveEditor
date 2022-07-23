
from colourDescriptors.colourDescriptor import ColourDescriptor

from colourDescriptors.colourDescriptorsCollection import DescriptorsCollection

import thesaurusWordnet
from nltk.corpus import wordnet

collection = DescriptorsCollection()
count = 0
with open("literary_resources/words_to_describe_colour.txt", "r") as filestream:
    for line in filestream:
        currentLine = line.split(":")
        sections = len(currentLine)
        if(sections == 3):
            targetDescriptor = currentLine[0].strip()
            targetDescriptorDescription = currentLine[1].strip()
            classification = currentLine[2].strip()  # this is a list
            if(classification.isspace()):
                classification = ["Unknown Classification"]
            else:
                classification = classification.replace(
                    '\n', '', 1).split(',')

            tags = []
            newDescriptor = ColourDescriptor(
                targetDescriptor, targetDescriptorDescription, classification, tags)
            collection.add(newDescriptor)
            count = count + 1
        else:
            print(
                "Error: Not enough or too many fields: " + str(sections) + " to create a word entry for entry " + str(count))
            print(currentLine)
            break

        if __name__ == '__main__':
            collection.save()
            collection.dump()
            print("Processed " + str(count) + " words")
