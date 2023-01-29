from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import preferenceProperties


class PreferencesDialog(QDialog):

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setSelectedLanguage(self, language):
        self.properties.language = language

    def setSelectedFileFormat(self, format):
        self.properties.fileFormat = format

    def setSelectedTheme(self, theme):
        print("Setting selected {} theme from settings: current theme {}".format(
            theme, self.parent.theme))
        if(theme != self.parent.theme):
            self.properties.theme = theme
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(
                "You will need to restart the application to load the new theme")
            retval = msg.exec_()

    def __init__(self, parent):
        super().__init__()
        # font = QFont(parent.fontFamilies[0])
        # self.setFont(font)
        self.parent = parent
        self._properties = preferenceProperties.PreferenceProperties()
        self.setWindowTitle("Lyrical Preferences")
        self.setGeometry(100, 100, 600, 200)  # X,Y, Width, Height
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

        languageOptions = ["enu", "eng"]

        self.languageLayout = QHBoxLayout()
        self.languageSelect = QComboBox()

        self.languageSelect.currentTextChanged.connect(
            self.setSelectedLanguage)
        self.languageSelect.addItems(languageOptions)
        self.languageSelect.setCurrentText(parent.language)
        self.languageLabel = QLabel("Language")

        fileFormatOptions = ["html", "text"]
        self.languageSelect.setCurrentText(parent.fileFormat)

        self.fileFormatLayout = QHBoxLayout()
        self.fileFormatSelect = QComboBox()
        self.fileFormatSelect.currentTextChanged.connect(
            self.setSelectedFileFormat)
        self.fileFormatSelect.addItems(fileFormatOptions)
        self.fileFormatSelect.setCurrentText(parent.language)
        self.fileFormatLabel = QLabel("File Format")

        themeSelectOptions = ["dark", "light"]
        self.themeSelectLayout = QHBoxLayout()
        self.themeSelect = QComboBox()
        self.themeSelect.addItems(themeSelectOptions)
        self.themeSelect.setCurrentText(parent.theme)
        self.themeSelect.currentTextChanged.connect(
            self.setSelectedTheme)

        self.themeSelectLabel = QLabel("Theme")
        self.themeSelectLayout.addWidget(self.themeSelectLabel)
        self.themeSelectLayout.addWidget(self.themeSelect)

        self.directoryLayout = QHBoxLayout()
        self.preferencesMainLayout = QVBoxLayout()
        self.directoryLayout.addWidget(self.projectHomeDirectorylabel)
        self.directoryLayout.addWidget(self.projectHomeDirectoryEdit)
        self.directoryLayout.addWidget(self.directoryButton)
        self.preferencesMainLayout.addLayout(self.directoryLayout)
        self.languageLayout.addWidget(self.languageLabel)
        self.languageLayout.addWidget(self.languageSelect)
        self.fileFormatLayout.addWidget(self.fileFormatLabel)
        self.fileFormatLayout.addWidget(self.fileFormatSelect)
        self.preferencesMainLayout.addLayout(self.languageLayout)
        self.preferencesMainLayout.addLayout(self.fileFormatLayout)
        self.preferencesMainLayout.addLayout(self.themeSelectLayout)
        self.preferencesMainLayout.addStretch()
        self.preferencesMainLayout.addWidget(self.buttonBox)
        self.setLayout(self.preferencesMainLayout)
        self.center()

    @ property
    def properties(self):
        return self._properties

    @ properties.setter
    def properties(self, newProperty):
        self._properties = newProperty
