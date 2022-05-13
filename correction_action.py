from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAction


class SpecialAction(QAction):

    @property
    def name(self):
        return self.__class__.__name__

    actionTriggered = pyqtSignal(str)

    def __init__(self, *args):
        super().__init__(*args)

        self.triggered.connect(self.emitTriggered)

    def emitTriggered(self):
        print("Class Name: " + self.name)
        # self.dumpObjectInfo()
        # text in this instance will be the descriptive text associated with this action
        self.actionTriggered.emit(self.text())
