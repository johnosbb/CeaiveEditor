import re

from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QTextDocument
from PyQt5.QtWidgets import qApp
from lintCheck import LintCheck


class LintHighlighter(QSyntaxHighlighter):

    def __init__(self, parent: QTextDocument) -> None:
        super().__init__(parent)
        self.echoDictionary = {}
        self._thread = QThread()
        self.blockNumber = -1
        self.selectionEnd = -1
        self.selectionStart = -1
        self.typeOfCheck = "Spelling"
        self.rules = None

    # This gets called with each paragraph of a document open in the QTextDocument

    def highlightBlock(self, text: str) -> None:
        if text == '':
            return
        self.textToCorrect = text
        block = self.currentBlock()
        # The character format of text in a document specifies the visual properties of the text, as well as information about its role in a hypertext document.
        self.misspelledFormat = QTextCharFormat()
        self.misspelledFormat.setUnderlineStyle(
            QTextCharFormat.SpellCheckUnderline)  # we can set its visual style
        self.misspelledFormat.setUnderlineColor(Qt.red)  # red and underlined

        self.echoFormat = QTextCharFormat()
        self.echoFormat.setUnderlineStyle(
            QTextCharFormat.WaveUnderline)  # we can set its visual style
        self.echoFormat.setUnderlineColor(Qt.blue)  # red and underlined
        if(self.currentBlockUserData()):
            rules = self.currentBlockUserData().value
            self.check(text, rules)

    def check(self, text, rules):
        self.textToCorrect = text
        if(rules):
            if(len(rules) > 0):
                for rule in rules:
                    startPosition = rule.offset
                    count = rule.errorLength
                    self.updateSyntax(startPosition, count)

    def updateSyntax(self, start, length):
        self.setFormat(    # if it is not we underline it using the style shown above
            start,  # index of first letter of match
            # index of last letter - index of first letter= length
            length,
            self.misspelledFormat,
        )

    def setTargetBlockNumber(self, blockNumber, start, end):
        self.blockNumber = blockNumber
        self.selectionStart = start
        self.selectionEnd = end

    def setLintRules(self, rules):
        self.rules = rules

    def setTypeOfCheck(self, checkType):
        self.typeOfCheck = checkType

    def resetTypeOfCheck(self):
        self.typeOfCheck = "spelling"
