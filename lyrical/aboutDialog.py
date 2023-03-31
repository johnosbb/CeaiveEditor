from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)

        self.setWindowTitle('About')
        self.setFixedSize(800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)
        label = QLabel(self)
        pixmap = QPixmap(":/images/images/MiniSplash.png")
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        text = QLabel(self)
        text.setText('Lyrical Version 1.0.0')
        text.setAlignment(Qt.AlignCenter)
        layout.addWidget(text)
