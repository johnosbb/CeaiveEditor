from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *


class PreferencesDialog(QDialog):

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __init__(self, parent):
        super().__init__()
        # font = QFont(parent.fontFamilies[0])
        # self.setFont(font)
        self.setWindowTitle("Lyrical Preferences")
        self.setGeometry(100, 100, 400, 200)  # X,Y, Width, Height
        QBtn = QDialogButtonBox.Cancel | QDialogButtonBox.Save

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        # Set up labels and line edit widgets
        self.projectHomeDirectorylabel = QLabel("Projects Home")
        self.projectHomeDirectoryEdit = QLineEdit()
        self.projectHomeDirectoryEdit.setText(parent.projectHomeDirectory)

        self.directoryButton = QPushButton(self)
        self.directoryButton.setText("...")  # text
        # self.directoryButton.setIcon(QIcon("close.png")) #icon
        self.directoryButton.setShortcut('Ctrl+D')  # shortcut key
        self.directoryButton.clicked.connect(parent.set_directory)
        self.directoryButton.setToolTip(
            "Select the Project Directory")  # Tool tip
        #self.directoryButton.move(100, 100)

        self.directoryLayout = QHBoxLayout()

        self.preferencesMainLayout = QVBoxLayout()
        self.directoryLayout.addWidget(self.projectHomeDirectorylabel)
        self.directoryLayout.addWidget(self.projectHomeDirectoryEdit)
        self.directoryLayout.addWidget(self.directoryButton)
        self.preferencesMainLayout.addLayout(self.directoryLayout)
        self.preferencesMainLayout.addStretch()
        self.preferencesMainLayout.addWidget(self.buttonBox)
        self.setLayout(self.preferencesMainLayout)
        self.center()
