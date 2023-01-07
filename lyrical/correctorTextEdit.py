
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import logging

from specialActionBlock import SpecialActionBlock


from pprint import pprint


class CorrectorTextEdit(QTextEdit):

    wordReplaced = pyqtSignal(object, object, int)

    def __init__(self, *args):
        super().__init__(*args[3:])
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.rule = None
        self.rules = None

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.createContextMenu()
            cursor = self.cursorForPosition(event.pos())
            position = cursor.position()
            textCursor = self.textCursor()
            textCursor.setPosition(position)
            newPosition = cursor.position()
            blockPosition = textCursor.positionInBlock()
            blockNumber = textCursor.blockNumber()
            print("Cursor position {} {}".format(position, blockPosition))
            rule = self.findAssociatedRule(blockNumber, blockPosition)
            if rule:
                self.addHelperContexts(rule, blockNumber)
            else:
                print("No rules found for this word")
            self.contextMenu.exec_(event.globalPos())

    def createContextMenu(self):
        self.contextMenu = QMenu(self)

    def addHelperContexts(self, rule, blockNumber):
        suggestions = rule.replacements
        if len(suggestions) > 0:
            self.contextMenu.addSeparator()
            self.contextMenu.addMenu(
                self.createSuggestionsMenu(suggestions, rule, blockNumber))

    def setRule(self, rule):
        self.rule = rule

    def setRules(self, rules):
        self.rules = rules

    def replaceSelectedWord(self, word, rule, blockNumber):
        # we are using the wrong line
        # textCursor = self.textCursor()

        block = self.document().findBlockByNumber(blockNumber)
        blockStartsAt = block.position()
        blockCursor = QTextCursor(block)
        blockCursor.beginEditBlock()
        blockCursor.clearSelection()
        blockCursor.setPosition(rule.offset + blockStartsAt)
        originalLength = len(rule.matchedText)
        modifiedLength = len(word)
        changeInOffset = modifiedLength - originalLength
        print("Change in offset {}".format(changeInOffset))
        blockCursor.setPosition(
            blockStartsAt + rule.offset + rule.errorLength, QTextCursor.KeepAnchor)
        self.setTextCursor(blockCursor)
        blockCursor.removeSelectedText()
        blockCursor.insertText(word)
        blockCursor.endEditBlock()
        self.ensureCursorVisible()
        self.wordReplaced.emit(rule, block, changeInOffset)

    @ pyqtSlot(str, object, int)
    def correctWord(self, word: str, rule, blockNumber):
        self.replaceSelectedWord(word, rule, blockNumber)

    def createSuggestionsMenu(self, suggestions: list[str], rule, blockNumber):
        suggestionsMenu = QMenu("Change to", self)
        for word in suggestions:
            action = SpecialActionBlock(
                word, self.contextMenu, rule, blockNumber)
            action.actionTriggered.connect(self.correctWord)
            suggestionsMenu.addAction(action)
        return suggestionsMenu

    def findAssociatedRule(self, blockNumber, currentPosition):
        # we only want to check single isolated words.
        print("Finding rules for position {}\n".format(
            currentPosition))
        block = self.document().findBlockByNumber(blockNumber)
        if(block.userData().value):
            rules = block.userData().value
            for rule in rules:
                ruleStart = (rule.offset)
                ruleEnd = (rule.errorLength+rule.offset)
                if((currentPosition >= ruleStart) and (currentPosition <= ruleEnd)):
                    print(" Position: {} - RS {} - RE {} ".format(
                        currentPosition, ruleStart,  ruleEnd))
                    self.rule = rule
                    return rule
        print("Could not find a rule for {}".format(currentPosition))
        return None
