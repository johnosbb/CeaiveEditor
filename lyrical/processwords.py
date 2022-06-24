
from beautifulwords.beautifulWord import BeautifulWord

from beautifulwords.beautifulWordsCollection import BeautifulWordsCollection

import thesaurusWordnet
from nltk.corpus import wordnet


def find_tags(target):
    thesaurus = thesaurusWordnet.ThesaurusWordnet()
    tags = thesaurus.suggestions(target)
    return tags


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


collection = BeautifulWordsCollection()
count = 0
with open("literary_resources/words.txt", "r") as filestream:
    for line in filestream:
        currentline = line.split(":")
        sections = len(currentline)
        # total = str(int(currentline[0]) + int(currentline[1]) + int(currentline [2])) + "\n"
        if(sections == 3):
            targetWord = currentline[0].strip()
            meaning = currentline[1]
            classification = currentline[2]  # this is a list
            if(classification.isspace()):
                classification = ["Unknown Classification"]
            pos = find_all_pos_for_word(targetWord)
            tags = find_tags(targetWord)
            newWord = BeautifulWord(
                targetWord, meaning, pos, classification, tags)
            collection.add(newWord)
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
