

from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QMenu, QAction, QDialog, QGridLayout,
                             QTableView,  QHeaderView, QLineEdit, QLabel, QFrame, QVBoxLayout, QHBoxLayout, QComboBox)
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import Qt, QRegExp, QRect, QSize,  QPoint
import logging
# import utilities as Utilities

from sortWordsForSmellFilterProxyModel import SortWordsForSmellFilterProxyModel


DIALOG_WIDTH = 900
DIALOG_HEIGHT = 700
IMAGE_WIDTH = DIALOG_WIDTH
IMAGE_HEIGHT = 103
COLUMN_TO_FILTER = 0
SPACER_SIZE = 20


class WordsForSmellSelectorDialog(QDialog):
    def __init__(self,  title, classifications, parent=None,):
        QDialog.__init__(self,  parent)
        self.parent = parent
        self._selectedWord = ""
        self.classifications = classifications

        self.lastStart = 0
        self.title = title
        self.proxyModel = SortWordsForSmellFilterProxyModel(self)
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
        self.tableView.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.tableView.setSortingEnabled(True)
        self.tableView.verticalHeader().hide()
        self.tableView.setSelectionMode(QTableView.SingleSelection)
        self.tableView.setSelectionBehavior(QTableView.SelectRows)
        self.tableView.clicked.connect(self.selectItem)

        self.filterString = ""
        self.filterColumn = 0
        self.resetFilterEnables()
        self.initUI()

    def resetFilterEnables(self):
        self.smellFilterEnabled = False
        self.smellDescriptionFilterEnabled = False
        self.tagFilterEnabled = False
        self.classificationFilterEnabled = False

    def clearFilters(self):
        logging.debug("Clearing the filters")
        self.smellFilter.setText("")
        self.classificationFilter.setCurrentIndex(0)

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

    def createHeader(self):
        self.headerLayout = QHBoxLayout()
        self.headerLayout.setObjectName("self.headerLayout")
        self.headerLayout.setContentsMargins(10, 10, 10, 10)
        self.headerFrame = QFrame(self.horizontalLayoutWidget)
        self.headerFrame.setMinimumSize(QSize(DIALOG_WIDTH-20, IMAGE_HEIGHT))
        self.headerFrame.setMaximumSize(QSize(DIALOG_WIDTH-20, IMAGE_HEIGHT))
        self.headerFrame.setBaseSize(QSize(0, 0))
        self.headerFrame.setAutoFillBackground(False)
        self.headerFrame.setObjectName("HeaderBackgroundImage")

        self.headerFrame.setStyleSheet(
            "QFrame#HeaderBackgroundImage { background-repeat:no-repeat; background-position: left; background-image: url(:/images/images/WordsForSmellLongForm.png); }")
        self.headerFrame.setFrameShape(QFrame.StyledPanel)
        self.headerFrame.setFrameShadow(QFrame.Raised)
        self.headerFrame.setLayout(self.headerLayout)
        self.headerSpacerWidget = QWidget(self.headerFrame)
        self.headerSpacerWidget.setObjectName("headerSpacerWidget")
        self.headerSpacerWidget.setGeometry(
            QRect(0, 0, SPACER_SIZE, SPACER_SIZE))
        self.headerSpacerWidget.setObjectName("headerSpacerWidget")
        self.smellFilter = QLineEdit(self.headerFrame)
        self.smellFilterLabel = QLabel(
            "  Smell Filter", self.headerFrame)
        self.smellFilterLabel.setBuddy(self.smellFilter)
        self.smellFilter.setStyleSheet("color: rgb(0, 0, 0);\n"
                                       "background-color: rgb(255, 255, 255);")
        self.smellFilterLabel.setStyleSheet(
            "QLabel { color: rgb(255, 255, 255); font-weight:600 }")
        self.smellFilterLabel.setObjectName(
            "smellFilterLabel")
        self.headerLayout.addStretch()
        self.headerLayout.addWidget(self.headerSpacerWidget)
        self.headerLayout.addWidget(self.smellFilterLabel)
        self.headerLayout.addWidget(self.smellFilter)

        self.smellFilter.setStyleSheet(
            "background-color: #FFFFFF; padding:1px 1px 1px 1px")
        self.smellFilter.setFixedWidth(120)

        self.smellFilter.textChanged.connect(self.setSmellFilter)
        self.smellFilter.setToolTip(
            "Enter a starting letter or letters to find colour descriptors")

        self.smellDescriptionFilterLabel = QLabel(
            "  Description Filter", self.headerFrame)
        self.smellDescriptionFilter = QLineEdit(self.headerFrame)
        self.smellDescriptionFilter.setStyleSheet("color: rgb(0, 0, 0);\n"
                                                  "background-color: rgb(255, 255, 255);")
        self.smellDescriptionFilterLabel.setBuddy(self.smellDescriptionFilter)
        self.smellDescriptionFilterLabel.setStyleSheet(
            "QLabel { color: rgb(255, 255, 255); font-weight:600 }")
        self.headerLayout.addWidget(self.smellDescriptionFilterLabel)
        self.headerLayout.addWidget(self.smellDescriptionFilter)

        self.smellDescriptionFilter.setStyleSheet(
            "background-color: #FFFFFF; padding:1px 1px 1px 1px")
        self.smellDescriptionFilter.setFixedWidth(120)
        self.smellDescriptionFilter.textChanged.connect(
            self.setSmellDescriptionFilter)
        self.smellDescriptionFilter.setToolTip(
            "Enter a description for which you would like to find a word describing smell")

        self.classificationFilterLabel = QLabel(
            " Smell Qualifier Filter", self.headerFrame)
        self.classificationFilter = QComboBox(self.headerFrame)

        self.classificationFilter.setStyleSheet("QComboBox { color: rgb(0, 0, 0);\n"
                                                "background-color: rgb(255, 255, 255); padding:1px 1px 1px 1px;}")

        self.classificationFilter.addItems(self.classifications)
        self.classificationFilterValue = self.classifications[0]
        self.classificationFilterLabel.setStyleSheet(
            "QLabel { color: rgb(255, 255, 255); font-weight:600 }")

        self.classificationFilterLabel.setBuddy(self.classificationFilter)
        self.headerLayout.addWidget(self.classificationFilterLabel)
        self.headerLayout.addWidget(self.classificationFilter)
        self.AddClearFiltersButton()
        self.headerLayout.addStretch()
        # self.classificationFilter.setStyleSheet(
        #     "background-color: #FFFFFF; padding:1px 1px 1px 1px")
        self.classificationFilter.setFixedWidth(120)
        self.classificationFilter.currentTextChanged.connect(
            self.setClassificationFilter)
        self.classificationFilter.setToolTip(
            "Select a descriptor classification for which you would like to find words")

    def initUI(self):
        mainLayout = QVBoxLayout()
        self.horizontalLayoutWidget = QWidget(self)
        self.horizontalLayoutWidget.setGeometry(
            QRect(0, 0, DIALOG_WIDTH, IMAGE_HEIGHT))
        self.createHeader()
        mainLayout.addWidget(self.headerFrame)
        mainLayout.addWidget(self.tableView)

        self.setGeometry(300, 300, DIALOG_WIDTH, DIALOG_HEIGHT)
        self.setFixedSize(DIALOG_WIDTH, DIALOG_HEIGHT)
        self.setWindowTitle(self.title)
        self.setLayout(mainLayout)

    def selectItem(self, index):
        mapped_index = self.proxyModel.mapToSource(index)
        data = mapped_index.data()
        self.selectionMenu = QMenu(self)
        icon = QIcon(":/images/images/clipboard-paste-document-text.png")
        selectionAction = self.selectionMenu.addAction(icon,
            'Click {} to insert this word into your document'.format("here"))
        selectionAction.triggered.connect(lambda: self.showSelection(data))
        x = QCursor.pos().x()
        y = QCursor.pos().y()
        newPosition = QPoint(x+5, y+5)
        self.selectionMenu.exec_(newPosition)

    def showSelection(self, data):
        self.selectedWord = data
        self.accept()

    def setSmellFilter(self):
        text = self.smellFilter.text()
        if((text is not None) and (not text.isspace()) and (text != "")):
            self.filterString = "" + text
            self.smellFilterPattern = repr(
                self.filterString)[1:-1]
            self.filterColumn = 0
            self.smellFilterEnabled = True
            self.filterRegExpChanged()
        else:
            self.smellFilterEnabled = False
            self.filterString = ""
            self.smellFilterPattern = repr(
                self.filterString)[1:-1]
            self.filterRegExpChanged()

    def setSmellDescriptionFilter(self):
        text = self.smellDescriptionFilter.text()
        if((text is not None) and (not text.isspace()) and (text != "")):
            self.descriptionFilterPattern = repr(
                text)[1:-1]
            self.filterColumn = 1
            self.smellDescriptionFilterEnabled = True
            self.filterRegExpChanged()
        else:
            self.smellDescriptionFilterEnabled = False
            self.filterString = ""
            self.descriptionFilterPattern = repr(
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
