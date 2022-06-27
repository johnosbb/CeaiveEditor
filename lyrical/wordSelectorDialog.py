

from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QMenu, QAction, QDialog, QSizePolicy,
                             QTableView,  QHeaderView, QLineEdit, QLabel, QFrame, QVBoxLayout, QHBoxLayout, QComboBox)
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QModelIndex, QRegExp, QRect, QSize, QEvent, QPoint
from typing import Callable
import utilities as Utilities
from pprint import pprint
import re

DIALOG_WIDTH = 1000
DIALOG_HEIGHT = 700
IMAGE_WIDTH = DIALOG_WIDTH
IMAGE_HEIGHT = 103
COLUMN_TO_FILTER = 0
SPACER_SIZE = 20
WORD_COLUMN = 0
MEANING_COLUMN = 1
TAG_COLUMN = 2
CLASSIFICATION_COLUMN = 3


headers = ["Word", "Meaning", ""]


class SortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent):
        # the dialog or class that is requesting the filter, in our case the wordSelectorDialog
        self.parentReference = parent
        super().__init__()

    def filterAcceptsRow_orig(self, sourceRow, sourceParent):
        # self.dumpModel(sourceParent)
        # self.dumpRow(sourceParent, sourceRow)
        # self.filterKeyColumn is set by self.proxyModel.setFilterKeyColumn()
        filterKeyColumn = self.filterKeyColumn()
        if filterKeyColumn == self.parentReference.filterColumn:
            index = self.sourceModel().index(
                sourceRow, self.parentReference.filterColumn, sourceParent)
            rawData = self.sourceModel().data(index)
            pattern = repr(self.parentReference.filterString)[1:-1]
            # print("Pattern: " +pattern + ", RawData: " + rawData)
            if((rawData is not None) and (not pattern.isspace()) and (pattern != "")):
                data = rawData.lstrip()
                # Note that the result raw string has the quote at the beginning and end of the string. To remove them, you can use slices: [1:-1]
                if(re.search(pattern, data)):
                    return True
        # Otherwise ignore
        return super(SortFilterProxyModel, self).filterAcceptsRow(sourceRow, sourceParent)

    def checkForPattern(self, sourceRow, sourceParent, pattern, column):
        index = self.sourceModel().index(
            sourceRow, column, sourceParent)
        rawData = self.sourceModel().data(index)

        # print("Pattern: " +pattern + ", RawData: " + rawData)
        if((rawData is not None) and (not pattern.isspace()) and (pattern != "")):
            data = rawData.lstrip()
            # Note that the result raw string has the quote at the beginning and end of the string. To remove them, you can use slices: [1:-1]
            if(re.search(pattern.lower(), data.lower())):
                return True
            else:
                return False
        else:
            return False

    def filterAcceptsRow(self, sourceRow, sourceParent):
        # self.dumpModel(sourceParent)
        # self.dumpRow(sourceParent, sourceRow)
        # self.filterKeyColumn is set by self.proxyModel.setFilterKeyColumn()
        if(self.parentReference.wordFilterEnabled is True):
            wordFilterFound = self.checkForPattern(
                sourceRow, sourceParent, self.parentReference.wordFilterPattern, WORD_COLUMN)
        else:
            wordFilterFound = False
        if(self.parentReference.meaningFilterEnabled is True):
            meaningFilterFound = self.checkForPattern(
                sourceRow, sourceParent, self.parentReference.meaningFilterPattern, MEANING_COLUMN)
        else:
            meaningFilterFound = False
        if(self.parentReference.tagFilterEnabled is True):
            tagFilterFound = self.checkForPattern(
                sourceRow, sourceParent, self.parentReference.tagFilterPattern, TAG_COLUMN)
        else:
            tagFilterFound = False
        if(self.parentReference.classificationFilterEnabled is True):
            classificationFilterFound = self.checkForPattern(
                sourceRow, sourceParent, self.parentReference.classificationFilterPattern, CLASSIFICATION_COLUMN)
        else:
            classificationFilterFound = False
        # filterKeyColumn = self.filterKeyColumn()
        # if filterKeyColumn == self.parentReference.filterColumn:
        includeWordSearchResults = self.parentReference.wordFilterEnabled and wordFilterFound
        if(self.parentReference.wordFilterEnabled is True and wordFilterFound is False):
            includeWordSearchResults = False
        else:
            includeWordSearchResults = True
        includeMeaningSearchResults = self.parentReference.meaningFilterEnabled and meaningFilterFound
        if(self.parentReference.meaningFilterEnabled is True and meaningFilterFound is False):
            includeMeaningSearchResults = False
        else:
            includeMeaningSearchResults = True
        if(self.parentReference.tagFilterEnabled is True and tagFilterFound is False):
            includeTagSearchResults = False
        else:
            includeTagSearchResults = True
        if(self.parentReference.classificationFilterEnabled is True and classificationFilterFound is False):
            includeClassificationSearchResults = False
        else:
            includeClassificationSearchResults = True

        if((includeWordSearchResults is True) and (includeMeaningSearchResults is True) and (includeTagSearchResults is True) and (includeClassificationSearchResults is True)):
            return True
        else:
            return False
        # Otherwise ignore
        # return super(SortFilterProxyModel, self).filterAcceptsRow(sourceRow, sourceParent)

    def dumpModel(self, sourceParent):
        rowCount = self.sourceModel().rowCount()
        columnCount = self.sourceModel().columnCount()
        for row in range(rowCount):
            data = ""
            for column in range(columnCount):
                index = self.sourceModel().index(
                    row, column, sourceParent)
                rawData = self.sourceModel().data(index)
                data = data + str(column) + " : " + rawData
            print(str(row) + " : " + data)

    def dumpRow(self, sourceParent, sourceRow):
        data = ""
        columnCount = self.sourceModel().columnCount()
        for column in range(columnCount):
            index = self.sourceModel().index(
                sourceRow, column, sourceParent)
            rawData = self.sourceModel().data(index)
            data = data + str(column) + " : " + rawData
        print(" Row:" + str(sourceRow) + ", Column Count: " +
              str(columnCount) + "  " + data)


