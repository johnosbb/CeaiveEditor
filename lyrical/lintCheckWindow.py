# import necessary modules
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,  QLineEdit, QPushButton, QStatusBar,
                             QVBoxLayout, QMainWindow, QDialog, QScrollArea, qApp, QTextEdit)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QTextBlockUserData, QTextDocument, QPalette, QColor
from lintHighlighter import LintHighlighter
from lintCheck import LintCheck
from correctorTextEdit import CorrectorTextEdit
import logging
import proselint


class LintCorrectionWindow(QDialog):

    requestCheck = pyqtSignal(QTextDocument)

    def __init__(self):
        super().__init__()
        self._textToCorrect = ""
        self._correctedText = ""
        self._thread = QThread()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.initializeUI()

    def reportProgress(self, n):
        logging.debug("Progress Update {}".format(n))

    def check(self, selection):
        self.selection = selection

        self.txtMain.setHtml(self.selection.toHtml())
        self.createThreadedCheck()

    def createThreadedCheck(self):
        self.status.showMessage("{}".format(
            "Linting the selection, please wait"), 2000)
        self._threaded = LintCheck(result=self.checkFinished)
        self.requestCheck.connect(self._threaded.checkDocument)
        self._thread.started.connect(self._threaded.start)
        self._threaded.moveToThread(self._thread)
        qApp.aboutToQuit.connect(self._thread.quit)
        self._thread.start()
        self.requestCheck.emit(self.txtMain.document())

    @pyqtSlot()
    def checkFinished(self):
        logging.debug("lintCheckWindow: Check finished")
        self.txtMain.lintHighlighter.rehighlight()
        self.status.showMessage("{}".format(
            "Lint Review Complete"), 2000)

    def initializeUI(self):
        self.txtMain = CorrectorTextEdit()
        self.setMinimumSize(800, 600)
        self.setWindowTitle('Lint Check')
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
        logging.debug("lintCheckWindow: A word was replaced rule offset: {} offset adjustment {} ".format(
            rule.offset, offsetAdjustment))
        self.textToCorrect = self.txtMain.toPlainText()
        if(block.userData().value):
            rules = block.userData().value
        self.updateRuleOffsets(rule, rules, offsetAdjustment)
        self.txtMain.lintHighlighter.rehighlight()

    def updateRuleOffsets(self, activeRule, rules, offsetAdjustment):
        for rule in rules:
            if(rule.offset > activeRule.offset):
                logging.debug("lintCheckWindow: Adjusting rule offset at {}, new offset is {}".format(
                    rule.offset, rule.offset + offsetAdjustment))
                rule.offset = rule.offset + offsetAdjustment
        rules.remove(activeRule)
        logging.debug(
            "lintCheckWindow: Removing active rule, rules remaining {}".format(len(rules)))

    def acceptCorrections(self):
        self._correctedText = self.txtMain.toHtml()
        self.accept()

    def SetupControls(self):
        self.txtMain.setMinimumHeight(200)
        self.txtMain.wordReplaced.connect(
            self.wordReplaced)
        self.txtMain.lintHighlighter = LintHighlighter(
            self.txtMain.document())
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
