from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import logging
import re
from specialAction import SpecialAction
from highlighter import Highlighter
# from spellCheck import SpellCheck
from spellCheckWord import SpellCheckWord
from describeWord import DescribeWord
from thesaurusWordnet import ThesaurusWordnet
from thesaurusWebster import ThesaurusWebster
import collections
from pprint import pprint


class TextEdit(QTextEdit):

    showSuggestionSignal = pyqtSignal([list])
    updateStatusSignal = pyqtSignal(str)

    def __init__(self, *args):
        if args and type(args[0]) == SpellCheckWord and type(args[1]) == ThesaurusWebster and type(args[2]) == DescribeWord:
            super().__init__(*args[3:])
            self.speller = args[0]
            self.thesaurus = args[1]
            self.compliment = args[2]
            self.lastFindStart = 0
            self.grammarCheckSet = False
            self.setObjectName("HeaderBackgroundColor")
            self.copyAvailable.connect(self.selectedTextChanged)
        else:
            super().__init__(*args)

        self.highlighter = Highlighter(self.document())
        if hasattr(self, "speller"):
            self.highlighter.setSpeller(self.speller)

    def getBackgroundColor(self):
        return self.backGroundColor

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.RightButton:
            event = QMouseEvent(
                QEvent.MouseButtonPress,
                event.pos(),
                Qt.LeftButton,
                Qt.LeftButton,
                Qt.NoModifier,
            )
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        # wordToCheck = self.findSingleSelectedWord()
        # if event.button() == Qt.LeftButton:
        #     if (wordToCheck != "") and (wordToCheck is not None):
        #         suggestions = self.thesaurus.suggestions(wordToCheck)
        #         self.showSuggestionSignal.emit(suggestions)
        #     else:
        #         self.showSuggestionSignal.emit([])
        super().mouseReleaseEvent(event)

    def selectedTextChanged(self, status):
        if(status):
            textCursor = self.textCursor()

            textCursor.select(QTextCursor.WordUnderCursor)
            selectedText = textCursor.selectedText()
            if " " not in selectedText:  # we check for spaces in the phrase and if we find none then we assume they have selected an isolated word
                if (selectedText != "") and (selectedText is not None):
                    # logging.debug("We selected {}".format(selectedText))
                    suggestions = self.thesaurus.suggestions(selectedText)
                    self.showSuggestionSignal.emit(suggestions)
                else:
                    self.showSuggestionSignal.emit([])

    def addHelperContexts(self, wordToCheck):
        suggestions = self.speller.suggestions(wordToCheck)
        alternatives = self.thesaurus.suggestions(wordToCheck)
        compliments = self.compliment.suggestions(wordToCheck)
        if(self.grammarCheckSet):
            self.createGrammarCorrectionMenu()
        if len(suggestions) > 0:
            self.contextMenu.addSeparator()
            self.contextMenu.addMenu(
                self.createSuggestionsMenu(suggestions))
            self.contextMenu.addSeparator()
            self.contextMenu.addMenu(
                self.createSynonymsMenu(alternatives))
            self.contextMenu.addSeparator()
            self.contextMenu.addMenu(
                self.createComplimentsMenu(compliments))
        if not self.speller.check(wordToCheck):
            addToDictionary_action = SpecialAction(
                "Add to dictionary", self.contextMenu
            )
            addToDictionary_action.triggered.connect(self.addToDictionary)
            self.contextMenu.addAction(addToDictionary_action)

    def keyReleaseEvent(self, event):
        key = event.key()

        if (key == Qt.Key_Insert):
            # print('Overwrite mode: ' + str(self.overwriteMode()))
            self.setOverwriteMode(not self.overwriteMode())
        else:
            # release keyrelease for normal behaviors
            super().keyReleaseEvent(event)

    def checkFormating(self):
        # assume no format by default
        bold = italic = underline = False
        textCursor = self.textCursor()
        rangeStart = textCursor.selectionStart()
        if textCursor.hasSelection():
            rangeEnd = textCursor.selectionEnd() + 1
        else:
            rangeEnd = textCursor.selectionStart() + 1
        wordToCheck = textCursor.selectedText()
        for pos in range(rangeStart, rangeEnd):
            textCursor.setPosition(pos)
            fmt = textCursor.charFormat()
            underline = fmt.fontUnderline()
            colour = fmt.underlineColor()
            # logging.debug("underline and colour :" +
            #       str(underline) + "  " + str(colour.name()))
            if fmt.fontWeight() >= QFont.Bold:
                bold = True
            if fmt.fontItalic():
                italic = True
            if fmt.fontUnderline():
                underline = True
            if all((bold, italic, underline)):
                # all formats are set, no need for further checking
                break

    def find(self, query, findType):
        text = self.toPlainText()
        format = QTextCharFormat()
        # format.setBackground(QBrush(QColor("green").lighter(250)))
        if findType == "Normal":
            # Use normal string search to find the query from the
            # last starting position
            self.lastFindStart = text.find(query, self.lastFindStart + 1)

            # If the find() method didn't return -1 (not found)
            if self.lastFindStart >= 0:
                end = self.lastFindStart + len(query)
                # self.moveCursor(self.lastFindStart, end)
                cursor = self.textCursor()
                cursor.setPosition(self.lastFindStart)
                cursor.movePosition(QTextCursor.EndOfWord, 1)
                cursor.mergeCharFormat(format)
                self.ensureCursorVisible()
                self.setTextCursor(cursor)
            else:
                # Make the next search start from the beginning again
                self.lastFindStart = 0
                self.moveCursor(QTextCursor.End)
                self.updateStatusSignal.emit(
                    "No matching text found for {}".format(query))

        else:  # this is a regular expression
            # Compile the pattern
            pattern = re.compile(query)
            # The actual search
            match = pattern.search(text, self.lastFindStart + 1)
            if match:
                self.lastFindStart = match.start()
                self.moveCursor(self.lastFindStart, match.end())
            else:
                self.lastFindStart = 0
                # We set the cursor to the end if the search was unsuccessful
                self.parent.editor.moveCursor(QTextCursor.End)
                self.updateStatusSignal.emit(
                    "No matching text found for expression {}".format(query))

    def highlightEchoes(self, text, echoes, blockNumber, start, end):
        self.highlighter.setEchoDictionary(echoes)
        self.highlighter.setTargetBlockNumber(blockNumber, start, end)
        self.highlighter.setTypeOfCheck("echoes")
        self.highlighter.rehighlight()
        self.highlighter.setEchoDictionary({})
        self.highlighter.resetTypeOfCheck()  # reset it to default

    def findSingleSelectedWord(self) -> None:
        # we only want to check single isolated words.
        textCursor = self.textCursor()
        selectedText = textCursor.selectedText()
        if " " not in selectedText:  # we check for spaces in the phrase and if we find none then we assume they have selected an isolated word
            textCursor.select(QTextCursor.WordUnderCursor)
            self.setTextCursor(textCursor)
            wordToCheck = textCursor.selectedText()
            textCursor.clearSelection()
            if wordToCheck != "":
                return wordToCheck
            else:
                return ""

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        self.contextMenu = self.createStandardContextMenu(event.pos())
        # we only want to check single isolated words.
        wordToCheck = self.findSingleSelectedWord()
        if wordToCheck != "":
            self.addHelperContexts(wordToCheck)
        self.contextMenu.exec_(event.globalPos())

    def createSuggestionsMenu(self, suggestions: list[str]):
        suggestionsMenu = QMenu("Change to", self)
        for word in suggestions:
            action = SpecialAction(word, self.contextMenu)
            action.actionTriggered.connect(self.correctWord)
            suggestionsMenu.addAction(action)
        return suggestionsMenu

    def createGrammarCorrectionMenu(self, suggestions: list[str]):
        suggestionsMenu = QMenu("Change to", self)
        for word in suggestions:
            action = SpecialAction(word, self.contextMenu)
            action.actionTriggered.connect(self.correctWord)
            suggestionsMenu.addAction(action)
        return suggestionsMenu

    def createComplimentsMenu(self, compliments: list[str]):
        complimentsMenu = QMenu("Find complimentary word", self)
        for word in compliments:
            action = SpecialAction(word, self.contextMenu)
            action.actionTriggered.connect(self.replaceWord)
            complimentsMenu.addAction(action)
        return complimentsMenu

    def createSynonymsMenu(self, synonym: list[str]):
        synonymMenu = QMenu("Thesaurus", self)
        for word in synonym:
            action = SpecialAction(word, self.contextMenu)
            action.actionTriggered.connect(self.replaceWord)
            synonymMenu.addAction(action)
        return synonymMenu

    def replaceSelectedWord(self, word: str):
        textCursor = self.textCursor()
        textCursor.beginEditBlock()
        textCursor.removeSelectedText()
        textCursor.insertText(word)
        textCursor.endEditBlock()

    def replaceSelectedText(self, text):
        textCursor = self.textCursor()
        textCursor.beginEditBlock()
        textCursor.removeSelectedText()
        textCursor.insertHtml(text)
        textCursor.endEditBlock()

    def insertSelectedWord(self, word: str):
        textCursor = self.textCursor()
        textCursor.beginEditBlock()
        textCursor.insertText(word)
        textCursor.endEditBlock()

    @ pyqtSlot(str)
    def correctWord(self, word: str):
        self.replaceSelectedWord(word)

    @ pyqtSlot(str)
    def replaceWord(self, word: str):
        self.replaceSelectedWord(word)

    @ pyqtSlot(str)
    def insertWord(self, word: str):
        self.insertSelectedWord(word)

    @ pyqtSlot()
    def addToDictionary(self):
        textCursor = self.textCursor()
        new_word = textCursor.selectedText()
        self.speller.add(new_word)
        self.highlighter.rehighlight()

    def canInsertFromMimeData(self, source):

        if source.hasImage():
            return True
        else:
            return super(TextEdit, self).canInsertFromMimeData(source)

    def insertFromMimeData(self, source):

        cursor = self.textCursor()
        document = self.document()

        if source.hasUrls():

            for u in source.urls():
                file_ext = splitext(str(u.toLocalFile()))
                if u.isLocalFile() and file_ext in IMAGE_EXTENSIONS:
                    image = QImage(u.toLocalFile())
                    document.addResource(QTextDocument.ImageResource, u, image)
                    cursor.insertImage(u.toLocalFile())

                else:
                    # If we hit a non-image or non-local URL break the loop and fall out
                    # to the super call & let Qt handle it
                    break

            else:
                # If all were valid images, finish here.
                return

        elif source.hasImage():
            image = source.imageData()
            uuid = hexuuid()
            document.addResource(QTextDocument.ImageResource, uuid, image)
            cursor.insertImage(uuid)
            return

        super(TextEdit, self).insertFromMimeData(source)
