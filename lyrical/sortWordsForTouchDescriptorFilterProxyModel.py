
import re
from sortFilterProxyModel import SortFilterProxyModel

DESCRIPTOR_COLUMN = 0
DESCRIPTION_COLUMN = 1
CLASSIFICATION_COLUMN = 2


class SortWordsForTouchDescriptorFilterProxyModel(SortFilterProxyModel):
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
        if(self.parentReference.touchDescriptorFilterEnabled is True):
            TouchDescriptorFilterFound = self.checkForPattern(
                sourceRow, sourceParent, self.parentReference.touchDescriptorFilterPattern, DESCRIPTOR_COLUMN)
        else:
            TouchDescriptorFilterFound = False
        if(self.parentReference.meaningFilterEnabled is True):
            meaningFilterFound = self.checkForPattern(
                sourceRow, sourceParent, self.parentReference.meaningFilterPattern, MEANING_COLUMN)
        else:
            meaningFilterFound = False
        if(self.parentReference.classificationFilterEnabled is True):
            classificationFilterFound = self.checkForPattern(
                sourceRow, sourceParent, self.parentReference.classificationFilterPattern, CLASSIFICATION_COLUMN)
        else:
            classificationFilterFound = False
        includeTouchSearchResults = self.parentReference.touchDescriptorFilterEnabled and TouchDescriptorFilterFound
        if(self.parentReference.touchDescriptorFilterEnabled is True and TouchDescriptorFilterFound is False):
            includeTouchSearchResults = False
        else:
            includeTouchSearchResults = True
        includeMeaningSearchResults = self.parentReference.meaningFilterEnabled and meaningFilterFound
        if(self.parentReference.meaningFilterEnabled is True and meaningFilterFound is False):
            includeMeaningSearchResults = False
        else:
            includeMeaningSearchResults = True
        if(self.parentReference.classificationFilterEnabled is True and classificationFilterFound is False):
            includeClassificationSearchResults = False
        else:
            includeClassificationSearchResults = True
        if((includeTouchSearchResults is True) and (includeMeaningSearchResults is True) and (includeClassificationSearchResults is True)):
            return True
        else:
            return False
