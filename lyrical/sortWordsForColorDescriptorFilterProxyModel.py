
import re
from sortFilterProxyModel import SortFilterProxyModel

DESCRIPTOR_COLUMN = 0
DESCRIPTION_COLUMN = 1
CLASSIFICATION_COLUMN = 2


class SortWordsForColorDescriptorFilterProxyModel(SortFilterProxyModel):
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
        if(self.parentReference.colourDescriptorFilterEnabled is True):
            colourDescriptorFilterFound = self.checkForPattern(
                sourceRow, sourceParent, self.parentReference.colourDescriptorFilterPattern, DESCRIPTOR_COLUMN)
        else:
            colourDescriptorFilterFound = False
        if(self.parentReference.classificationFilterEnabled is True):
            classificationFilterFound = self.checkForPattern(
                sourceRow, sourceParent, self.parentReference.classificationFilterPattern, CLASSIFICATION_COLUMN)
        else:
            classificationFilterFound = False
        includeColourSearchResults = self.parentReference.colourDescriptorFilterEnabled and colourDescriptorFilterFound
        if(self.parentReference.colourDescriptorFilterEnabled is True and colourDescriptorFilterFound is False):
            includeColourSearchResults = False
        else:
            includeColourSearchResults = True

        if(self.parentReference.classificationFilterEnabled is True and classificationFilterFound is False):
            includeClassificationSearchResults = False
        else:
            includeClassificationSearchResults = True
        if((includeColourSearchResults is True) and (includeClassificationSearchResults is True)):
            return True
        else:
            return False
