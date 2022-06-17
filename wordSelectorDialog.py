

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QTableWidget, QTableWidgetItem, QMenu, QAction, QDialog, QSizePolicy,
                             QInputDialog, QTableView,  QHeaderView, QLineEdit, QLabel, QFrame, QVBoxLayout, QHBoxLayout, QComboBox)
from PyQt5.QtGui import QIcon, QStandardItemModel
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QModelIndex, QRegExp, QRect, QSize
from typing import Callable
import imageBox
import re

DIALOG_WIDTH = 1000
DIALOG_HEIGHT = 700
IMAGE_WIDTH = DIALOG_WIDTH
IMAGE_HEIGHT = 103
COLUMN_TO_FILTER = 0
SPACER_SIZE = 20


headers = ["Word", "Meaning", ""]


class SortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent):
        self.parentReference = parent
        super().__init__()

    def filterAcceptsRow(self, sourceRow, sourceParent):
        # self.dumpModel(sourceParent)
        filterKeyColumn = self.filterKeyColumn()
        if filterKeyColumn == self.parentReference.filterColumn:
            index = self.sourceModel().index(
                sourceRow, self.parentReference.filterColumn, sourceParent)
            rawData = self.sourceModel().data(index)
            pattern = repr(self.parentReference.filterString)[1:-1]
            #print("Pattern: " +pattern + ", RawData: " + rawData)
            if((rawData is not None) and (not pattern.isspace()) and (pattern != "")):
                data = rawData.lstrip()
                # Note that the result raw string has the quote at the beginning and end of the string. To remove them, you can use slices: [1:-1]

                # print(data)
                if(re.search(pattern, data)):
                    return True
        # Otherwise ignore
        return super(SortFilterProxyModel, self).filterAcceptsRow(sourceRow, sourceParent)

    def dumpModel(self):
        rowCount = self.sourceModel().rowCount()
        columnCount = self.sourceModel().columnCount()
        for row in range(rowCount):
            print(row)