class WordSelectorDialog(QDialog):
    def __init__(self,  title,  parent=None):
        QDialog.__init__(self,  parent)
        self.parent = parent
        self._selectedWord = ""
        # stylesheet = 'QMainWindow { background-image: url("' + ":/images/images/WomanReadingABookLongForm.png" + \
        #     '"); background-repeat: no-repeat; background-position: center; } '
        # self.setStyleSheet(stylesheet)
        self.lastStart = 0
        self.title = title
        self.setWindowIcon(QIcon('beauty.png'))
        self.proxyModel = SortFilterProxyModel(self)
        # This property holds whether the proxy model is dynamically sorted and filtered whenever the contents of the source model change
        self.proxyModel.setDynamicSortFilter(True)
        self.sourceView = QTableView()  # where we store the unfiltered list
        self.tableView = QTableView()
        # self.installEventFilter(self.tableView)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setModel(self.proxyModel)
        self.tableView.setSortingEnabled(True)
        self.setWindowTitle(title)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSortingEnabled(True)
        self.tableView.verticalHeader().hide()
        self.tableView.setSelectionMode(QTableView.SingleSelection)
        self.tableView.setSelectionBehavior(QTableView.SelectRows)
        self.tableView.clicked.connect(self.getItem)
        # self.tableView.doubleClicked.connect(self.selectItem)
        self.filterString = ""
        self.filterColumn = 0
        self.wordFilterEnabled = False
        self.meaningFilterEnabled = False
        self.tagFilterEnabled = False
        self.classificationFilterEnabled = False
        self.initUI()

    def mousePressEvent(self, event):
        '''re-implemented to suppress Right-Clicks from selecting items.'''
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton:
                print("Right button was pressed")
                return
            else:
                super(QDialog, self).mousePressEvent(event)

    def clearFilters(self):
        print("Clearing the filters")
        self.wordFilter.setText("")
        self.meaningFilter.setText("")
        self.classificationFilter.setCurrentIndex(0)
        self.tagFilter.setText("")

    def AddClearFiltersButton(self):
        self.clearFiltersButton = QPushButton('', self)
        self.clearFiltersButton.setStyleSheet("QPushButton { color: rgb(255, 255, 255);\n"
                                              "background-color: rgb(0, 0, 0); }\n"
                                              "QPushButton:pressed { color: rgb(255, 255, 255);\n"
                                              "background-color: rgb(47,79,79); }\n"
                                              "QPushButton { border: none; }")
        self.clearFiltersButton.clicked.connect(self.clearFilters)
        self.clearFiltersButton.setIcon(
            QIcon(":/images/images/clearAll.png"))
        self.clearFiltersButton.setIconSize(QSize(32, 32))
        self.headerLayout.addWidget(self.clearFiltersButton)

    def initUI(self):
        mainLayout = QVBoxLayout()
        self.horizontalLayoutWidget = QWidget(self)
        self.horizontalLayoutWidget.setGeometry(
            QRect(0, 0, DIALOG_WIDTH, IMAGE_HEIGHT))
        self.headerLayout = QHBoxLayout()
        self.headerLayout.setObjectName("self.headerLayout")
        self.headerLayout.setContentsMargins(10, 10, 10, 10)
        headerFrame = QFrame(self.horizontalLayoutWidget)
        headerFrame.setMinimumSize(QSize(DIALOG_WIDTH, IMAGE_HEIGHT))
        headerFrame.setBaseSize(QSize(0, 0))
        headerFrame.setAutoFillBackground(False)
        headerFrame.setObjectName("headerFrame")
        headerFrame.setStyleSheet(
            "QFrame#headerFrame { background-repeat:no-repeat; background-position: left; background-image: url(:/images/images/WomanReadingHeader.png); }")
        headerFrame.setFrameShape(QFrame.StyledPanel)
        headerFrame.setFrameShadow(QFrame.Raised)
        headerFrame.setLayout(self.headerLayout)
        self.headerSpacerWidget = QWidget(headerFrame)
        self.headerSpacerWidget.setObjectName("headerSpacerWidget")
        self.headerSpacerWidget.setGeometry(
            QRect(0, 0, SPACER_SIZE, SPACER_SIZE))
        self.headerSpacerWidget.setObjectName("headerSpacerWidget")
        self.wordFilter = QLineEdit(headerFrame)
        self.wordFilterLabel = QLabel("  Word Filter", headerFrame)
        self.wordFilterLabel.setBuddy(self.wordFilter)
        self.wordFilter.setStyleSheet("color: rgb(0, 0, 0);\n"
                                      "background-color: rgb(255, 255, 255);")
        self.wordFilterLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.wordFilterLabel.setObjectName("wordFilterLabel")
        self.headerLayout.addStretch()
        self.headerLayout.addWidget(self.headerSpacerWidget)
        self.headerLayout.addWidget(self.wordFilterLabel)
        self.headerLayout.addWidget(self.wordFilter)
        # self.headerLayout.addStretch()
        self.wordFilter.setStyleSheet(
            "background-color: #FFFFFF; padding:1px 1px 1px 1px")
        self.wordFilter.setFixedWidth(120)
        # self.wordFilter.returnPressed.connect(self.setWordFilter)
        self.wordFilter.textChanged.connect(self.setWordFilter)
        self.wordFilter.setToolTip(
            "Enter a starting letter or letters to find beautiful words")
        self.meaningFilterLabel = QLabel("  Meaning Filter", headerFrame)
        self.meaningFilter = QLineEdit(headerFrame)
        self.meaningFilter.setStyleSheet("color: rgb(0, 0, 0);\n"
                                         "background-color: rgb(255, 255, 255);")
        self.meaningFilterLabel.setBuddy(self.meaningFilter)
        self.meaningFilterLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.headerLayout.addWidget(self.meaningFilterLabel)
        self.headerLayout.addWidget(self.meaningFilter)
        # self.headerLayout.addStretch()
        self.meaningFilter.setStyleSheet(
            "background-color: #FFFFFF; padding:1px 1px 1px 1px")
        self.meaningFilter.setFixedWidth(120)
        self.meaningFilter.textChanged.connect(self.setMeaningFilter)
        self.meaningFilter.setToolTip(
            "Enter a meaning for which you would like to find a beautiful word")
        self.tagFilterLabel = QLabel(" Tag Filter", headerFrame)
        self.tagFilter = QLineEdit(headerFrame)
        self.tagFilter.setStyleSheet("color: rgb(0, 0, 0);\n"
                                     "background-color: rgb(255, 255, 255);")
        self.tagFilterLabel.setBuddy(self.tagFilter)
        self.tagFilterLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.headerLayout.addWidget(self.tagFilterLabel)
        self.headerLayout.addWidget(self.tagFilter)
        # self.headerLayout.addStretch()
        self.tagFilter.setStyleSheet(
            "background-color: #FFFFFF; padding:1px 1px 1px 1px")
        self.tagFilter.setFixedWidth(120)
        self.tagFilter.textChanged.connect(self.setTagFilter)
        self.tagFilter.setToolTip(
            "Enter a word you like like to find beautiful synonyms for")
        # These classifications need to move into a file that is generated from processing the word list; they should not be hard coded
        classifications = ["All", "Measurement", "Sexuality", "Feelings and Emotions", "Fears", "Colours Tones Shades", "Sounds", "Texture", "Atmosphere", "Interiors, Furnishings", "Exteriors", "Light, Darkness", "Botany", "Olfactory", "Temperament", "Personalities",
                           "Love", "Movement", "Music", "Taste", "Touch", "Beauty", "Art", "Culture", "Speech", "Geography", "Relationships", "Travel", "Sensory ", "Education and Development", "Physicality ", "Shape", "Time", "Spiritual", "Unknown Classification"]
        self.classificationFilterLabel = QLabel(
            " Classification Filter", headerFrame)
        self.classificationFilter = QComboBox(headerFrame)
        self.classificationFilter.setStyleSheet("color: rgb(0, 0, 0);\n"
                                                "background-color: rgb(255, 255, 255);")
        self.classificationFilter.addItems(classifications)
        self.classificationFilterValue = classifications[0]
        self.classificationFilterLabel.setStyleSheet(
            "color: rgb(255, 255, 255);")
        self.tagFilterLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.classificationFilterLabel.setBuddy(self.classificationFilter)
        self.headerLayout.addWidget(self.classificationFilterLabel)
        self.headerLayout.addWidget(self.classificationFilter)
        self.AddClearFiltersButton()
        self.headerLayout.addStretch()
        self.classificationFilter.setStyleSheet(
            "background-color: #FFFFFF; padding:1px 1px 1px 1px")
        self.classificationFilter.setFixedWidth(120)
        self.classificationFilter.currentTextChanged.connect(
            self.setClassificationFilter)
        self.classificationFilter.setToolTip(
            "Select a Classification for which you would like to find beautiful words")
        # self.headerLayout.addSpacing(50)
        # mainLayout.addChildLayout()
        # mainLayout.addLayout(self.headerLayout)
        mainLayout.addWidget(headerFrame)
        mainLayout.addWidget(self.tableView)
        self.setGeometry(300, 300, DIALOG_WIDTH, DIALOG_HEIGHT)
        self.setFixedSize(DIALOG_WIDTH, DIALOG_HEIGHT)
        self.setWindowTitle(self.title)
        self.setLayout(mainLayout)

    def getItem(self, index):
        mapped_index = self.proxyModel.mapToSource(index)
        row = mapped_index.row()
        column = mapped_index.column()
        data = mapped_index.data()
        #print("Row:  " + str(row) + ",Column:  " + str(column) + "  " + data)
        self.selectItem(index)

    def selectItem(self, index):
        mapped_index = self.proxyModel.mapToSource(index)
        row = mapped_index.row()
        column = 0
        data = mapped_index.data()
        self.selectionMenu = QMenu(self)
        selectionAction = self.selectionMenu.addAction(
            'Click to insert this word into your document')
        selectionAction.triggered.connect(lambda: self.showSelection(data))
        x = QCursor.pos().x()
        y = QCursor.pos().y()
        newPosition = QPoint(x+5, y+5)
        self.selectionMenu.exec_(newPosition)

        # self.selectionMenu.installEventFilter(self)
        #print("You selected Data: " + data)

    def showSelection(self, data):
        self.selectedWord = data
        self.accept()
        #print("Selection: " + data)

    # def eventFilter(self, source, event):
    #     if event.type() == QEvent.ContextMenu:
    #         if source == self.tableView:
    #             self.selectionMenu.exec_(event.globalPos())
    #             return True
    #         elif source == self.selectionMenu:
    #             self.subMenu.exec_(event.globalPos())
    #             return True
    #     elif event.type() == QEvent.MouseButtonPress:
    #         if event.button() == Qt.RightButton:
    #             print("Right button clicked")
    #     else:
    #         print("Event: " + str(event.type()) + "  " + str(source))
    #         Utilities.print_attributes(event)
    #     return super().eventFilter(source, event)

    def setWordFilter(self):
        text = self.wordFilter.text()
        if((text is not None) and (not text.isspace()) and (text != "")):
            self.filterString = "^" + text
            self.wordFilterPattern = repr(
                self.filterString)[1:-1]
            self.filterColumn = 0
            self.wordFilterEnabled = True
            self.filterRegExpChanged()
        else:
            self.wordFilterEnabled = False
            self.filterString = ""
            self.wordFilterPattern = repr(
                self.filterString)[1:-1]
            self.filterRegExpChanged()

    def setMeaningFilter(self):
        text = self.meaningFilter.text()
        if((text is not None) and (not text.isspace()) and (text != "")):
            self.meaningFilterPattern = repr(
                text)[1:-1]
            self.filterColumn = 1
            self.meaningFilterEnabled = True
            self.filterRegExpChanged()
        else:
            self.meaningFilterEnabled = False
            self.filterString = ""
            self.meaningFilterPattern = repr(
                self.filterString)[1:-1]
            self.filterRegExpChanged()

    def setTagFilter(self):
        text = self.tagFilter.text()
        if((text is not None) and (not text.isspace()) and (text != "")):
            self.tagFilterPattern = repr(
                text)[1:-1]
            self.filterColumn = 2
            self.tagFilterEnabled = True
            self.filterRegExpChanged()
        else:
            self.tagFilterEnabled = False
            self.filterString = ""
            self.tagFilterPattern = repr(
                self.filterString)[1:-1]
            self.filterRegExpChanged()

    def setClassificationFilter(self, text):
        """
        Change the combo box value . Values represent the different file
         extensions.
        """
        if(text != "All"):
            self.classificationFilterValue = text
            self.filterString = text
            self.classificationFilterPattern = repr(
                text)[1:-1]
            self.classificationFilterEnabled = True
            self.filterColumn = 3
            self.filterRegExpChanged()
        else:
            self.filterString = ""
            self.classificationFilterPattern = repr(
                self.filterString)[1:-1]
            self.filterColumn = 3
            self.classificationFilterEnabled = False
            self.filterRegExpChanged()

    def setSourceModel(self, model):
        # the proxy model points to a source model then we create to hold the actual data
        self.proxyModel.setSourceModel(model)
        self.sourceView.setModel(model)

    def filterRegExpChanged(self):
        syntax = QRegExp.RegExp  # can be one of QRegExp.RegExp2, QRegExp.WildCard, QRegExp.RegExp2 etc, see https://doc.qt.io/qt-5/qregexp.html#PatternSyntax-enum
        caseSensitivity = Qt.CaseInsensitive
        regExp = QRegExp(self.filterString,
                         caseSensitivity, syntax)
        # This property holds the QRegExp used to filter the contents of the source model
        self.proxyModel.setFilterKeyColumn(self.filterColumn)
        self.proxyModel.setFilterRegExp(regExp)

    @ property
    def selectedWord(self):
        return self._selectedWord

    @ selectedWord.setter
    def selectedWord(self, newWord):
        self._selectedWord = newWord
    # Reference: https://doc.qt.io/archives/qtjambi-4.5.2_01/com/trolltech/qt/qtjambi-customfilter.html
