# import necessary modules
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
import globals
import resources


class InformationalLabel(QLabel):
    def __init__(self, text):
        super().__init__()
        fontId = QFontDatabase.addApplicationFont(
            ':/fonts/fonts/Amarante-Regular.ttf')
        if(globals.USE_STYLESHEETS_FOR_COLOR):
            self.setStyleSheet(
                "background-color: #C99958; border: 1px solid #5F8A77; padding:4px 4px;")

        self.fontFamilies = QFontDatabase.applicationFontFamilies(fontId)
        font = QFont(self.fontFamilies[0])
        self.setFont(font)
        self.setText(text)
