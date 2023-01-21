from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import imageBox
import resources
import globals


class ProjectTypeDialog(QDialog):

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __init__(self, parent):
        super().__init__()
        self._project = "Novel"
        font = QFont(parent.fontFamilies[0])
        self.setFont(font)
        self.setWindowTitle("Select a Project Type")
        self.setGeometry(100, 100, 780, 330)  # X,Y, Width, Height
        QBtn = QDialogButtonBox.Cancel
        self.projectSelectorMainLayout = QHBoxLayout()
        essayImage = ":/images/images/EssayButton.png"
        shortStoryImage = ":/images/images/ShortStoryButton.png"
        novelImage = ":/images/images/NovelButton.png"
        self.imageBoxShortStory = imageBox.ImageBox(
            shortStoryImage, 0, 0, 255, 322)
        self.imageBoxEssay = imageBox.ImageBox(
            essayImage, 260, 0, 255, 322)
        self.imageBoxNovel = imageBox.ImageBox(
            novelImage, 520, 0, 255, 322)
        if(globals.USE_STYLESHEETS_FOR_COLOR):
            self.setStyleSheet("background-color: #E6E9CC;")
        self.projectSelectorMainLayout.addWidget(self.imageBoxShortStory)
        self.projectSelectorMainLayout.addWidget(self.imageBoxEssay)
        self.projectSelectorMainLayout.addWidget(self.imageBoxNovel)
        self.imageBoxShortStory.clicked.connect(
            lambda: self.set_project("ShortStory"))
        self.imageBoxEssay.clicked.connect(lambda: self.set_project("Essay"))
        self.imageBoxNovel.clicked.connect(lambda: self.set_project("Novel"))
        self.imageBoxNovel.setStyleSheet("QLabel::hover"
                                         "{"
                                         " border: 4px solid #d0d0d0;"
                                         "}")
        self.setLayout(self.projectSelectorMainLayout)
        self.center()

    @property
    def project(self):
        return self._project

    @project.setter
    def project(self, new_project):
        self._project = new_project

    def set_project(self, choice):
        self.project = choice
        self.accept()
