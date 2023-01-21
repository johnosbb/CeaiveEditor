# import necessary modules
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
import globals
import resources


class PushButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        # fontId = QFontDatabase.addApplicationFont(
        #     ':/fonts/fonts/Amarante-Regular.ttf')
        if(globals.USE_STYLESHEETS_FOR_COLOR):
            self.setStyleSheet("QPushButton{color:#E6E9CC}"
                               "QPushButton:hover{color:#FFFFFF}"
                               "QPushButton{background-color:#5F8A77}"
                               "QPushButton{border:2px solid black}"
                               # determines the corner radius
                               "QPushButton{border-radius:5px}"
                               "QPushButton{padding:2px 2px}"
                               "QPushButton:pressed{background-color:#F5F6EB; color:black; border:2px solid white;}"
                               )
        # self.fontFamilies = QFontDatabase.applicationFontFamilies(fontId)
        # font = QFont(self.fontFamilies[0])
        # self.setFont(font)
        # self.setText(text)
