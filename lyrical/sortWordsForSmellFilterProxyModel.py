
import re
from sortFilterProxyModel import SortFilterProxyModel

SMELL_COLUMN = 0
CLASSIFICATION_COLUMN = 1


class SortWordsForSmellFilterProxyModel(SortFilterProxyModel):
    def __init__(self, parent):
        # the dialog or class that is requesting the filter, in our case the wordSelectorDialog
        self.parentReference = parent
        super().__init__(parent)

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
        # self.dumpModel(sourceParent)
        # self.dumpRow(sourceParent, sourceRow)
        # self.filterKeyColumn is set by self.proxyModel.setFilterKeyColumn()
        if(self.parentReference.smellFilterEnabled is True):
            smellFilterFound = self.checkForPattern(
                sourceRow, sourceParent, self.parentReference.smellFilterPattern, SMELL_COLUMN)
        else:
            smellFilterFound = False
        if(self.parentReference.classificationFilterEnabled is True):
            classificationFilterFound = self.checkForPattern(
                sourceRow, sourceParent, self.parentReference.classificationFilterPattern, CLASSIFICATION_COLUMN)
        else:
            classificationFilterFound = False
        includeSmellSearchResults = self.parentReference.smellFilterEnabled and smellFilterFound
        if(self.parentReference.smellFilterEnabled is True and smellFilterFound is False):
            includeSmellSearchResults = False
        else:
            includeSmellSearchResults = True

        if(self.parentReference.classificationFilterEnabled is True and classificationFilterFound is False):
            includeClassificationSearchResults = False
        else:
            includeClassificationSearchResults = True
        if((includeSmellSearchResults is True) and (includeClassificationSearchResults is True)):
            return True
        else:
            return False
