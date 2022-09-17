import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont

# from spellCheck import SpellCheck
from spellCheckWord import SpellCheckWord

class SpellCheckHighlighter(QSyntaxHighlighter):
    wordRegEx = re.compile(r"\b([A-Za-z]{2,})\b")

    def highlightBlock(self, text: str) -> None:
        if not hasattr(self, "speller"):
            return

        # The character format of text in a document specifies the visual properties of the text, as well as information about its role in a hypertext document.
        self.misspelledFormat = QTextCharFormat()
        self.misspelledFormat.setUnderlineStyle(
            QTextCharFormat.SpellCheckUnderline)  # we can set its visual style
        self.misspelledFormat.setUnderlineColor(Qt.red)  # red and underlined

        # we iterate the text using the regular expression above which identifies word boundaries
        for word_object in self.wordRegEx.finditer(text):
            # we check to see if this is a recognised word
            if not self.speller.check(word_object.group()):
                self.setFormat(    # if it is not we underline it using the style shown above
                    word_object.start(),  # index of first letter of match
                    # index of last letter - index of first letter= length
                    word_object.end() - word_object.start(),
                    self.misspelledFormat,
                )

    def setSpeller(self, speller: SpellCheckWord):
        self.speller = speller
