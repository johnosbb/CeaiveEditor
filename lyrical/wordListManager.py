
from PyQt5.QtGui import QIcon, QStandardItemModel

import sys
from beautifulwords.beautifulWordsCollection import BeautifulWordsCollection
from beautifulwords.beautifulWord import BeautifulWord

# import beautifulWordsCollection
# import beautifulWord
#import beautifulWord

from PyQt5.QtCore import Qt, QSortFilterProxyModel, QModelIndex, QRegExp
from typing import Callable
from wordSelectorDialog import WordSelectorDialog


NUMBER_OF_COLUMNS = 4


class WordListManager:
    def createBeautifulWordsModel(self, parent):
        aBeautifulWordsCollection = BeautifulWordsCollection()
        numberOfRows = aBeautifulWordsCollection.load()
        model = QStandardItemModel(
            numberOfRows, NUMBER_OF_COLUMNS, parent)  # rows columns
        model.setHeaderData(0, Qt.Horizontal, "Word")
        model.setHeaderData(1, Qt.Horizontal, "Meaning")
        model.setHeaderData(2, Qt.Horizontal, "Tags")
        model.setHeaderData(3, Qt.Horizontal, "Classification")
        for row, word in enumerate(aBeautifulWordsCollection.wordList):
            model.setData(model.index(
                row, 0, QModelIndex()), word.word, Qt.DisplayRole)
            model.setData(model.index(
                row, 1, QModelIndex()), word.meaning, Qt.DisplayRole)
            tags = ""
            for number, tag in enumerate(word.tags):
                tags = tags + " " + tag
            model.setData(model.index(
                row, 2, QModelIndex()), tags, Qt.DisplayRole)
            classifications = ""
            for number, classification in enumerate(word.classification):
                classifications = classifications + " " + classification
            model.setData(model.index(
                row, 3, QModelIndex()), classifications, Qt.DisplayRole)
        return model

    def dumpModel(self, model):
        rowCount = model.rowCount()
        for row in range(rowCount):
            self.dumpRow(model, row)

    def dumpRow(self, model, sourceRow):
        data = ""
        columnCount = model.columnCount()
        for column in range(columnCount):
            index = model.index(
                sourceRow, column, QModelIndex())
            rawData = model.data(index)
            data = data + str(column) + " : " + rawData
        print(" Row:" + str(sourceRow) + ", Column Count: " +
              str(columnCount) + "  " + data)

    def createBeautifulWordsList(self, parent):
        classifications = ["All", "Measurement", "Sexuality", "Feelings and Emotions", "Fears", "Colours Tones Shades", "Sounds", "Texture", "Atmosphere", "Interiors, Furnishings", "Exteriors", "Light, Darkness", "Botany", "Olfactory", "Temperament", "Personalities",
                           "Love", "Movement", "Music", "Taste", "Touch", "Beauty", "Art", "Culture", "Speech", "Geography", "Relationships", "Travel", "Sensory ", "Education and Development", "Physicality ", "Shape", "Time", "Spiritual", "Unknown Classification"]
        wordSelector = WordSelectorDialog(
            "Beautiful Words", classifications, parent)
        model = self.createBeautifulWordsModel(wordSelector)
        wordSelector.setSourceModel(model)
        if wordSelector.exec():
            print("Word selected was " +
                  wordSelector.selectedWord)
            parent.editor.insert_selected_word(wordSelector.selectedWord)
        else:
            print("Canceled! Beautiful Words Dialog {}".format(
                wordSelector.selectedWord))
