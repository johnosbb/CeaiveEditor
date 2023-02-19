

from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QMenu, QAction, QDialog,
                             QTableView,  QHeaderView, QLineEdit, QLabel, QFrame, QVBoxLayout, QHBoxLayout, QComboBox)
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import Qt, QRegExp, QRect, QSize,  QPoint, QItemSelectionModel

# import utilities as Utilities

from sortBeautifulWordsFilterProxyModel import SortBeautifulWordsFilterProxyModel
import globals
import logging


DIALOG_WIDTH = 1000
DIALOG_HEIGHT = 700
IMAGE_WIDTH = DIALOG_WIDTH
IMAGE_HEIGHT = 103
COLUMN_TO_FILTER = 0
SPACER_SIZE = 20


class BeautifulWordSelectorDialog(QDialog):
    def __init__(self,  title, classifications, parent=None,):
        QDialog.__init__(self,  parent)
        self.parent = parent
        self._selectedWord = ""
        self.classifications = classifications

        self.lastStart = 0
        self.title = title
        self.proxyModel = SortBeautifulWordsFilterProxyModel(self)
        # This property holds whether the proxy model is dynamically sorted and filtered whenever the contents of the source model change
        self.proxyModel.setDynamicSortFilter(True)
        self.sourceView = QTableView()  # where we store the unfiltered list
        self.tableView = QTableView()
        self.selectedWord = None
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setModel(self.proxyModel)
        self.tableView.setSortingEnabled(True)
        self.setWindowTitle(title)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSortingEnabled(True)
        self.tableView.verticalHeader().hide()
        self.tableView.setSelectionMode(QTableView.SingleSelection)
        self.tableView.setSelectionBehavior(QTableView.SelectItems)
        self.tableView.clicked.connect(self.selectItem)
        # selectionModel = self.tableView.selectionModel()
        # selectionModel.selectionChanged.connect(self.selectionChanged)

        self.filterString = ""
        self.filterColumn = 0
        self.resetFilterEnables()
        self.initUI()

    def resetFilterEnables(self):
        self.wordFilterEnabled = False
        self.meaningFilterEnabled = False
        self.tagFilterEnabled = False
        self.classificationFilterEnabled = False

    def clearFilters(self):
        logging.debug("Clearing the filters")
        self.wordFilter.setText("")
        self.meaningFilter.setText("")
        self.classificationFilter.setCurrentIndex(0)
        self.tagFilter.setText("")

    def AddClearFiltersButton(self):
        self.clearFiltersButton = QPushButton('', self)
        if(globals.USE_STYLESHEETS_FOR_COLOR):
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
            "QFrame#HeaderBackgroundImage { background-repeat:no-repeat; background-position: left; background-image: url(:/images/images/WomanReadingHeader.png); }")
        self.headerFrame.setFrameShape(QFrame.StyledPanel)
        self.headerFrame.setFrameShadow(QFrame.Raised)
        self.headerFrame.setLayout(self.headerLayout)
        self.headerSpacerWidget = QWidget(self.headerFrame)
        self.headerSpacerWidget.setObjectName("headerSpacerWidget")
        self.headerSpacerWidget.setGeometry(
            QRect(0, 0, SPACER_SIZE, SPACER_SIZE))
        self.headerSpacerWidget.setObjectName("headerSpacerWidget")
        self.wordFilter = QLineEdit(self.headerFrame)
        self.wordFilterLabel = QLabel("  Word Filter", self.headerFrame)
        self.wordFilterLabel.setBuddy(self.wordFilter)
        if(globals.USE_STYLESHEETS_FOR_COLOR):
            self.wordFilter.setStyleSheet("color: rgb(0, 0, 0);\n"
                                          "background-color: rgb(255, 255, 255);")
            self.wordFilterLabel.setStyleSheet(
                "QLabel { color: rgb(255, 255, 255); font-weight:600 }")
        self.wordFilterLabel.setObjectName("wordFilterLabel")
        self.headerLayout.addStretch()
        self.headerLayout.addWidget(self.headerSpacerWidget)
        self.headerLayout.addWidget(self.wordFilterLabel)
        self.headerLayout.addWidget(self.wordFilter)
        if(globals.USE_STYLESHEETS_FOR_COLOR):
            self.wordFilter.setStyleSheet(
                "background-color: #FFFFFF; padding:1px 1px 1px 1px")
        self.wordFilter.setFixedWidth(120)

        self.wordFilter.textChanged.connect(self.setWordFilter)
        self.wordFilter.setToolTip(
            "Enter a starting letter or letters to find words")
        self.meaningFilterLabel = QLabel("  Meaning Filter", self.headerFrame)
        self.meaningFilter = QLineEdit(self.headerFrame)
        if(globals.USE_STYLESHEETS_FOR_COLOR):
            self.meaningFilter.setStyleSheet("color: rgb(0, 0, 0);\n"
                                             "background-color: rgb(255, 255, 255);")
        self.meaningFilterLabel.setBuddy(self.meaningFilter)
        self.meaningFilterLabel.setStyleSheet(
            "QLabel { color: rgb(255, 255, 255); font-weight:600 }")
        self.headerLayout.addWidget(self.meaningFilterLabel)
        self.headerLayout.addWidget(self.meaningFilter)
        if(globals.USE_STYLESHEETS_FOR_COLOR):
            self.meaningFilter.setStyleSheet(
                "background-color: #FFFFFF; padding:1px 1px 1px 1px")
        self.meaningFilter.setFixedWidth(120)
        self.meaningFilter.textChanged.connect(self.setMeaningFilter)
        self.meaningFilter.setToolTip(
            "Enter a meaning for which you would like to find a word")
        self.tagFilterLabel = QLabel(" Tag Filter", self.headerFrame)
        self.tagFilter = QLineEdit(self.headerFrame)
        if(globals.USE_STYLESHEETS_FOR_COLOR):
            self.tagFilter.setStyleSheet("color: rgb(0, 0, 0);\n"
                                         "background-color: rgb(255, 255, 255);")
        self.tagFilterLabel.setBuddy(self.tagFilter)
        if(globals.USE_STYLESHEETS_FOR_COLOR):
            self.tagFilterLabel.setStyleSheet(
                "QLabel { color: rgb(255, 255, 255); font-weight:600 }")
        self.headerLayout.addWidget(self.tagFilterLabel)
        self.headerLayout.addWidget(self.tagFilter)
        if(globals.USE_STYLESHEETS_FOR_COLOR):
            self.tagFilter.setStyleSheet(
                "background-color: #FFFFFF; padding:1px 1px 1px 1px")
        self.tagFilter.setFixedWidth(120)
        self.tagFilter.textChanged.connect(self.setTagFilter)
        self.tagFilter.setToolTip(
            "Enter a word you like like to find synonyms for")
        # These classifications need to move into a file that is generated from processing the word list; they should not be hard coded
        self.classificationFilterLabel = QLabel(
            " Classification Filter", self.headerFrame)
        self.classificationFilter = QComboBox(self.headerFrame)
        if(globals.USE_STYLESHEETS_FOR_COLOR):
            self.classificationFilter.setStyleSheet("color: rgb(0, 0, 0);\n"
                                                    "background-color: rgb(255, 255, 255); padding:1px 1px 1px 1px;")
        self.classificationFilter.addItems(self.classifications)
        self.classificationFilterValue = self.classifications[0]
        if(globals.USE_STYLESHEETS_FOR_COLOR):
            self.classificationFilterLabel.setStyleSheet(

                "QLabel { color: rgb(255, 255, 255); font-weight:600 }")
            self.tagFilterLabel.setStyleSheet(
                "QLabel { color: rgb(255, 255, 255); font-weight:600 }")
        self.classificationFilterLabel.setBuddy(self.classificationFilter)
        self.headerLayout.addWidget(self.classificationFilterLabel)
        self.headerLayout.addWidget(self.classificationFilter)
        self.AddClearFiltersButton()
        self.headerLayout.addStretch()

        self.classificationFilter.setFixedWidth(120)
        self.classificationFilter.currentTextChanged.connect(
            self.setClassificationFilter)
        self.classificationFilter.setToolTip(
            "Select a Classification for which you would like to find words")

    def initUI(self):
        mainLayout = QVBoxLayout()
        self.horizontalLayoutWidget = QWidget(self)
        self.horizontalLayoutWidget.setGeometry(
            QRect(0, 0, DIALOG_WIDTH, IMAGE_HEIGHT))
        self.createHeader()
        self.acceptButton = QPushButton("Insert Selected Word", self)
        self.acceptButton.setToolTip(
            'Insert the selected word into your document')
        self.acceptButton.clicked.connect(
            lambda: self.acceptSelection(self.selectedWord))
        self.acceptButton.setEnabled(False)
        mainLayout.addWidget(self.headerFrame)
        mainLayout.addWidget(self.tableView)
        mainLayout.addWidget(self.acceptButton)
        self.setGeometry(300, 300, DIALOG_WIDTH, DIALOG_HEIGHT)
        self.setFixedSize(DIALOG_WIDTH, DIALOG_HEIGHT)
        self.setWindowTitle(self.title)
        self.setLayout(mainLayout)

    def selectItem(self, index):
        mapped_index = self.proxyModel.mapToSource(index)
        model = mapped_index.model()
        row = mapped_index.row()
        column = mapped_index.column()
        standardItem = model.item(row, 0)
        modelIndex = standardItem.index()
        self.selectedWord = modelIndex.data(0)
        self.acceptButton.setEnabled(True)
        selectionModel = self.tableView.selectionModel()
        # newIndex = self.tableView.model().index(row, 0)
        # selectionModel.select(newIndex, QItemSelectionModel.ClearAndSelect)
        # self.selectionMenu = QMenu(self)
        # icon = QIcon(":/images/images/clipboard-paste-document-text.png")
        # selectionAction = self.selectionMenu.addAction(icon,
        #                                                'Click {} to insert this word into your document'.format("here"))

        # selectionAction.triggered.connect(lambda: self.acceptSelection(data))
        # x = QCursor.pos().x()
        # y = QCursor.pos().y()
        # newPosition = QPoint(x+5, y+5)
        # self.selectionMenu.exec_(newPosition)

    def acceptSelection(self, data):
        if(data):
            self.selectedWord = data
            self.accept()

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
