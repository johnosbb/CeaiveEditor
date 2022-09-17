from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import imageLabel
import informationalLabel
import pushButton
import resources
import novelProperties
import logging


class NovelPropertiesDialog(QDialog):

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __init__(self, parent):
        super().__init__()
        self._properties = novelProperties.NovelProperties()
        self._project = "Novel"
        self.setWindowTitle("Set the Properties for your Project")
        # this will hide the title bar
        # self.setWindowFlag(Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 255, 322)  # X,Y, Width, Height
        self.setStyleSheet(
            "background-color: #E6E9CC; padding:1px 1px 1px 1px")

        self.mainLayout = QVBoxLayout()

        self.topPanelLayout = QHBoxLayout()

        self.foreword = QCheckBox("Foreword", self)
        self.preface = QCheckBox("Preface", self)
        self.introduction = QCheckBox("Introduction", self)
        self.prologue = QCheckBox("Prologue", self)
        self.epilogue = QCheckBox("Epilogue", self)

        self.createButton = pushButton.PushButton("Create")
        self.cancelButton = pushButton.PushButton("Cancel")
        self.createButton.clicked.connect(self.create_button_clicked)
        self.cancelButton.clicked.connect(self.cancel_button_clicked)

        self.ButtonFrame = QFrame(self)  # Create QFrame object
        size_policy = QSizePolicy(QSizePolicy.Expanding,
                                  QSizePolicy.Preferred)
        self.ButtonFrame.setSizePolicy(size_policy)
        self.ButtonFrame.setFrameShape(QFrame.Box)
        self.ButtonFrame.setFrameShadow(QFrame.Raised)
        self.ButtonFrame.setStyleSheet("background-color: #223232;")
        self.ButtonFrame.setLineWidth(1)

        self.PropertiesFrame = QFrame(self)  # Create QFrame object
        # size_policy = QSizePolicy(QSizePolicy.Expanding,
        #                           QSizePolicy.Preferred)
        # self.PropertiesFrame.setSizePolicy(size_policy)
        # self.PropertiesFrame.setFrameShape(QFrame.Box)
        # self.PropertiesFrame.setFrameShadow(QFrame.Raised)
        # self.PropertiesFrame.setStyleSheet("background-color: #223232;")
        # self.PropertiesFrame.setLineWidth(1)

        # self.ButtonFrame.setLineWidth(3)
        # self.ButtonFrame.setMidLineWidth(5)
        self.buttonPanelLayout = QHBoxLayout(self.ButtonFrame)

        self.buttonPanelLayout.addWidget(self.createButton)
        self.buttonPanelLayout.addWidget(self.cancelButton)

        self.propertiesPanelLayout = QVBoxLayout()
        self.propertiesPanelLayout.addWidget(self.foreword)
        self.propertiesPanelLayout.addWidget(self.preface)
        self.propertiesPanelLayout.addWidget(
            self.introduction)
        self.propertiesPanelLayout.addWidget(self.prologue)
        self.propertiesPanelLayout.addWidget(self.epilogue)

        # self.createButton.setStyleSheet('background-color:red')

        self.foreword.toggled.connect(
            lambda: self.set_foreword_state(self.foreword))
        self.preface.toggled.connect(
            lambda: self.set_preface_state(self.preface))
        self.introduction.toggled.connect(
            lambda: self.set_introduction_state(self.introduction))
        self.prologue.toggled.connect(
            lambda: self.set_prologue_state(self.prologue))
        self.epilogue.toggled.connect(
            lambda: self.set_epilogue_state(self.epilogue))

        self.numberOfChapters = QSpinBox()
        # setting prefix to spin
        self.numberOfChapters.setPrefix("Chapters ")
        self.numberOfChapters.setRange(0, 100)
        self.numberOfChapters.setGeometry(0, 0, 40, 40)
        self.numberOfChapters.valueChanged.connect(
            self.set_chapter_count)
        self.propertiesPanelLayout.addWidget(
            self.numberOfChapters)
        self.topPanelLayout.addLayout(
            self.propertiesPanelLayout)
        novelImage = ":/images/images/Novel.png"
        self.ImageLabelNovel = imageLabel.ImageLabel(
            novelImage, 520, 0, 255, 322)
        self.informationLabel = informationalLabel.InformationalLabel(
            "Select the properties you require for your novel.\nYou can modify properties and add chapters as your project progresses.")

        self.topPanelLayout.addWidget(self.ImageLabelNovel)
        self.mainLayout.addLayout(self.topPanelLayout)
        self.mainLayout.addWidget(self.informationLabel)
        self.mainLayout.addWidget(
            self.ButtonFrame)

        self.setLayout(self.mainLayout)
        self.center()

    @ property
    def project(self):
        return self._project

    @ project.setter
    def project(self, new_project):
        self._project = new_project

    def set_chapter_count(self):
        self.properties.numberOfChapters = self.numberOfChapters.value()
        logging.debug("Chapters Requested {}".format(self.properties.numberOfChapters))

    def set_foreword_state(self, cb):
        self.properties.foreword = cb.isChecked()
        if (self.properties.foreword == True):
            logging.debug("{} Selected".format(cb.text()))
        else:
            logging.debug("{} De-Selected".format(cb.text()))

    def set_prologue_state(self, cb):
        self.properties.prologue = cb.isChecked()
        if (self.properties.prologue == True):
            logging.debug("{} Selected".format(cb.text()))
        else:
            logging.debug("{} De-Selected".format(cb.text()))

    def set_epilogue_state(self, cb):
        self.properties.epilogue = cb.isChecked()
        if (self.properties.epilogue == True):
            logging.debug("{} Selected".format(cb.text()))
        else:
            logging.debug("{} De-Selected".format(cb.text()))

    def set_preface_state(self, cb):
        self.properties.preface = cb.isChecked()
        if (self.properties.preface == True):
            logging.debug("{} Selected".format(cb.text()))
        else:
            logging.debug("{} De-Selected".format(cb.text()))

    def set_introduction_state(self, cb):
        self.properties.introduction = cb.isChecked()
        if (self.properties.introduction == True):
            logging.debug("{} Selected".format(cb.text()))
        else:
            logging.debug("{} De-Selected".format(cb.text()))

    def create_button_clicked(self):
        logging.debug("Create button clicked")
        self.accept()

    def cancel_button_clicked(self):
        logging.debug("Create button clicked")
        self.close()

    @ property
    def properties(self):
        return self._properties

    @ properties.setter
    def properties(self, newProperty):
        self._properties = newProperty
