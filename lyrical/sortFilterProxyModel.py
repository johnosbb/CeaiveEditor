from PyQt5.QtCore import Qt, QSortFilterProxyModel
from pprint import pprint
import re

WORD_COLUMN = 0
MEANING_COLUMN = 1
TAG_COLUMN = 2
CLASSIFICATION_COLUMN = 3


class SortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent):
        # the dialog or class that is requesting the filter, in our case the wordSelectorDialog
        self.parentReference = parent
        super().__init__()

    def checkForPattern(self, sourceRow, sourceParent, pattern, column):
        index = self.sourceModel().index(
            sourceRow, column, sourceParent)
        rawData = self.sourceModel().data(index)

        # print("Pattern: " +pattern + ", RawData: " + rawData)
        if((rawData is not None) and (not pattern.isspace()) and (pattern != "")):
            data = rawData.lstrip()
            # Note that the result raw string has the quote at the beginning and end of the string. To remove them, you can use slices: [1:-1]
            if(re.search(pattern.lower(), data.lower())):
                return True
            else:
                return False
        else:
            return False

    def filterAcceptsRow(self, sourceRow, sourceParent):
        # Do we filter for the date column?
        if self.filterKeyColumn() == DATE:
            # Fetch datetime value.
            index = self.sourceModel().index(sourceRow, DATE, sourceParent)
            data = self.sourceModel().data(index)
            # Return, if regExp match in displayed format.
            return (self.filterRegExp().indexIn(data.toString(Qt.DefaultLocaleShortDate)) >= 0)
        # Not our business.
        return super(SortFilterProxyModel, self).filterAcceptsRow(sourceRow, sourceParent)

    def dumpModel(self, sourceParent):
        rowCount = self.sourceModel().rowCount()
        columnCount = self.sourceModel().columnCount()
        for row in range(rowCount):
            data = ""
            for column in range(columnCount):
                index = self.sourceModel().index(
                    row, column, sourceParent)
                rawData = self.sourceModel().data(index)
                data = data + str(column) + " : " + rawData
            print(str(row) + " : " + data)

    def dumpRow(self, sourceParent, sourceRow):
        data = ""
        columnCount = self.sourceModel().columnCount()
        for column in range(columnCount):
            index = self.sourceModel().index(
                sourceRow, column, sourceParent)
            rawData = self.sourceModel().data(index)
            data = data + str(column) + " : " + rawData
        print(" Row:" + str(sourceRow) + ", Column Count: " +
              str(columnCount) + "  " + data)
