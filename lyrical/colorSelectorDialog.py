

from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QMenu, QDialog, QGridLayout,
                             QTableView,  QHeaderView, QLineEdit, QLabel, QFrame, QVBoxLayout, QHBoxLayout, QComboBox)
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import Qt, QRegExp, QRect, QSize,  QPoint

# import utilities as Utilities

from sortWordsForColorFilterProxyModel import SortWordsForColorFilterProxyModel

from colorTile import ColorTile

DIALOG_WIDTH = 620
DIALOG_HEIGHT = 700
IMAGE_WIDTH = DIALOG_WIDTH
IMAGE_HEIGHT = 103
COLUMN_TO_FILTER = 0
SPACER_SIZE = 20


class WordForColorSelectorDialog(QDialog):
    def __init__(self,  title, classifications, parent=None,):
        QDialog.__init__(self,  parent)
        self.parent = parent
        self._selectedWord = ""
        self.classifications = classifications

        self.lastStart = 0
        self.title = title
        self.proxyModel = SortWordsForColorFilterProxyModel(self)
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
        self.tableView.setAlternatingRowColors(True)
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
        self.colourFilterEnabled = False
        self.meaningFilterEnabled = False
        self.tagFilterEnabled = False
        self.classificationFilterEnabled = False

    def clearFilters(self):
        print("Clearing the filters")
        self.colourFilter.setText("")
        # self.meaningFilter.setText("")
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
            "QFrame#HeaderBackgroundImage { background-repeat:no-repeat; background-position: left; background-image: url(:/images/images/WordsForColourLongForm.png); }")
        self.headerFrame.setFrameShape(QFrame.StyledPanel)
        self.headerFrame.setFrameShadow(QFrame.Raised)
        self.headerFrame.setLayout(self.headerLayout)
        self.headerSpacerWidget = QWidget(self.headerFrame)
        self.headerSpacerWidget.setObjectName("headerSpacerWidget")
        self.headerSpacerWidget.setGeometry(
            QRect(0, 0, SPACER_SIZE, SPACER_SIZE))
        self.headerSpacerWidget.setObjectName("headerSpacerWidget")
        self.colourFilter = QLineEdit(self.headerFrame)
        self.colourFilterLabel = QLabel("  Colour Filter", self.headerFrame)
        self.colourFilterLabel.setBuddy(self.colourFilter)
        self.colourFilter.setStyleSheet("QLineEdit { color: rgb(0, 0, 0);\n"
                                        "background-color: rgb(255, 255, 255); }")
        self.colourFilterLabel.setStyleSheet(
            "QLabel { color: rgb(255, 255, 255); font-weight:600 }")
        self.colourFilterLabel.setObjectName("colourFilterLabel")
        self.headerLayout.addStretch()
        self.headerLayout.addWidget(self.headerSpacerWidget)
        self.headerLayout.addWidget(self.colourFilterLabel)
        self.headerLayout.addWidget(self.colourFilter)

        self.colourFilter.setStyleSheet(
            "background-color: #FFFFFF; padding:1px 1px 1px 1px")
        self.colourFilter.setFixedWidth(120)

        self.colourFilter.textChanged.connect(self.setWordFilter)
        self.colourFilter.setToolTip(
            "Enter a starting letter or letters to find colours")

        # self.tagFilterLabel = QLabel(" Tag Filter", self.headerFrame)
        # self.tagFilter = QLineEdit(self.headerFrame)
        # self.tagFilter.setStyleSheet("color: rgb(0, 0, 0);\n"
        #                              "background-color: rgb(255, 255, 255);")
        # self.tagFilterLabel.setBuddy(self.tagFilter)
        # self.tagFilterLabel.setStyleSheet("color: rgb(255, 255, 255);")
        # self.headerLayout.addWidget(self.tagFilterLabel)
        # self.headerLayout.addWidget(self.tagFilter)
        # self.tagFilterLabel.setStyleSheet("color: rgb(255, 255, 255);")
        # self.tagFilter.setStyleSheet(
        #     "background-color: #FFFFFF; padding:1px 1px 1px 1px")
        # self.tagFilter.setFixedWidth(120)
        # self.tagFilter.textChanged.connect(self.setTagFilter)
        # self.tagFilter.setToolTip(
        #     "Enter a word you like like to find synonyms for")
        # These classifications need to move into a file that is generated from processing the word list; they should not be hard coded
        self.classificationFilterLabel = QLabel(
            " Colour Family Filter", self.headerFrame)
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
            "Select a Classification for which you would like to find words")

    def createColorPanel(self):
        # Create grid layout
        self.mainGrid = QGridLayout()
        tile1 = ColorTile(0, 0, 20, 20, "#ffffff")
        self.mainGrid.addWidget(tile1, 0, 0)
        tile2 = ColorTile(0, 0, 20, 20, "#ffEDff")
        self.mainGrid.addWidget(tile2, 0, 1)

    def initUI(self):
        mainLayout = QVBoxLayout()
        self.horizontalLayoutWidget = QWidget(self)
        self.horizontalLayoutWidget.setGeometry(
            QRect(0, 0, DIALOG_WIDTH, IMAGE_HEIGHT))
        self.createHeader()
        mainLayout.addWidget(self.headerFrame)
        mainLayout.addWidget(self.tableView)
        # self.createColorPanel()
        # mainLayout.addLayout(self.mainGrid)
        self.setGeometry(300, 300, DIALOG_WIDTH, DIALOG_HEIGHT)
        self.setFixedSize(DIALOG_WIDTH, DIALOG_HEIGHT)
        self.setWindowTitle(self.title)
        self.setLayout(mainLayout)

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

    def showSelection(self, data):
        self.selectedWord = data
        self.accept()

    def setWordFilter(self):
        text = self.colourFilter.text()
        if((text is not None) and (not text.isspace()) and (text != "")):
            self.filterString = "" + text
            self.colourFilterPattern = repr(
                self.filterString)[1:-1]
            self.filterColumn = 0
            self.colourFilterEnabled = True
            self.filterRegExpChanged()
        else:
            self.colourFilterEnabled = False
            self.filterString = ""
            self.colourFilterPattern = repr(
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
