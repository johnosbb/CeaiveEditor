
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
            # print("Cursor position {} {}".format(position, blockPosition))
            rule = self.findAssociatedRule(blockNumber, blockPosition)
            if rule:
                self.addHelperContexts(rule, blockNumber)
            else:
                logging.debug(
                    "CorrectTextEdit - MousePressEvent: No rules found for this text")
            self.contextMenu.exec_(event.globalPos())

    def createContextMenu(self):
        self.contextMenu = QMenu(self)

    def addHelperContexts(self, rule, blockNumber):
        suggestions = rule.replacements
        if(suggestions):
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
        if(rule.ruleId == -1):
            if(rule.category in ["cliches.garner", "cliches.write_good"]):
                logging.debug(
                    "correctorTextEdit: Cliche detected {}".format(rule.message))
                suggestionsMenu = QMenu("{}".format(rule.ruleIssueType), self)
                suggestionsClicheAction = QAction(
                    "I suggest you replace with a more original alternative.", self)
                suggestionsClicheAction.setDisabled(True)
                suggestionsMenu.addAction(suggestionsClicheAction)
            elif(rule.category in ["typography.symbols.multiplication_symbol", "skunked_terms.misc", "mixed_metaphors.misc.bottleneck", "uncomparables.misc", "misc.illogic.coin", "misc.suddenly", "leonard.hell", "dates_times.dates", "dates_times.am_pm.midnight_noon", "lexical_illusions.misc", "redundancy.nordquist", "pinker.scare_quotes", "hyperbolic.misc"]):
                logging.debug(
                    "correctorTextEdit: Issue detected {}".format(rule.message))
                suggestionsMenu = QMenu("{}".format(rule.ruleIssueType), self)
                suggestionsClicheAction = QAction(
                    "I suggest you revise.", self)
                suggestionsClicheAction.setDisabled(True)
            elif(rule.category in ["oxford.venery_terms", "garner.preferred_forms"]):
                logging.debug(
                    "correctorTextEdit: venery or preferred terms issue detected {}".format(rule.message))
                suggestionsMenu = QMenu("{}".format(rule.ruleIssueType), self)
                suggestionsAction = QAction(
                    "I suggest you replace with: {}".format(rule.replacements), self)
                suggestionsAction.setDisabled(False)
                suggestionsMenu.addAction(suggestionsAction)
                action = SpecialActionBlock(
                    suggestions, self.contextMenu, rule, blockNumber)
                action.actionTriggered.connect(self.correctWord)
                suggestionsMenu.addAction(action)
            elif(rule.category == "misc.mondegreens"):
                logging.debug(
                    "correctorTextEdit: Possible mondegreens detected {}".format(rule.message))
                suggestionsMenu = QMenu("{}".format(rule.ruleIssueType), self)
                suggestionsAction = QAction(
                    "Did you mean: {}".format(rule.replacements), self)
                suggestionsAction.setDisabled(False)
                suggestionsMenu.addAction(suggestionsAction)
                action = SpecialActionBlock(
                    suggestions, self.contextMenu, rule, blockNumber)
                action.actionTriggered.connect(self.correctWord)
                suggestionsMenu.addAction(action)
            else:
                logging.debug(
                    "correctorTextEdit: Issues detected {}".format(rule.message))
                suggestionsMenu = QMenu("{}".format(rule.ruleIssueType), self)
                suggestionsAction = QAction(
                    "I suggest you replace with: {}".format(rule.replacements), self)
                suggestionsAction.setDisabled(False)
                suggestionsMenu.addAction(suggestionsAction)
                if type(suggestions) == list:
                    for suggestion in suggestions:
                        action = SpecialActionBlock(
                            suggestion, self.contextMenu, rule, blockNumber)
                elif type(suggestions) == str:
                    action = SpecialActionBlock(
                        suggestions, self.contextMenu, rule, blockNumber)
                action.actionTriggered.connect(self.correctWord)
                suggestionsMenu.addAction(action)
        else:
            logging.debug(
                "correctorTextEdit: Issue detected {}".format(rule.message))
            suggestionsMenu = QMenu("Change to", self)
            for word in suggestions:
                action = SpecialActionBlock(
                    word, self.contextMenu, rule, blockNumber)
            action.actionTriggered.connect(self.correctWord)
            suggestionsMenu.addAction(action)
            # suggestionsMenu = QMenu("{}".format(rule.ruleIssueType), self)
        # oxford.venery_terms
        return suggestionsMenu

    def findAssociatedRule(self, blockNumber, currentPosition):
        # we only want to check single isolated words.
        logging.debug("Finding rules for position {}\n".format(
            currentPosition))
        block = self.document().findBlockByNumber(blockNumber)
        if(block.userData().value):
            rules = block.userData().value
            for rule in rules:
                logging.debug(
                    "correctorTextEdit: Checking rule {} for text {} at position {}".format(rule.message, block.text(), currentPosition))
                ruleStart = (rule.offset)
                ruleEnd = (rule.errorLength+rule.offset)
                if((currentPosition >= ruleStart) and (currentPosition <= ruleEnd)):
                    logging.debug("CorrectorTextEdit: Found Rule {} at position: {} - RS {} - RE {} ".format(
                        rule.message, currentPosition, ruleStart,  ruleEnd))
                    self.rule = rule
                    return rule
        logging.debug("Could not find a rule for {}".format(currentPosition))
        return None
