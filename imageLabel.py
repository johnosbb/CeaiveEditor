# import necessary modules
import sys
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap
import resources


class ImageLabel(QLabel):

    def __init__(self, image, x, y, w, h):
        super().__init__()
        self.load_image(image, x, y, w, h)
        self.setStyleSheet(
            "background-color: #314B4A; border: 3px solid #314B4A;")

    def load_image(self, image, x, y, w, h):
        try:

            self.setScaledContents(True)
            self.setAlignment(Qt.AlignCenter)
            pixmap = QPixmap(image)
            self.setGeometry(x, y, w, h)
            pixmap = pixmap.scaled(
                self.size(), Qt.KeepAspectRatio)
            self.setPixmap(pixmap)
            self.move(x, y)

        except FileNotFoundError:
            print("Image not found.")
