# import necessary modules
import sys
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap
import resources
import globals


class ColorTile(QLabel):
    """
    Define a signal change_style that takes no arguments.
    """
    clicked = pyqtSignal()

    def __init__(self, x, y, w, h, color):
        super().__init__()
        if(globals.USE_STYLESHEETS_FOR_COLOR):
            stylesheet = "background-color: {}; border: 3px solid #314B4A;".format(
                color)
            self.setStyleSheet(
                stylesheet)
        self.createTile(x, y, w, h)

    # def enterEvent(self, event):
    #     self.setStyleSheet("border: 3px solid #000000;")

    # def leaveEvent(self, event):
    #     self.setStyleSheet(
    #         "background-color: #314B4A; border: 3px solid #314B4A;")

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.clicked.emit()

    def createTile(self, x, y, w, h):
        self.setAlignment(Qt.AlignCenter)
        self.setGeometry(x, y, w, h)
        self.move(x, y)
