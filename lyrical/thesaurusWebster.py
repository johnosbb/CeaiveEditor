from typing import Callable
from PyQt5.QtCore import QTemporaryFile
from nltk.corpus import wordnet as wn
import json
import requests
import os


class ThesaurusWebster:

    def __init__(
        self
    ):
        self.synonyms = []
        # self.antonyms = []

    # Returns a unique list with any duplicates removed avoiding the reordering a set operation alone might cause
    def unique(self, sequence):
        seen = set()
        return [x for x in sequence if not (x in seen or seen.add(x))]

    def suggestions(self, word: str) -> list[str]:
        """
        Query Webster's Thesaurus API
        :param word: query's word
        :return: definitions, examples, antonyms, synonyms
        """
        synonymsList = []
        if word is not None:
            api_key = os.environ.get('API_KEY')
            word = word.lower()
            if (api_key == "" or (api_key is None)):
                print(
                    "Could not locate the API Key, you will need to register with www.dictionaryapi.com")

            else:
                print("Found an API Key: " + api_key)
            url = f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={api_key}"
            try:
                response = requests.get(url)
                apiResponse = json.loads(response.text)
                # print(apiResponse)
                if response.status_code == 200:
                    try:
                        for data in apiResponse:
                            synonyms = ["sorry, no synonyms are available."]
                            print("data = " + str(data))
                            if word in data["meta"]["id"]:
                                try:
                                    if len(data["meta"]["syns"]) != 0:
                                        synonyms = data["meta"]["syns"][0]
                                        for synonym in synonyms:
                                            synonymsList.append(synonym)
                                except KeyError as e:
                                    print(e)
                    except TypeError as e:
                        print(e)

            except SystemError as error:
                print("Error :" + error)

        # return list(set(synonymsList))
        return self.unique(synonymsList)
