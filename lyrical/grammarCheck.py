from typing import Callable
import language_tool_python
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot
from PyQt5.QtGui import QTextDocument, QTextBlockUserData
import logging


# background worker
class GrammarCheck(QObject):

    result = pyqtSignal()

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.__matches = {}
        self.content = ""

    @pyqtSlot()
    def start(self): print("Thread started")

    def getErrors(self):
        return self.__matches

    def getCorrection(self) -> str:
        return self.tool.correct(self.content)

    def setText(self, text: str):
        self.content = text

    def showMatches(self):
        index = 0
        for match in self.__matches:
            index = index + 1
            print("Match: {}\n".format(index))
            print("Rule ID: {}\n".format(match.ruleId))
            print("Context: {}\n".format(match.context))
            print("Sentence: {}\n".format(match.sentence))
            print("Category: {}\n".format(match.category))
            print("Rule Issue Type: {}\n".format(match.ruleIssueType))
            print("Replacements: {}\n".format(match.replacements))
            print("Messages: {}\n".format(match.message))
            print("Offset: {}\n".format(match.offsetInContext))
            print("Offset in context: {}\n".format(match.offset))
            print("Error Length: {}\n".format(match.errorLength))

    @pyqtSlot(QTextDocument)
    def checkDocument(self, document):
        for blockIndex in range(document.blockCount()):
            logging.debug("Finding rules for block {}".format(blockIndex))
            block = document.findBlockByNumber(blockIndex)
            logging.debug("Block Text: {}".format(block.text()))
            self.checkSection(block, blockIndex)
        self.result.emit()

    def checkSection(self, block, blockIndex):
        logging.debug("grammarCheck: Checking Section: {}".format(block.text()))
        self.content = block.text()
        if(self.content != ""):
            self.__matches = self.__tool.check(self.content)
            logging.debug("grammarCheck: checking Section: found {} rules for block {} ".format(
                self.__matches, blockIndex))
            userData = QTextBlockUserData()
            userData.value = self.__matches
            block.setUserData(userData)
        else:
            logging.debug("grammarCheck: checkSection: Nothing to check")

        # we will now have a set of matches and each of these relates to a section of text in the given text block.
        # We can return these as a collection of corrections
        # The calling program should ideally present these as a correction option when:
        # (a) Someone hovers over that section of text or
        # (b) As a panel of issues which can be corrected by clicking on the relevant issue

    @ property
    def rules(self):
        return self.__matches

    @ rules.setter
    def textToCorrect(self, theRules):
        self.__matches = theRules

    @ property
    def tool(self):
        return self.__tool

    @ tool.setter
    def tool(self, theTool):
        self.__tool = theTool
