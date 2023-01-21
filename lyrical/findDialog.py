# PYQT5 PyQt4’s QtGui module has been split into PyQt5’s QtGui, QtPrintSupport and QtWidgets modules

from PyQt5 import QtWidgets
# PYQT5 QTextEdit, QDialog, QPushButton, QRadioButton, QGridLayout
import imageBox
import pushButton
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
import globals
import re


class Find(QtWidgets.QDialog):
    def __init__(self, parent=None):

        QtWidgets.QDialog.__init__(self, parent)

        self.parent = parent

        self.lastStart = 0

        self.initUI()

    def initUI(self):

        IMAGE_WIDTH = 46
        IMAGE_HEIGHT = 62
        #IMAGE_WIDTH = 92
        #IMAGE_HEIGHT = 124
        # Button to search the document for something
        #findButton = QtWidgets.QPushButton("Find", self)
        findButton = pushButton.PushButton("Find")
        findButton.clicked.connect(self.find)

        # Button to replace the last finding
        replaceButton = pushButton.PushButton("Replace")
        replaceButton.clicked.connect(self.replace)

        # Button to remove all findings
        allButton = pushButton.PushButton("Replace All")
        allButton.clicked.connect(self.replaceAll)

        # Normal mode - radio button
        self.normalRadio = QtWidgets.QRadioButton("Normal", self)

        # Regular Expression Mode - radio button
        regexRadio = QtWidgets.QRadioButton("RegEx", self)

        # The field into which to type the query
        searchImage = ":/images/images/SearchImage.png"
        self.searchImageBox = imageBox.ImageBox(
            searchImage, 0, 0, IMAGE_WIDTH, IMAGE_HEIGHT)
        self.findField = QtWidgets.QTextEdit(self)
        if(globals.USE_STYLESHEETS_FOR_COLOR):
            self.findField.setStyleSheet(
                "background-color: #FFFFFF; padding:1px 1px 1px 1px")
        self.findField.resize(250, 50)

        # The field into which to type the text to replace the
        # queried text
        replaceImage = ":/images/images/Replace.png"
        self.replaceImageBox = imageBox.ImageBox(
            replaceImage, 0, 0, IMAGE_WIDTH, IMAGE_HEIGHT)
        self.replaceField = QtWidgets.QTextEdit(self)
        if(globals.USE_STYLESHEETS_FOR_COLOR):
            self.replaceField.setStyleSheet(
                "background-color: #FFFFFF; padding:1px 1px 1px 1px")
        self.replaceField.resize(250, 50)
        if(globals.USE_STYLESHEETS_FOR_COLOR):
            self.setStyleSheet(
                "background-color: #E6E9CC; padding:1px 1px 1px 1px")
        layout = QtWidgets.QGridLayout()
        # addWidget(widget, row,column, rowSpan, columnSpan,alignment)
        layout.addWidget(self.searchImageBox, 1, 0, 1, 1)
        layout.addWidget(self.findField, 1, 1, 1, 4)
        layout.addWidget(self.normalRadio, 2, 2)
        layout.addWidget(regexRadio, 2, 3)
        layout.addWidget(findButton, 2, 0, 1, 2)

        layout.addWidget(self.replaceImageBox, 3, 0, 1, 1)
        layout.addWidget(self.replaceField, 3, 1, 1, 4)
        layout.addWidget(replaceButton, 4, 0, 1, 2)
        layout.addWidget(allButton, 4, 3, 1, 2)

        self.setGeometry(300, 300, 360, 250)
        self.setWindowTitle("Find and Replace")
        self.setLayout(layout)

        # By default the normal mode is activated
        self.normalRadio.setChecked(True)

    def find(self):

        # Grab the parent's text
        text = self.parent.editor.toPlainText()

        # And the text to find
        query = self.findField.toPlainText()

        if self.normalRadio.isChecked():

            # Use normal string search to find the query from the
            # last starting position
            self.lastStart = text.find(query, self.lastStart + 1)

            # If the find() method didn't return -1 (not found)
            if self.lastStart >= 0:

                end = self.lastStart + len(query)

                self.moveCursor(self.lastStart, end)

            else:

                # Make the next search start from the beginning again
                self.lastStart = 0

                self.parent.editor.moveCursor(QtGui.QTextCursor.End)
                self.parent.update_status_bar(
                    "No matching text found for {}".format(query))

        else:

            # Compile the pattern
            pattern = re.compile(query)

            # The actual search
            match = pattern.search(text, self.lastStart + 1)

            if match:

                self.lastStart = match.start()

                self.moveCursor(self.lastStart, match.end())

            else:

                self.lastStart = 0

                # We set the cursor to the end if the search was unsuccessful
                self.parent.editor.moveCursor(QtGui.QTextCursor.End)
                self.parent.update_status_bar(
                    "No matching text found for expression {}".format(pattern))

    def replace(self):

        # Grab the text cursor
        cursor = self.parent.editor.textCursor()

        # Security
        if cursor.hasSelection():

            # We insert the new text, which will override the selected
            # text
            cursor.insertText(self.replaceField.toPlainText())

            # And set the new cursor
            self.parent.editor.setTextCursor(cursor)

    def replaceAll(self):

        self.lastStart = 0

        self.find()

        # Replace and find until self.lastStart is 0 again
        while self.lastStart:
            self.replace()
            self.find()

    def moveCursor(self, start, end):

        # We retrieve the QTextCursor object from the parent's QTextEdit
        cursor = self.parent.editor.textCursor()

        # Then we set the position to the beginning of the last match
        cursor.setPosition(start)

        # Next we move the Cursor by over the match and pass the KeepAnchor parameter
        # which will make the cursor select the the match's text
        cursor.movePosition(QtGui.QTextCursor.Right,
                            QtGui.QTextCursor.KeepAnchor, end - start)

        # And finally we set this new cursor as the parent's
        self.parent.editor.setTextCursor(cursor)
