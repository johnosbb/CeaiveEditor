
from touchDescriptors.touchWord import TouchWord

from touchDescriptors.touchWordsCollection import TouchWordsCollection

import thesaurusWordnet
from nltk.corpus import wordnet


def find_tags(target):
    thesaurus = thesaurusWordnet.ThesaurusWordnet()
    tags = thesaurus.suggestions(target)
    return tags


def find_meaning(target):
    synonyms = wordnet.synsets(target)
    if synonyms:
        return (synonyms[0].definition())
    else:
        return ""


def find_all_synonyms_for_word(target):

    synonyms = wordnet.synsets(target)
    allSynSet = set()
    for synset in synonyms:
        word = synset.name().split('.')[0]
        allSynSet.add(word)
    return list(allSynSet)


def find_all_pos_for_word(target):
    wordnet_tag_map = {
        'n': 'Noun',
        's': 'Adjective',
        'a': 'Adjective',
        'r': 'Adverb',
        'v': 'Verb'
    }
    synonyms = wordnet.synsets(target)
    partsOfSpeech = set()
    for synset in synonyms:
        fullName = synset.name().strip()
        pos = synset.pos().strip()
        partOfSpeech = wordnet_tag_map.get(synset.pos()).strip()
        word = synset.name().split('.')[0]
        if(word == target.lower()):
            partsOfSpeech.add(partOfSpeech)
    return list(partsOfSpeech)


collection = TouchWordsCollection()
count = 0
with open("literary_resources/words_for_touch.txt", "r") as filestream:
    for line in filestream:
        currentline = line.split(":")
        sections = len(currentline)
        # total = str(int(currentline[0]) + int(currentline[1]) + int(currentline [2])) + "\n"
        if(sections == 2):
            targetWord = currentline[0].strip()
            meaning = find_meaning(targetWord)
            classification = currentline[1]  # this is a list
            if(classification.isspace()):
                classification = ["Unknown Classification"]
            else:
                classification = classification.replace(
                    '\n', '', 1).split(',')
                #classification = classification.split(",")
            pos = find_all_pos_for_word(targetWord)
            tags = find_tags(targetWord)
            newWord = TouchWord(
                targetWord, meaning, pos, classification, tags)
            collection.add(newWord)
            count = count + 1
        else:
            print(
                "Error: Not enough or too many fields: [" + str(sections) + "] to create a touch record for entry: " + str(count) + " " + line)
            print(currentline)
            break

        if __name__ == '__main__':
            collection.save()
            collection.dump()
            print("Processed " + str(count) + " words")
