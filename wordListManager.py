
from PyQt5.QtGui import QIcon, QStandardItemModel

import sys
import beautifulWordsCollection
import beautifulWord

from PyQt5.QtCore import Qt, QSortFilterProxyModel, QModelIndex, QRegExp
from typing import Callable
from wordSelectorDialog import WordSelectorDialog


NUMBER_OF_COLUMNS = 3


class WordListManager:
    def createModel(self, parent):

        beautifulWords = beautifulWordsCollection.BeautifulWordsCollection()
        numberOfRows = beautifulWords.load()
        model = QStandardItemModel(
            numberOfRows, NUMBER_OF_COLUMNS, parent)  # rows columns
        model.setHeaderData(0, Qt.Horizontal, "Word")
        model.setHeaderData(1, Qt.Horizontal, "Meaning")
        for row, word in enumerate(beautifulWords.wordList):
            model.setData(model.index(
                row, 0, QModelIndex()), word.word, Qt.DisplayRole)
            model.setData(model.index(
                row, 1, QModelIndex()), word.meaning, Qt.DisplayRole)
            tags = ""
            for number, tag in enumerate(word.tags):
                tags = tags + " " + tag
            model.setData(model.index(
                row, 2, QModelIndex()), tags, Qt.DisplayRole)
        return model

    def dumpModel(self, model):
        rowCount = model.rowCount()
        columnCount = model.columnCount()
        for row in range(rowCount):
            print(row)

    def createBeautifulWordsList(self, parent):
        wordSelector = WordSelectorDialog("Beautiful Words", parent)
        model = self.createModel(wordSelector)
        wordSelector.setSourceModel(model)
        # self.dumpModel(model)
        wordSelector.show()
