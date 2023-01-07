from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAction


class SpecialActionBlock(QAction):

    @property
    def name(self):
        return self.__class__.__name__

    actionTriggered = pyqtSignal(str, object, int)

    def __init__(self, word, menu, rule, blockNumber):
        super().__init__(word, menu)
        # for arg in args:
        #     print("arg: {}".format(arg))
        self.triggered.connect(self.emitTriggered)
        self.__blockNumber = blockNumber
        self.__rule = rule

    def emitTriggered(self):
        # print("Class Name: " + self.name)
        # self.dumpObjectInfo()
        # text in this instance will be the descriptive text associated with this action
        self.actionTriggered.emit(self.text(), self.__rule, self.__blockNumber)