class WordSelectorDialog(QDialog):
    def __init__(self,  title,  parent=None):
        QDialog.__init__(self,  parent)
        self.parent = parent
        # stylesheet = 'QMainWindow { background-image: url("' + ":/images/images/WomanReadingABookLongForm.png" + \
        #     '"); background-repeat: no-repeat; background-position: center; } '
        # self.setStyleSheet(stylesheet)
        self.lastStart = 0
        self.title = title
        self.proxyModel = SortFilterProxyModel(self)
        # This property holds whether the proxy model is dynamically sorted and filtered whenever the contents of the source model change
        self.proxyModel.setDynamicSortFilter(True)
        self.sourceView = QTableView()  # where we store the unfiltered list
        self.tableView = QTableView()
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
        self.filterString = ""
        self.filterColumn = 0
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()
        # headerImage = ":/images/images/WomanReadingHeader.png"
        # self.headerImageBox = imageBox.ImageBox(
        #     headerImage, 0, 0, IMAGE_WIDTH, IMAGE_HEIGHT)
        # mainLayout.addWidget(self.headerImageBox)
        self.horizontalLayoutWidget = QWidget(self)
        self.horizontalLayoutWidget.setGeometry(
            QRect(0, 0, DIALOG_WIDTH, IMAGE_HEIGHT))

        headerLayout = QHBoxLayout()
        headerLayout.setObjectName("headerLayout")
        headerLayout.setContentsMargins(10, 10, 10, 10)
        headerFrame = QFrame(self.horizontalLayoutWidget)
        headerFrame.setMinimumSize(QSize(DIALOG_WIDTH, IMAGE_HEIGHT))
        headerFrame.setBaseSize(QSize(0, 0))
        headerFrame.setAutoFillBackground(False)
        headerFrame.setObjectName("headerFrame")
        headerFrame.setStyleSheet(
            "QFrame#headerFrame { background-repeat:no-repeat; background-position: left; background-image: url(:/images/images/WomanReadingHeader.png); }")
        headerFrame.setFrameShape(QFrame.StyledPanel)
        headerFrame.setFrameShadow(QFrame.Raised)
        headerFrame.setLayout(headerLayout)

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
        headerLayout.addStretch()
        headerLayout.addWidget(self.headerSpacerWidget)
        headerLayout.addWidget(self.wordFilterLabel)
        headerLayout.addWidget(self.wordFilter)
        # headerLayout.addStretch()
        self.wordFilter.setStyleSheet(
            "background-color: #FFFFFF; padding:1px 1px 1px 1px")
        self.wordFilter.setFixedWidth(120)
        self.wordFilter.returnPressed.connect(self.setWordFilter)
        self.wordFilter.setToolTip(
            "Enter a starting letter or letters to find beautiful words")

        self.meaningFilterLabel = QLabel("  Meaning Filter", headerFrame)
        self.meaningFilter = QLineEdit(headerFrame)
        self.meaningFilter.setStyleSheet("color: rgb(0, 0, 0);\n"
                                         "background-color: rgb(255, 255, 255);")
        self.meaningFilterLabel.setBuddy(self.meaningFilter)
        self.meaningFilterLabel.setStyleSheet("color: rgb(255, 255, 255);")
        headerLayout.addWidget(self.meaningFilterLabel)
        headerLayout.addWidget(self.meaningFilter)
        # headerLayout.addStretch()

        self.meaningFilter.setStyleSheet(
            "background-color: #FFFFFF; padding:1px 1px 1px 1px")
        self.meaningFilter.setFixedWidth(120)
        self.meaningFilter.returnPressed.connect(self.setMeaningFilter)
        self.meaningFilter.setToolTip(
            "Enter a meaning for which you would like to find a beautiful word")

        self.tagFilterLabel = QLabel(" Tag Filter", headerFrame)
        self.tagFilter = QLineEdit(headerFrame)
        self.tagFilter.setStyleSheet("color: rgb(0, 0, 0);\n"
                                     "background-color: rgb(255, 255, 255);")
        self.tagFilterLabel.setBuddy(self.tagFilter)
        self.tagFilterLabel.setStyleSheet("color: rgb(255, 255, 255);")
        headerLayout.addWidget(self.tagFilterLabel)
        headerLayout.addWidget(self.tagFilter)
        # headerLayout.addStretch()

        self.tagFilter.setStyleSheet(
            "background-color: #FFFFFF; padding:1px 1px 1px 1px")
        self.tagFilter.setFixedWidth(120)
        self.tagFilter.returnPressed.connect(self.setTagFilter)
        self.tagFilter.setToolTip(
            "Enter a word you like like to find beautiful synonyms for")

        classifications = ["Feelings and Emotions", "Fears", "Colours, Tones, shades", "Sounds", "Texture", "Atmosphere", "Interiors, Furnishings", "Exteriors", "Light, Darkness", "Botany", "Olfactory", "Personalities",
                           "Love", "Movement", "Music", "Taste", "Touch", "Beauty", "Art", "Culture", "Speech", "Geography", "Relationships", "Travel", "Sensory ", "Education and Development", "Physicality ", "Shape", "Time"]
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
        headerLayout.addWidget(self.classificationFilterLabel)
        headerLayout.addWidget(self.classificationFilter)
        headerLayout.addStretch()

        self.classificationFilter.setStyleSheet(
            "background-color: #FFFFFF; padding:1px 1px 1px 1px")
        self.classificationFilter.setFixedWidth(120)
        self.classificationFilter.currentTextChanged.connect(
            self.setClassificationFilter)
        self.classificationFilter.setToolTip(
            "Select a Classification for which you would like to find beautiful words")
        # headerLayout.addSpacing(50)
        # mainLayout.addChildLayout()
        # mainLayout.addLayout(headerLayout)
        mainLayout.addWidget(headerFrame)
        mainLayout.addWidget(self.tableView)

        self.setGeometry(300, 300, DIALOG_WIDTH, DIALOG_HEIGHT)
        self.setFixedSize(DIALOG_WIDTH, DIALOG_HEIGHT)
        self.setWindowTitle(self.title)
        self.setLayout(mainLayout)

    def setWordFilterString(self, string):
        self.filterString = "^" + string

    def setMeaningFilterString(self, string):
        self.filterString = string

    def setTagFilterString(self, string):
        self.filterString = string

    def getItem(self, index):
        mapped_index = self.proxyModel.mapToSource(index)
        row = mapped_index.row()
        column = mapped_index.column()
        data = mapped_index.data()
        print("Row:  " + str(row) + ",Column:  " + str(column) + "  " + data)

    def setWordFilter(self):
        self.setWordFilterString(self.wordFilter.text())
        self.filterColumn = 0
        self.filterRegExpChanged()

    def setMeaningFilter(self):
        self.setMeaningFilterString(self.meaningFilter.text())
        self.filterColumn = 1
        self.filterRegExpChanged()

    def setTagFilter(self):
        self.setTagFilterString(self.tagFilter.text())
        self.filterColumn = 2
        self.filterRegExpChanged()

    def setSourceModel(self, model):
        # the proxy model points to a source model then we create to hold the actual data
        self.proxyModel.setSourceModel(model)
        self.sourceView.setModel(model)

    def setClassificationFilter(self, text):
        """
        Change the combo box value . Values represent the different file
         extensions.
        """
        self.classificationFilterValue = text

    def filterRegExpChanged(self):
        syntax = QRegExp.RegExp  # can be one of QRegExp.RegExp2, QRegExp.WildCard, QRegExp.RegExp2 etc, see https://doc.qt.io/qt-5/qregexp.html#PatternSyntax-enum
        caseSensitivity = Qt.CaseInsensitive
        regExp = QRegExp(self.filterString,
                         caseSensitivity, syntax)
        # This property holds the QRegExp used to filter the contents of the source model
        self.proxyModel.setFilterKeyColumn(self.filterColumn)
        self.proxyModel.setFilterRegExp(regExp)

    # Reference: https://doc.qt.io/archives/qtjambi-4.5.2_01/com/trolltech/qt/qtjambi-customfilter.html
