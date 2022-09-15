
import re
from sortFilterProxyModel import SortFilterProxyModel

SOUND_COLUMN = 0
DESCRIPTION_COLUMN = 1
CLASSIFICATION_COLUMN = 2


class SortWordsForSoundFilterProxyModel(SortFilterProxyModel):
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
        if(self.parentReference.soundFilterEnabled is True):
            soundFilterFound = self.checkForPattern(
                sourceRow, sourceParent, self.parentReference.soundFilterPattern, SOUND_COLUMN)
        else:
            soundFilterFound = False
        if(self.parentReference.soundDescriptionFilterEnabled is True):
            descriptionFilterFound = self.checkForPattern(
                sourceRow, sourceParent, self.parentReference.descriptionFilterPattern, DESCRIPTION_COLUMN)
        else:
            descriptionFilterFound = False

        if(self.parentReference.soundDescriptionFilterEnabled is True and descriptionFilterFound is False):
            includeDescriptionSearchResults = False
        else:
            includeDescriptionSearchResults = True
        if(self.parentReference.classificationFilterEnabled is True):
            classificationFilterFound = self.checkForPattern(
                sourceRow, sourceParent, self.parentReference.classificationFilterPattern, CLASSIFICATION_COLUMN)
        else:
            classificationFilterFound = False
        includeSoundSearchResults = self.parentReference.soundFilterEnabled and soundFilterFound
        if(self.parentReference.soundFilterEnabled is True and soundFilterFound is False):
            includeSoundSearchResults = False
        else:
            includeSoundSearchResults = True
        includeDescriptionSearchResults = self.parentReference.soundDescriptionFilterEnabled and descriptionFilterFound
        if(self.parentReference.soundDescriptionFilterEnabled is True and descriptionFilterFound is False):
            includeDescriptionSearchResults = False
        else:
            includeDescriptionSearchResults = True
        if(self.parentReference.classificationFilterEnabled is True and classificationFilterFound is False):
            includeClassificationSearchResults = False
        else:
            includeClassificationSearchResults = True
        if((includeSoundSearchResults is True) and (includeDescriptionSearchResults is True) and (includeClassificationSearchResults is True)):
            return True
        else:
            return False
