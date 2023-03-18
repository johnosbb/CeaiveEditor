import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QTextDocument

# from spellCheck import SpellCheck
from spellCheckWord import SpellCheckWord


class Highlighter(QSyntaxHighlighter):

    def __init__(self, parent: QTextDocument) -> None:
        super().__init__(parent)
        self.echoDictionary = {}
        self.blockNumber = -1
        self.selectionEnd = -1
        self.selectionStart = -1
        self.typeOfCheck = "Spelling"

    wordRegEx = re.compile(r"\b([A-Za-z]{2,})\b")  # find words
    # This gets called with each paragraph of a document open in the QTextDocument

    def highlightBlock(self, text: str) -> None:
        if not hasattr(self, "speller"):
            return
        if text == '':
            return

        # The character format of text in a document specifies the visual properties of the text, as well as information about its role in a hypertext document.
        self.misspelledFormat = QTextCharFormat()
        self.misspelledFormat.setUnderlineStyle(
            QTextCharFormat.SpellCheckUnderline)  # we can set its visual style
        self.misspelledFormat.setUnderlineColor(Qt.red)  # red and underlined

        self.echoFormat = QTextCharFormat()
        self.echoFormat.setUnderlineStyle(
            QTextCharFormat.WaveUnderline)  # we can set its visual style
        self.echoFormat.setUnderlineColor(Qt.cyan)  # cyan and underlined

        # for spelling and echoes we iterate the text using the regular expression above which identifies word boundaries
        # find individual words in the contained text
        for word_object in self.wordRegEx.finditer(text):
            # we check to see if this is a recognised word
            wordToCheck = word_object.group()

            if not self.speller.check(wordToCheck):
                self.setFormat(    # if it is not we underline it using the style shown above
                    word_object.start(),  # index of first letter of match
                    # index of last letter - index of first letter= length
                    word_object.end() - word_object.start(),
                    self.misspelledFormat,
                )

            currentBlock = self.currentBlock().blockNumber()
            fln = self.currentBlock().firstLineNumber()
            position = self.currentBlock().position()
            startOfBlock = self.selectionStart
            length = self.currentBlock().length()
            endOfBlock = self.selectionEnd
            if(self.typeOfCheck == "echoes"):
                if(self.currentBlock().contains(startOfBlock) or self.currentBlock().contains(endOfBlock)):
                    if(len(self.echoDictionary) > 0):   # if we have a dictionary of echoed words
                        if wordToCheck in self.echoDictionary:  # check to see if the word is an echo
                            self.setFormat(    # if it is not we underline it using the style shown above
                                word_object.start(),  # index of first letter of match
                                # index of last letter - index of first letter= length
                                word_object.end() - word_object.start(),
                                self.echoFormat,
                            )
            if(self.typeOfCheck == "grammar"):
                if(self.currentBlock().contains(startOfBlock) or self.currentBlock().contains(endOfBlock)):
                    # we could pass a collection of grammar errors with their starting and ending position
                    # this would be enough to high light the errors using setFormat
                    # But we also need to present the error to the user and then offer them the possibility
                    # of correcting the error.
                    # Ideally we could present a dialog which shows the error, the suggested replacement and a button to affect the replacement
                    # clicking outside the window will cause it to disappear.
                    if(len(self.echoDictionary) > 0):   # if we have a dictionary of echoed words
                        if wordToCheck in self.echoDictionary:  # check to see if the word is an echo
                            self.setFormat(    # if it is not we underline it using the style shown above
                                word_object.start(),  # index of first letter of match
                                # index of last letter - index of first letter= length
                                word_object.end() - word_object.start(),
                                self.echoFormat,
                            )

    # We can set the echoes here. The pool of echoed words form the reference dictionary for our check

    def setEchoDictionary(self, dictionary):
        self.echoDictionary = dictionary

    def setTargetBlockNumber(self, blockNumber, start, end):
        self.blockNumber = blockNumber
        self.selectionStart = start
        self.selectionEnd = end

    def setSpeller(self, speller: SpellCheckWord):
        self.speller = speller

    def setTypeOfCheck(self, checkType):
        self.typeOfCheck = checkType

    def resetTypeOfCheck(self):
        self.typeOfCheck = "spelling"
