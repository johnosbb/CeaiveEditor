
from PyQt5.QtGui import QStandardItemModel, QBrush, QColor

import sys
from beautifulwords.beautifulWordsCollection import BeautifulWordsCollection
from touchDescriptors.touchWord import TouchWord
from touchDescriptors.touchWordsCollection import TouchWordsCollection

from colours.coloursCollection import ColoursCollection
from colourDescriptors.colourDescriptorsCollection import DescriptorsCollection
from colourDescriptors.colourDescriptorsCollection import DescriptorsCollection
from colours.colour import Colour

from smells.smellsCollections import SmellsCollection
from sounds.soundsCollections import SoundsCollection
import logging

# import beautifulWordsCollection
# import beautifulWord
#import beautifulWord

from PyQt5.QtCore import Qt, QModelIndex

from beautifulWordSelectorDialog import BeautifulWordSelectorDialog
from colorSelectorDialog import WordForColorSelectorDialog
from colorDescriptorSelectorDialog import WordForColorDescriptorsSelectorDialog
from touchDescriptorSelectorDialog import WordForTouchDescriptorsSelectorDialog
from smellSelectorDialog import WordsForSmellSelectorDialog
from soundSelectorDialog import WordsForSoundSelectorDialog

NUMBER_OF_BW_COLUMNS = 2
NUMBER_OF_WFC_COLUMNS = 3
NUMBER_OF_WFS_COLUMNS = 3
NUMBER_OF_SMELL_COLUMNS = 3
NUMBER_OF_SOUND_COLUMNS = 3


