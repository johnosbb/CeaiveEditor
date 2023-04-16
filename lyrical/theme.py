from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Theme():

    def __init__(self) -> None:
        super().__init__()
        self.__lightPalette = QPalette()
        self.__darkPalette = QPalette()
        self.__lyricalPalette = QPalette()
        self.createDarkPalette()
        self.createLightPalette()
        self.createLyricalPalette()

    def createDarkPalette(self):

        self.__darkPalette.setColor(QPalette.Window, QColor(
            53, 53, 53))  # a dark grey, almost black A general background color.
        # A general foreground color.
        self.__darkPalette.setColor(QPalette.WindowText, Qt.white)
        self.__darkPalette.setColor(QPalette.Base, QColor(
            25, 25, 25))  # a dark grey, almost black Used mostly as the background color for text entry widgets, but can also be used for other painting - such as the background of combobox drop down lists and toolbar handles. It is usually white or another light color.
        self.__darkPalette.setColor(QPalette.AlternateBase,
                                    QColor(53, 53, 53))  # a dark grey, almost black Used as the alternate background color in views with alternating row colors
        self.__darkPalette.setColor(QPalette.ToolTipBase, Qt.white)
        self.__darkPalette.setColor(QPalette.ToolTipText, Qt.black)
        # The foreground color used with Base. This is usually the same as the WindowText, in which case it must provide good contrast with Window and Base.
        self.__darkPalette.setColor(QPalette.Text, Qt.white)
        self.__darkPalette.setColor(QPalette.Button, QColor(
            53, 53, 53))  # a dark grey, almost black
        # A foreground color used with the Button color.
        self.__darkPalette.setColor(QPalette.ButtonText, Qt.white)
        # A text color that is very different from WindowText, and contrasts well with e.g. Dark. Typically used for text that needs to be drawn where Text or WindowText would give poor contrast, such as on pressed push buttons. Note that text colors can be used for things other than just words; text colors are usually used for text, but it's quite common to use the text color roles for lines, icons, etc.
        self.__darkPalette.setColor(QPalette.BrightText, Qt.red)
        self.__darkPalette.setColor(QPalette.Link, QColor(
            42, 130, 218))  # a mid range blue
        self.__darkPalette.setColor(QPalette.Highlight, QColor(
            42, 130, 218))  # a mid range blue
        self.__darkPalette.setColor(QPalette.HighlightedText, Qt.black)

    def createLightPalette(self):

        self.__lightPalette.setColor(QPalette.Window, QColor(
            202, 202, 202))  # a light grey
        self.__lightPalette.setColor(QPalette.WindowText, QColor(
            53, 53, 53))  # a dark grey, almost black
        self.__lightPalette.setColor(QPalette.Base, QColor(
            230, 230, 230))  # a lighter grey
        self.__lightPalette.setColor(QPalette.AlternateBase,
                                     QColor(202, 202, 202))
        self.__lightPalette.setColor(QPalette.ToolTipBase, QColor(
            53, 53, 53))  # a dark grey, almost black
        self.__lightPalette.setColor(QPalette.ToolTipText, QColor(
            202, 202, 202))  # a light grey
        self.__lightPalette.setColor(QPalette.Text, QColor(
            53, 53, 53))  # a dark grey, almost black
        self.__lightPalette.setColor(QPalette.Button, QColor(
            202, 202, 202))  # a light grey
        self.__lightPalette.setColor(QPalette.ButtonText, QColor(53, 53, 53))
        self.__lightPalette.setColor(QPalette.BrightText, Qt.red)
        self.__lightPalette.setColor(QPalette.Link, QColor(
            42, 130, 218))  # a mid range blue
        self.__lightPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        self.__lightPalette.setColor(QPalette.HighlightedText,
                                     QColor(202, 202, 202))  # a light grey

    def createLyricalPalette(self):

        self.__lyricalPalette.setColor(QPalette.Window, QColor(
            245, 246, 234))  # a light green E6E9CC
        self.__lyricalPalette.setColor(QPalette.WindowText, QColor(
            49, 75, 74))  # a dark green, almost black
        self.__lyricalPalette.setColor(QPalette.Base, QColor(
            249, 249, 242))  # a lighter green
        self.__lyricalPalette.setColor(QPalette.AlternateBase,
                                       QColor(230, 233, 204))
        self.__lyricalPalette.setColor(QPalette.ToolTipBase, QColor(
            30, 59, 59))  # a dark green, almost black
        self.__lyricalPalette.setColor(QPalette.ToolTipText, QColor(
            245, 246, 234))  # a lighter green
        self.__lyricalPalette.setColor(QPalette.Text, QColor(
            31, 47, 46))  # a dark green, almost black
        self.__lyricalPalette.setColor(QPalette.Button, QColor(
            203, 198, 165))  # a light green
        self.__lyricalPalette.setColor(
            QPalette.ButtonText, QColor(31, 47, 46))
        self.__lyricalPalette.setColor(
            QPalette.BrightText, QColor(251, 124, 43))
        self.__lyricalPalette.setColor(QPalette.Link, QColor(
            233, 172, 41))  # a mid range orange
        self.__lyricalPalette.setColor(
            QPalette.Highlight, QColor(251, 124, 43))
        self.__lyricalPalette.setColor(QPalette.HighlightedText,
                                       QColor(240, 241, 224))  # a light green

    @ property
    def darkPalette(self):
        return self.__darkPalette

    @ darkPalette.setter
    def darkPalette(self, value):
        self._darkPalette = value

    @ property
    def lightPalette(self):
        return self.__lightPalette

    @ lightPalette.setter
    def lightPalette(self, value):
        self._lightPalette = value

    @ property
    def lyricalPalette(self):
        return self.__lyricalPalette

    @ lyricalPalette.setter
    def lyricalPalette(self, value):
        self._lyricalPalette = value
