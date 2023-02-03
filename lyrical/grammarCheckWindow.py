# import necessary modules
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,  QLineEdit, QPushButton, QStatusBar,
                             QVBoxLayout, QMainWindow, QDialog, QScrollArea, qApp, QTextEdit)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QTextBlockUserData, QTextDocument, QPalette, QColor
from grammarHighlighter import GrammarHighlighter
from grammarCheck import GrammarCheck
from correctorTextEdit import CorrectorTextEdit
import logging


class GrammarCorrectionWindow(QDialog):

    requestCheck = pyqtSignal(QTextDocument)

    def __init__(self, tool):
        super().__init__()
        self._textToCorrect = ""
        self._correctedText = ""
        self.tool = tool
        self._thread = QThread()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # self.checkGrammar('At lunchtime, we went to Mangan’s Cafe. It was a nice sunny afternoon and we noticed that the staff had put one or two seating areas out on the sidewalk. These were small green cast iron tables with two ruleing chairs; a navy and white table cloth gave the area a novel continental look that, while a little out of place for the town, was pleasant and refreshing. In the centre of the table was a small glass jar with some lavender and soft peach garden roses arranged in an attractive display. We took our seats there and each ordered a sandwich and an coffee. The town looked very pretty in the warm sunshine; the houses seemed a shade more vibrant and the hills in the background, which were usually softened and obscured by mist, were unusually clear and vivid against a cloudless blue sky.')
        self.initializeUI()

    def reportProgress(self, n):
        logging.debug("Progress Update {}".format(n))

    def check(self, selection):
        self.selection = selection

        self.txtMain.setHtml(self.selection.toHtml())
        self.createThreadedCheck()

    def createThreadedCheck(self):
        self.status.showMessage("{}".format(
            "Reviewing grammar and spelling, please wait"), 2000)
        self._threaded = GrammarCheck(result=self.checkFinished)
        self._threaded.tool = self.tool
        self.requestCheck.connect(self._threaded.checkDocument)
        self._thread.started.connect(self._threaded.start)
        self._threaded.moveToThread(self._thread)
        qApp.aboutToQuit.connect(self._thread.quit)
        self._thread.start()
        self.requestCheck.emit(self.txtMain.document())

    @pyqtSlot()
    def checkFinished(self):
        print("Check finished")
        self.txtMain.grammarHighlighter.rehighlight()
        self.status.showMessage("{}".format(
            "Grammar Review Complete"), 2000)

    def initializeUI(self):
        self.txtMain = CorrectorTextEdit()
        self.setMinimumSize(800, 600)
        self.setWindowTitle('Grammar Check')
        # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.vboxLayout = QVBoxLayout(self)
        # self.vboxLayoutContainingWidget.setLayout(self.vboxLayout)
        self.vboxLayout.addWidget(self.txtMain)
        # self.setCentralWidget(self.scroll)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        self.setPalette(palette)
        self.SetupControls()
        # self.show()

    def wordReplaced(self, rule, block, offsetAdjustment):
        print("A word was replaced rule offset: {} offset adjustment {} ".format(
            rule.offset, offsetAdjustment))
        self.textToCorrect = self.txtMain.toPlainText()
        if(block.userData().value):
            rules = block.userData().value
        self.updateRuleOffsets(rule, rules, offsetAdjustment)
        self.txtMain.grammarHighlighter.rehighlight()

    def updateRuleOffsets(self, activeRule, rules, offsetAdjustment):
        for rule in rules:
            if(rule.offset > activeRule.offset):
                print("Adjusting rule offset at {}, new offset is {}".format(
                    rule.offset, rule.offset + offsetAdjustment))
                rule.offset = rule.offset + offsetAdjustment
        rules.remove(activeRule)
        print("Removing active rule, rules remaining {}".format(len(rules)))

    def acceptCorrections(self):
        self._correctedText = self.txtMain.toHtml()
        self.accept()

    def SetupControls(self):
        self.txtMain.setMinimumHeight(200)
        self.txtMain.wordReplaced.connect(
            self.wordReplaced)
        self.txtMain.grammarHighlighter = GrammarHighlighter(
            self.txtMain.document(), self.tool)
        self.acceptButton = QPushButton(self)
        self.acceptButton.setText("Accept Corrections")  # text
        self.acceptButton.clicked.connect(self.acceptCorrections)
        self.vboxLayout.addWidget(self.acceptButton)
        self.status = QStatusBar()
        # self.statusMode = QLabel("Status")
        # self.status.addPermanentWidget(self.statusMode)
        self.vboxLayout.addWidget(self.status)
        # self.vboxLayout.addWidget(self.txtMain)

    @ property
    def correctedText(self):
        return self._correctedText

    @ correctedText.setter
    def correctedText(self, newWord):
        self._correctedText = newWord

    @ property
    def textToCorrect(self):
        return self._textToCorrect

    @ textToCorrect.setter
    def textToCorrect(self, newWord):
        self._textToCorrect = newWord
