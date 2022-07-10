from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *


from specialAction import SpecialAction
from highlighter import SpellCheckHighlighter
from spellCheck import SpellCheck
from thesaurusWordnet import ThesaurusWordnet
from thesaurusWebster import ThesaurusWebster

from pprint import pprint


class TextEdit(QTextEdit):

    showSuggestionSignal = pyqtSignal([list])

    def __init__(self, *args):
        if args and type(args[0]) == SpellCheck and type(args[1]) == ThesaurusWebster:
            super().__init__(*args[2:])
            self.speller = args[0]
            self.thesaurus = args[1]
            self.setObjectName("HeaderBackgroundColor")
            # background-repeat:repeat; background-position: top left; background-origin: content;  background-clip: padding;
            # self.setStyleSheet(
            #    "QTextEdit#HeaderBackgroundImage { background-position: top left; background-origin: content;  background-clip: padding; background-image: url(:/images/images/paperbackgrounds1.png); }")
            self.setStyleSheet(
                "QTextEdit#HeaderBackgroundColor { background-color: #F1F0E8;}")
        else:
            super().__init__(*args)

        self.highlighter = SpellCheckHighlighter(self.document())
        if hasattr(self, "speller"):
            self.highlighter.setSpeller(self.speller)

    def setSpeller(self, speller):
        self.speller = speller
        self.highlighter.setSpeller(self.speller)

    def setThesaurus(self, thesaurus):
        self.thesaurus = thesaurus
        self.highlighter.setThesaurus(self.thesaurus)

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
        wordToCheck = self.findSingleSelectedWord()
        if event.button() == Qt.LeftButton:
            if (wordToCheck != "") and (wordToCheck is not None):
                suggestions = self.thesaurus.suggestions(wordToCheck)
                self.showSuggestionSignal.emit(suggestions)
            else:
                self.showSuggestionSignal.emit([])
        super().mouseReleaseEvent(event)

    def addSpellCheckAndThesaurusContext(self, wordToCheck):
        suggestions = self.speller.suggestions(wordToCheck)
        alternatives = self.thesaurus.suggestions(wordToCheck)

        if len(suggestions) > 0:
            self.contextMenu.addSeparator()
            self.contextMenu.addMenu(
                self.createSuggestionsMenu(suggestions))
            self.contextMenu.addSeparator()
            self.contextMenu.addMenu(
                self.create_synonyms_menu(alternatives))

        if not self.speller.check(wordToCheck):
            addToDictionary_action = SpecialAction(
                "Add to dictionary", self.contextMenu
            )
            addToDictionary_action.triggered.connect(self.addToDictionary)
            self.contextMenu.addAction(addToDictionary_action)

    def keyReleaseEvent(self, event):
        key = event.key()

        if (key == Qt.Key_Insert):
            print('Overwrite mode: ' + str(self.overwriteMode()))
            self.setOverwriteMode(not self.overwriteMode())
        else:
            # release keyrelease for normal behaviors
            super().keyReleaseEvent(event)

    def check_formatting(self):
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
            print("underline and colour :" +
                  str(underline) + "  " + str(colour.name()))
            if fmt.fontWeight() >= QFont.Bold:
                bold = True
            if fmt.fontItalic():
                italic = True
            if fmt.fontUnderline():
                underline = True
            if all((bold, italic, underline)):
                # all formats are set, no need for further checking
                break

    def findSingleSelectedWord(self) -> None:
        # we only want to check single isolated words.
        textCursor = self.textCursor()
        selectedText = textCursor.selectedText()
        if " " not in selectedText:  # we check for spaces in the phrase and if we find none then we assume they have selected an isolated word
            textCursor.select(QTextCursor.WordUnderCursor)
            self.setTextCursor(textCursor)
            wordToCheck = textCursor.selectedText()
            if wordToCheck != "":
                return wordToCheck
            else:
                return ""

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        self.contextMenu = self.createStandardContextMenu(event.pos())
        # we only want to check single isolated words.
        wordToCheck = self.findSingleSelectedWord()
        if wordToCheck != "":
            self.addSpellCheckAndThesaurusContext(wordToCheck)
        self.contextMenu.exec_(event.globalPos())

    def createSuggestionsMenu(self, suggestions: list[str]):
        suggestionsMenu = QMenu("Change to", self)
        for word in suggestions:
            action = SpecialAction(word, self.contextMenu)
            action.actionTriggered.connect(self.correct_word)
            suggestionsMenu.addAction(action)

        return suggestionsMenu

    def create_synonyms_menu(self, synonym: list[str]):
        synonymMenu = QMenu("Thesaurus", self)
        for word in synonym:
            action = SpecialAction(word, self.contextMenu)
            action.actionTriggered.connect(self.replaceWord)
            synonymMenu.addAction(action)

        return synonymMenu

    def replace_selected_word(self, word: str):
        textCursor = self.textCursor()
        textCursor.beginEditBlock()
        textCursor.removeSelectedText()
        textCursor.insertText(word)
        textCursor.endEditBlock()

    def insert_selected_word(self, word: str):
        textCursor = self.textCursor()
        textCursor.beginEditBlock()
        textCursor.insertText(word)
        textCursor.endEditBlock()

    @ pyqtSlot(str)
    def correct_word(self, word: str):
        self.replace_selected_word(word)

    @ pyqtSlot(str)
    def replaceWord(self, word: str):
        self.replace_selected_word(word)

    @ pyqtSlot(str)
    def insertWord(self, word: str):
        self.insert_selected_word(word)

    @ pyqtSlot()
    def addToDictionary(self):
        textCursor = self.textCursor()
        new_word = textCursor.selectedText()
        self.speller.add(new_word)
        self.highlighter.rehighlight()

    def can_insert_from_mime_data(self, source):

        if source.hasImage():
            return True
        else:
            return super(TextEdit, self).can_insert_from_mime_data(source)

    def insert_from_mime_data(self, source):

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

        super(TextEdit, self).insert_from_mime_data(source)