class WordListManager:
    def createBeautifulWordsModel(self, parent):
        aBeautifulWordsCollection = BeautifulWordsCollection()
        numberOfRows = aBeautifulWordsCollection.load()
        model = QStandardItemModel(
            numberOfRows, NUMBER_OF_BW_COLUMNS, parent)  # rows columns
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

    def createWordsForSmellModel(self, parent):
        aSmellWordsCollection = SmellsCollection()
        numberOfRows = aSmellWordsCollection.load()
        model = QStandardItemModel(
            numberOfRows, NUMBER_OF_SMELL_COLUMNS, parent)  # rows columns
        model.setHeaderData(0, Qt.Horizontal, "Smell")
        model.setHeaderData(1, Qt.Horizontal, "Description")
        model.setHeaderData(2, Qt.Horizontal, "Classification")
        for row, smell in enumerate(aSmellWordsCollection.smellList):
            model.setData(model.index(
                row, 0, QModelIndex()), smell.smell, Qt.DisplayRole)
            model.setData(model.index(
                row, 1, QModelIndex()), smell.description, Qt.DisplayRole)
            classifications = ""
            for number, classification in enumerate(smell.classification):
                classifications = classifications + " " + classification
            model.setData(model.index(
                row, 2, QModelIndex()), classifications, Qt.DisplayRole)
        return model

    def createWordsForSoundModel(self, parent):
        aSoundsCollection = SoundsCollection()
        numberOfRows = aSoundsCollection.load()
        model = QStandardItemModel(
            numberOfRows, NUMBER_OF_SOUND_COLUMNS, parent)  # rows columns
        model.setHeaderData(0, Qt.Horizontal, "Sound")
        model.setHeaderData(1, Qt.Horizontal, "Description")
        #model.setHeaderData(2, Qt.Horizontal, "Tags")
        model.setHeaderData(2, Qt.Horizontal, "Classification")
        for row, sound in enumerate(aSoundsCollection.soundList):
            model.setData(model.index(
                row, 0, QModelIndex()), sound.sound, Qt.DisplayRole)
            classifications = ""
            model.setData(model.index(
                row, 1, QModelIndex()), sound.description, Qt.DisplayRole)
            for number, classification in enumerate(sound.classification):
                classifications = classifications + " " + classification
            model.setData(model.index(
                row, 2, QModelIndex()), classifications, Qt.DisplayRole)
        return model

    def createWordsForColourModel(self, parent):
        aColoursCollection = ColoursCollection()
        numberOfRows = aColoursCollection.load()
        model = QStandardItemModel(
            numberOfRows, NUMBER_OF_WFC_COLUMNS, parent)  # rows columns
        model.setHeaderData(0, Qt.Horizontal, "Colour")
        model.setHeaderData(1, Qt.Horizontal, "Swatch")
        #model.setHeaderData(2, Qt.Horizontal, "Tags")
        model.setHeaderData(2, Qt.Horizontal, "Classification")
        for row, colour in enumerate(aColoursCollection.colourList):
            model.setData(model.index(
                row, 0, QModelIndex()), colour.colour, Qt.DisplayRole)

            model.setData(model.index(
                row, 1, QModelIndex()), "                                                                                 ", Qt.DisplayRole)
            model.setData(model.index(
                row, 1, QModelIndex()), QBrush(
                QColor(colour.rgbValue)), Qt.BackgroundRole)
            classifications = ""
            for number, classification in enumerate(colour.classification):
                classifications = classifications + " " + classification
            model.setData(model.index(
                row, 2, QModelIndex()), classifications, Qt.DisplayRole)
        return model

    def createWordsForTouchDescriptorsModel(self, parent):
        aTouchCollection = TouchWordsCollection()
        numberOfRows = aTouchCollection.load()
        model = QStandardItemModel(
            numberOfRows, NUMBER_OF_WFC_COLUMNS, parent)  # rows columns
        model.setHeaderData(0, Qt.Horizontal, "Touch Descriptor")
        model.setHeaderData(1, Qt.Horizontal, "Description")
        #model.setHeaderData(2, Qt.Horizontal, "Tags")
        model.setHeaderData(2, Qt.Horizontal, "Classification")
        for row, descriptor in enumerate(aTouchCollection.wordList):
            model.setData(model.index(
                row, 0, QModelIndex()), descriptor.word, Qt.DisplayRole)

            model.setData(model.index(
                row, 1, QModelIndex()), descriptor.meaning, Qt.DisplayRole)
            classifications = ""
            for number, classification in enumerate(descriptor.classification):
                classifications = classifications + " " + classification
            model.setData(model.index(
                row, 2, QModelIndex()), classifications, Qt.DisplayRole)
        return model

    def createWordsForColourDescriptorsModel(self, parent):
        aDescriptorsCollection = DescriptorsCollection()
        numberOfRows = aDescriptorsCollection.load()
        model = QStandardItemModel(
            numberOfRows, NUMBER_OF_WFC_COLUMNS, parent)  # rows columns
        model.setHeaderData(0, Qt.Horizontal, "Colour Descriptor")
        model.setHeaderData(1, Qt.Horizontal, "Description")
        #model.setHeaderData(2, Qt.Horizontal, "Tags")
        model.setHeaderData(2, Qt.Horizontal, "Classification")
        for row, descriptor in enumerate(aDescriptorsCollection.descriptorList):
            model.setData(model.index(
                row, 0, QModelIndex()), descriptor.descriptor, Qt.DisplayRole)

            model.setData(model.index(
                row, 1, QModelIndex()), descriptor.description, Qt.DisplayRole)
            classifications = ""
            for number, classification in enumerate(descriptor.classification):
                classifications = classifications + " " + classification
            model.setData(model.index(
                row, 2, QModelIndex()), classifications, Qt.DisplayRole)
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
        classifications = ["All", "Measurement", "Sexuality", "Feelings and Emotions", "Inspiration", "Fears", "Colours Tones Shades", "Sounds", "Texture", "Atmosphere", "Interiors", "Furnishings", "Exteriors", "Light, Darkness", "Botany", "Olfactory", "Temperament", "Transformation", "Personalities",
                           "Love", "Movement", "Music", "Taste", "Touch", "Beauty", "Art", "Culture", "Speech", "Geography", "Relationships", "Travel", "Sensory ", "Education and Development", "Physicality ", "Rhythms", "Shape", "Time", "Spiritual", "Unknown Classification", "Garments"]
        wordSelector = BeautifulWordSelectorDialog(
            "Beautiful Words", classifications, parent)
        model = self.createBeautifulWordsModel(wordSelector)
        wordSelector.setSourceModel(model)
        if wordSelector.exec():
            logging.debug("Word selected was " +
                          wordSelector.selectedWord)
            parent.editor.insertSelectedWord(wordSelector.selectedWord)
        else:
            logging.debug("Canceled! Beautiful Words Dialog {}".format(
                wordSelector.selectedWord))

    def createWordsForSmellList(self, parent):
        classifications = ["All", "General words for smell", "Unpleasant Smells",
                           "Pleasant Smells", "Words that smell like something"]
        wordSelector = WordsForSmellSelectorDialog(
            "Words For Smell", classifications, parent)
        model = self.createWordsForSmellModel(wordSelector)
        wordSelector.setSourceModel(model)
        if wordSelector.exec():
            logging.debug("Smell selected was " +
                          wordSelector.selectedWord)
            parent.editor.insertSelectedWord(wordSelector.selectedWord)
        else:
            logging.debug("Canceled! Words for Smell Dialog {}".format(
                wordSelector.selectedWord))

    def createWordsForSoundList(self, parent):
        classifications = ["All", "General Words Describing Sounds", "Unpleasant Sounds",
                           "Pleasant Sounds", "Neutral Sound", "Noisy Sounds"]
        wordSelector = WordsForSoundSelectorDialog(
            "Words For Sound", classifications, parent)
        model = self.createWordsForSoundModel(wordSelector)
        wordSelector.setSourceModel(model)
        if wordSelector.exec():
            logging.debug("Sound selected was " +
                          wordSelector.selectedWord)
            parent.editor.insertSelectedWord(wordSelector.selectedWord)
        else:
            logging.debug("Canceled! Words for Sound Dialog {}".format(
                wordSelector.selectedWord))

    def createWordsForColorList(self, parent):
        classifications = ["All", "Red", "Blue", "Yellow", "Pink", "Orange",
                           "Green", "White", "Brown", "Black", "Grey", "Gray", "Silver", "Gold"]
        wordSelector = WordForColorSelectorDialog(
            "Words For Color", classifications, parent)
        model = self.createWordsForColourModel(wordSelector)
        wordSelector.setSourceModel(model)
        if wordSelector.exec():
            logging.debug("Colour selected was " +
                          wordSelector.selectedWord)
            parent.editor.insertSelectedWord(wordSelector.selectedWord)
        else:
            logging.debug("Canceled! Words for Colour Dialog {}".format(
                wordSelector.selectedWord))

    def createWordsForColorDescriptorsList(self, parent):
        classifications = ["All", "Qualify Colour", "Qualify Lack of Colour"]
        wordSelector = WordForColorDescriptorsSelectorDialog(
            "Words For Color Descriptors", classifications, parent)
        model = self.createWordsForColourDescriptorsModel(wordSelector)
        wordSelector.setSourceModel(model)
        if wordSelector.exec():
            logging.debug("Descriptor selected was " +
                          wordSelector.selectedWord)
            parent.editor.insertSelectedWord(wordSelector.selectedWord)
        else:
            logging.debug("Canceled! Colour Descriptor Words Dialog {}".format(
                wordSelector.selectedWord))

    def createWordsForTouchDescriptorsList(self, parent):
        classifications = ["All", "Sensations", "Surfaces", "Textures",
                           "Materials", "General words for touch", "Size"]
        wordSelector = WordForTouchDescriptorsSelectorDialog(
            "Words For Touch Descriptors", classifications, parent)
        model = self.createWordsForTouchDescriptorsModel(wordSelector)
        wordSelector.setSourceModel(model)
        if wordSelector.exec():
            logging.debug("Descriptor selected was " +
                          wordSelector.selectedWord)
            parent.editor.insertSelectedWord(wordSelector.selectedWord)
        else:
            logging.debug("Canceled! Touch Descriptor Words Dialog {}".format(
                wordSelector.selectedWord))
