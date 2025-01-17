from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import re

import os
import sys
import uuid

# from pydantic import DirectoryPath


import style
import utilities
import logging
from theme import Theme
import preferencesDialog
import projectTypeDialog
import novelPropertiesDialog
import textEditor
import resources
import spellCheckWord
from customFileSystemModel import CustomFileSystemModel
import thesaurusWebster
import describeWord
import findDialog
from specialAction import SpecialAction
from PyQt5.QtCore import QEvent
from grammarCheckWindow import GrammarCorrectionWindow
from lintCheckWindow import LintCorrectionWindow
import language_tool_python
from wordListManager import WordListManager
import globals

from aboutDialog import AboutDialog

FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14,
              18, 24, 36, 48, 64, 72, 96, 144, 288]
IMAGE_EXTENSIONS = ['.jpg', '.png', '.bmp']
HTML_EXTENSIONS = ['.htm', '.html', '.txt']

# When creating a QSettings object, you must pass the name of your company or organization as well as the name of your application.
ORGANIZATION_NAME = 'Lyrical-Editor'
ORGANIZATION_DOMAIN = 'lyrical-editor.com'
APPLICATION_NAME = 'Lyrical-Editor'
SETTINGS_TRAY = 'settings/tray'
TEST_TEXT = "This is the first sentence. This is the second sentence. This is the third sentence. This is the fourth sentence. \
This is the fifth sentence. This is the sixth sentence. This is the seventh sentence. This is the eight sentence."


# Get logger
logger = logging.getLogger("my logger")

# Create a handler
c_handler = logging.StreamHandler()

# link handler to logger
logger.addHandler(c_handler)

# Set logging level to the logger
logger.setLevel(logging.DEBUG)


def hexuuid():
    return uuid.uuid4().hex

# Split the path name into a pair root and ext.
# Here, ext stands for extension and has the extension portion of the specified path while root is everything except ext part.


def splitext(p):
    return os.path.splitext(p)[1].lower()


class SplashScreen(QSplashScreen):
    def __init__(self):
        super(QSplashScreen, self).__init__()
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        pixmap = QPixmap("splash.png")
        self.setPixmap(pixmap)

    def closeSplash(self):
        self.close()

    def delayedClose(self):
        QTimer.singleShot(2000, self.closeSplash)


class MainWindow(QMainWindow):

    def __init__(self, appContext, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.load_settings()
        self.colorTheme = Theme()
        self.setWindowIcon(QIcon(":/images/images/logo.png"))
        self.resourcePath = getattr(
            sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        logging.debug(
            "The resource path is located at {}".format(self.resourcePath))
        if(self.theme == "light"):
            self.palette = self.colorTheme.lightPalette
            appContext.setPalette(self.palette)
        elif(self.theme == "lyrical"):
            self.palette = self.colorTheme.lyricalPalette
            appContext.setPalette(self.palette)
        else:
            self.palette = self.colorTheme.darkPalette
            appContext.setPalette(self.palette)
        self.word_list_path = "./local_dictionary.txt"
        layout = QVBoxLayout()  # The QVBoxLayout class lines up widgets vertically
        # this is using the editor class based on QTextEdit above, this is a new member declaration
        self.speller = spellCheckWord.SpellCheckWord(
            self.getWords(), self.addToDictionary)
        self.thesaurus = thesaurusWebster.ThesaurusWebster(self.websterAPIkey
                                                           )
        self.compliment = describeWord.DescribeWord(
        )
        self.editor = textEditor.TextEdit(
            self.speller, self.thesaurus, self.compliment)
        self.editor.showSuggestionSignal.connect(self.updateSuggestions)
        self.editor.updateStatusSignal.connect(self.update_status_bar)
        # Setup the QTextEdit editor configuration
        self.editor.setAutoFormatting(QTextEdit.AutoAll)
        self.editor.selectionChanged.connect(self.update_format)
        self.editor.cursorPositionChanged.connect(self.cursorPosition)
        self.editor.installEventFilter(self)
        self.projectType = "Novel"
        # # enable this for a frameless window
        # # Borderless window code begins
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.center()
        # #self.setFixedSize(320, 450)
        # self.setStyleSheet(
        #     "QMainWindow{background-color: darkgray;border: 1px solid black}")
        # # Borderless window code ends
        # self.path holds the path of the currently open file.
        # If none, we haven't got a file open yet (or creating new).
        self.path = None
        self.originalFormat = self.editor.currentCharFormat()
        layout.addWidget(self.editor)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setup_status_bar()
        self.define_file_toolbar()
        self.define_edit_toolbar()
        self.define_format_toolbar()
        self.addToolBarBreak()
        self.define_style_toolbar()
        self.define_word_list_toolbar()
        self.define_about_toolbar()
        self.addToolBarBreak()
        self.define_suggestions_toolbar()
        self.defineFileExplorerTreeView()
        # Initialize.
        self.update_format()
        self.update_title()
        self.oldPos = self.pos()
        # self.setWindowFlag(Qt.WindowStaysOnTopHint)

    @staticmethod
    def restart():
        MainWindow.singleton = MainWindow()

    def loadInBackground(self):
        print("Loading language tool")
        self.languageTool = language_tool_python.LanguageTool('en-GB')
        print("Loaded language tool")
        self.grammarCheck = GrammarCorrectionWindow(self.languageTool)
        self.lintCheck = LintCorrectionWindow()

    def define_suggestions_toolbar(self):
        """
        Defines the tools bar and actions associated with suggestions analysis
        """
        self.suggestions_toolbar = QToolBar("suggestions")
        self.suggestions_toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(self.suggestions_toolbar)
        self.suggestions_dock = QDockWidget("Suggestions", self)
        self.suggestions_dock.setWidget(self.suggestions_toolbar)
        self.suggestions_dock.setFloating(False)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.suggestions_dock)

    def eventFilter(self, source, event):
        if (event.type() == QEvent.FocusOut and source is self.editor and (len(self.editor.toPlainText()) > 0)):
            self.file_save()
        # return true here to bypass default behaviour
        return super(MainWindow, self).eventFilter(source, event)

    def update_suggestions_toolbar(self, suggestions):
        self.suggestions_toolbar.clear()
        for word in range(len(suggestions)):
            replace_word_action = SpecialAction(
                suggestions[word], self)
            replace_word_action.actionTriggered.connect(
                self.replace_word_in_editor)
            self.suggestions_toolbar.addAction(replace_word_action)

    def setup_status_bar(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.statusMode = QLabel("Left")
        self.status.addPermanentWidget(self.statusMode)
        self.statusContext = QLabel("Context")
        self.status.addPermanentWidget(self.statusContext)

    def update_status_bar(self, message):
        self.status.showMessage(
            "{}".format(message), 2000)

    def load_font(self):
        fontId = QFontDatabase.addApplicationFont(
            ':/fonts/fonts/Amarante-Regular.ttf')
        if fontId < 0:
            print('font not loaded')
        else:
            self.fontFamilies = QFontDatabase.applicationFontFamilies(fontId)
            font = QFont(self.fontFamilies[0])

    def getWords(self) -> list[str]:
        if not os.path.exists(self.word_list_path):
            open(self.word_list_path, 'w')
        with open(self.word_list_path, "r") as f:
            word_list = [line.strip() for line in f]
        return word_list

    def addToDictionary(self, new_word: str):
        with open(self.word_list_path, "a") as f:
            f.write("\n" + new_word)

    def show_preferences(self, s):
        self.preferencesDialog = preferencesDialog.PreferencesDialog(self)

        if self.preferencesDialog.exec():
            self.projectHomeDirectory = self.preferencesDialog.projectHomeDirectoryEdit.text()
            self.language = self.preferencesDialog.properties.language
            self.fileFormat = self.preferencesDialog.properties.fileFormat
            self.theme = self.preferencesDialog.properties.theme
            self.websterAPIkey = self.preferencesDialog.properties.websterAPIKey
        else:
            logging.debug("lyrical :Canceled Showing Preferences!")

    # def mouseMoveEvent(self, event):
    #     delta = QPoint(event.globalPos() - self.oldPos)
    #     self.move(self.x() + delta.x(), self.y() + delta.y())
    #     self.oldPos = event.globalPos()

    def block_signals(self, objects, b):
        for o in objects:
            o.blockSignals(b)

    def updateUi(self, arg=None):
        self.save_file_action.setEnabled(
            self.editor.document().isModified())
        self.saveas_file_action.setEnabled(
            not self.editor.document().isEmpty())
        enable = self.editor.textCursor().hasSelection()
        self.copy_action.setEnabled(enable)
        self.edit_action.setEnabled(enable)
        self.paste_action.setEnabled(self.editor.canPaste())

    def highlightWordYellow(self):
        backGroundColor = QColor(Qt.yellow).lighter()
        foreGroundColor = QColor(Qt.blue)
        format = QTextCharFormat()
        format.setBackground(QBrush(backGroundColor))
        format.setForeground(QBrush(foreGroundColor))
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(format)

    def highlightWordRed(self):
        color = QColor(Qt.red)
        format = QTextCharFormat()
        format.setBackground(QBrush(color))
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(format)

    def unHighlightWord(self):
        format = QTextCharFormat()
        format.clearBackground()
        format.clearForeground()
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        # font = currentFormat.font().family()
        font = self.editor.currentFont()
        format.setFont(font)
        cursor.setCharFormat(format)

    def removeMultipleFonts(self):
        html = self.editor.document().toHtml()
        htmlTransformed = re.sub(r"(font-family:)('.+'),('.+')", r'\1\3', html)
        self.editor.document().setHtml(htmlTransformed)

    # sets the currently selected Font to the editor

    def setSelectedFont(self, font):
        logging.debug(
            "setSelectedFont: font has changed: setting the editor font to {}".format(font.toString()))
        self.editor.setCurrentFont(font)
        self.removeMultipleFonts()
        self.editor.setFocus()

    def setFont(self):
        font, ok = QFontDialog.getFont(self.editor.currentFont(), self)
        if ok:
            # sets the font of the current format
            self.editor.setCurrentFont(font)

    def define_format_toolbar(self):

        # # Adds a format menu option to the top level menu
        format_toolbar = QToolBar("Format")
        format_toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(format_toolbar)
        format_menu = self.menuBar().addMenu("&Format")

        # # We need references to these actions/settings to update as selection changes, so attach to self.
        self.fonts = QFontComboBox()
        self.fonts.setWritingSystem(QFontDatabase.Latin)
        self.fonts.currentFontChanged.connect(self.setSelectedFont)
        format_toolbar.addWidget(self.fonts)

        self.fontSize = QComboBox()
        self.fontSize.addItems([str(s) for s in FONT_SIZES])

        # # Connect to the signal producing the text of the current selection. Convert the string to float
        # # and set as the pointsize. We could also use the index + retrieve from FONT_SIZES.
        self.fontSize.currentIndexChanged[str].connect(
            lambda s: self.editor.setFontPointSize(float(s)))
        format_toolbar.addWidget(self.fontSize)

        # self.bold_action = QAction(
        #     QIcon(os.path.join('images', 'edit-bold.png')), "Bold", self)

        icon = QIcon()
        if(self.theme == "dark"):
            icon.addPixmap(QPixmap(
                ":/images/images/edit-bold-dark.png"), QIcon.Normal, QIcon.Off)
        else:
            icon.addPixmap(QPixmap(
                ":/images/images/edit-bold-light.png"), QIcon.Normal, QIcon.Off)
        self.bold_action = QAction(
            icon, "Bold", self)

        self.bold_action.setStatusTip("Bold")
        self.bold_action.setShortcut(QKeySequence.Bold)
        self.bold_action.setCheckable(True)
        self.bold_action.toggled.connect(
            lambda x: self.editor.setFontWeight(QFont.Bold if x else QFont.Normal))
        format_toolbar.addAction(self.bold_action)
        format_menu.addAction(self.bold_action)

        # fontSelectAction = QAction(
        #     QIcon(":/images/images/echoes.png"), "Font Selection", self)
        # fontSelectAction.setStatusTip("Select a Font")
        # fontSelectAction.triggered.connect(
        #     self.setFont)
        # format_toolbar.addAction(fontSelectAction)
        # format_toolbar.addAction(fontSelectAction)

        # self.italic_action = QAction(
        #    QIcon(os.path.join('images', 'edit-italic.png')), "Italic", self)
        if(self.theme == "dark"):
            self.italic_action = QAction(
                QIcon(":/images/images/edit-italic-dark.png"), "Italic", self)
        else:
            self.italic_action = QAction(
                QIcon(":/images/images/edit-italic-light.png"), "Italic", self)
        self.italic_action.setStatusTip("Italic")
        self.italic_action.setShortcut(QKeySequence.Italic)
        self.italic_action.setCheckable(True)
        self.italic_action.toggled.connect(self.editor.setFontItalic)
        format_toolbar.addAction(self.italic_action)
        format_toolbar.addAction(self.italic_action)

        if(self.theme == "dark"):
            self.underline_action = QAction(
                QIcon(":/images/images/edit-underline-dark.png"), "Underline", self)
        else:
            self.underline_action = QAction(
                QIcon(":/images/images/edit-underline-light.png"), "Underline", self)
        self.underline_action.setStatusTip("Underline")
        self.underline_action.setShortcut(QKeySequence.Underline)
        self.underline_action.setCheckable(True)
        self.underline_action.toggled.connect(self.editor.setFontUnderline)
        format_toolbar.addAction(self.underline_action)
        format_menu.addAction(self.underline_action)

        if(self.theme == "dark"):
            self.highlight_action = QAction(
                QIcon(":/images/images/edit-highlight-clear-dark.png"), "Highlight", self)
        else:
            self.highlight_action = QAction(
                QIcon(":/images/images/edit-highlight-clear-light.png"), "Highlight", self)
        if(self.theme == "dark"):
            self.highlight_action_yellow = QAction(
                QIcon(":/images/images/edit-highlight-yellow-dark.png"), "Highlight in Yellow", self)
        else:
            self.highlight_action_yellow = QAction(
                QIcon(":/images/images/edit-highlight-yellow-light.png"), "Highlight in Yellow", self)
        if(self.theme == "dark"):
            self.highlight_action_red = QAction(
                QIcon(":/images/images/edit-highlight-red-dark.png"), "Highlight in Red", self)
        else:
            self.highlight_action_red = QAction(
                QIcon(":/images/images/edit-highlight-red-light.png"), "Highlight in Red", self)
        if(self.theme == "dark"):
            self.highlight_action_clear = QAction(
                QIcon(":/images/images/edit-highlight-clear-dar.png"), "Clear Highlighting", self)
        else:
            self.highlight_action_clear = QAction(
                QIcon(":/images/images/edit-highlight-clear-light.png"), "Clear Highlighting", self)
        self.highlight_action.setStatusTip("Select a highlight style")
        self.highlight_action_yellow.setStatusTip("Highlight in Yellow")
        self.highlight_action_red.setStatusTip("Highlight in Red")
        self.highlight_action_red.setStatusTip("Clear Highlighting")
        # self.highlight_action.setShortcut(QKeySequence.Highlight)
        self.highlight_action.setCheckable(False)
        self.highlightMenu = QMenu()
        self.highlightMenu.addAction(self.highlight_action_yellow)
        self.highlightMenu.addAction(self.highlight_action_red)
        self.highlightMenu.addAction(self.highlight_action_clear)
        self.highlight_action.setMenu(self.highlightMenu)
        self.highlight_action_yellow.setCheckable(True)
        self.highlight_action_red.setCheckable(True)
        self.highlight_action_clear.setCheckable(True)
        # self.highlight_action.toggled.connect(self.highlightWord)
        self.highlight_action_yellow.toggled.connect(self.highlightWordYellow)
        self.highlight_action_red.toggled.connect(self.highlightWordRed)
        self.highlight_action_clear.toggled.connect(self.unHighlightWord)
        format_toolbar.addAction(self.highlight_action)
        format_menu.addAction(self.highlight_action)

        format_menu.addSeparator()

        self.align_left_action = QAction(
            QIcon(":/images/images/edit-alignment.png"), "Align left", self)
        self.align_left_action.setStatusTip("Align text left")
        self.align_left_action.setCheckable(True)
        self.align_left_action.triggered.connect(
            lambda: self.editor.setAlignment(Qt.AlignLeft))
        format_toolbar.addAction(self.align_left_action)
        format_menu.addAction(self.align_left_action)

        self.alignc_action = QAction(
            QIcon(":/images/images/edit-alignment-center.png"), "Align center", self)
        self.alignc_action.setStatusTip("Align text center")
        self.alignc_action.setCheckable(True)
        self.alignc_action.triggered.connect(
            lambda: self.editor.setAlignment(Qt.AlignCenter))
        format_toolbar.addAction(self.alignc_action)
        format_menu.addAction(self.alignc_action)

        self.align_right_action = QAction(
            QIcon(":/images/images/edit-alignment-right.png"), "Align right", self)
        self.align_right_action.setStatusTip("Align text right")
        self.align_right_action.setCheckable(True)
        self.align_right_action.triggered.connect(
            lambda: self.editor.setAlignment(Qt.AlignRight))
        format_toolbar.addAction(self.align_right_action)
        format_menu.addAction(self.align_right_action)

        self.align_justify_action = QAction(
            QIcon(":/images/images/edit-alignment-justify.png"), "Justify", self)
        self.align_justify_action.setStatusTip("Justify text")
        self.align_justify_action.setCheckable(True)
        self.align_justify_action.triggered.connect(
            lambda: self.editor.setAlignment(Qt.AlignJustify))
        format_toolbar.addAction(self.align_justify_action)
        format_menu.addAction(self.align_justify_action)

        # # In some situations it is useful to group QAction objects together.
        # # For example, if you have a Left Align action, a Right Align action, a Justify action,
        # # and a Center action, only one of these actions should be active at any one time.
        # # One simple way of achieving this is to group the actions together in an action group.
        format_group = QActionGroup(self)
        format_group.setExclusive(True)
        format_group.addAction(self.align_left_action)
        format_group.addAction(self.alignc_action)
        format_group.addAction(self.align_right_action)
        format_group.addAction(self.align_justify_action)

        format_menu.addSeparator()

        # The underscore prefix is meant as a hint to another programmer that a variable or method starting with a single underscore
        # is intended for internal use or private in the case of a class.
        # A list of all format-related widgets/actions, so we can disable/enable signals when updating.
        self._format_actions = [
            self.fonts,
            self.fontSize,
            self.bold_action,
            self.italic_action,
            self.underline_action,
            # We don't need to disable signals for alignment, as they are paragraph-wide.
        ]
        return format_toolbar

    def define_edit_toolbar(self):
        # The QToolBar class provides a movable panel that contains a set of controls. In this instance we are creating the Edit Toolbar.
        # This will appear on the main application menu.
        edit_toolbar = QToolBar("Edit")
        edit_toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(edit_toolbar)
        # The QMainWindow Class has a menuBar property, the menuBar can contain a collection of menus
        edit_menu = self.menuBar().addMenu("&Edit")

        undo_action = QAction(
            QIcon(":/images/images/undo.png"), "Undo", self)
        undo_action.setStatusTip("Undo last change")
        undo_action.triggered.connect(self.editor.undo)
        edit_toolbar.addAction(undo_action)
        edit_menu.addAction(undo_action)

        redo_action = QAction(
            QIcon(":/images/images/redo.png"), "Redo", self)
        redo_action.setStatusTip("Redo last change")
        redo_action.triggered.connect(self.editor.redo)
        edit_toolbar.addAction(redo_action)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction(
            QIcon(":/images/images/scissors.png"), "Cut", self)
        cut_action.setStatusTip("Cut selected text")
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.triggered.connect(self.editor.cut)
        edit_toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)

        copy_action = QAction(
            QIcon(":/images/images/document-copy.png"), "Copy", self)
        copy_action.setStatusTip("Copy selected text")
        cut_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.editor.copy)
        edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)

        paste_action = QAction(
            QIcon(":/images/images/clipboard-paste-document-text.png"), "Paste", self)
        paste_action.setStatusTip("Paste from clipboard")
        cut_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.editor.paste)
        edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)

        select_action = QAction(
            QIcon(":/images/images/selection-input.png"), "Select all", self)
        select_action.setStatusTip("Select all text")
        cut_action.setShortcut(QKeySequence.SelectAll)
        select_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_action)

        edit_menu.addSeparator()

        wrap_action = QAction(
            QIcon(":/images/images/arrow-continue.png"), "Wrap text to window", self)
        wrap_action.setStatusTip("Toggle wrap text to window")
        wrap_action.setCheckable(True)
        wrap_action.setChecked(True)
        wrap_action.triggered.connect(self.edit_toggle_wrap)
        edit_menu.addAction(wrap_action)

        self.findAction = QAction(QIcon(
            ":/images/images/find-replace.png"), "Find and replace", self)
        self.findAction.setStatusTip("Find and replace words in your document")
        self.findAction.setShortcut("Ctrl+F")
        self.findAction.triggered.connect(findDialog.Find(self).show)
        edit_menu.addAction(self.findAction)
        edit_toolbar.addAction(self.findAction)

        self.findAndReplaceLabel = QLabel("  Find ")
        edit_toolbar.addWidget(self.findAndReplaceLabel)

        self.findLineEdit = QLineEdit(self)
        if(globals.USE_STYLESHEETS_FOR_COLOR):
            self.findLineEdit.setStyleSheet(
                "background-color: #FFFFFF; padding:1px 1px 1px 1px")
        self.findLineEdit.setFixedWidth(120)
        self.findLineEdit.returnPressed.connect(self.findWord)
        edit_toolbar.addWidget(self.findLineEdit)

        # self.toolButton = QToolButton(edit_toolbar)
        # icon = QIcon()
        # icon.addPixmap(QPixmap(":/images/images/case_16.png"),
        #                                   QIcon.Normal, QIcon.Off)

        # # adding icon to the toolbutton
        # self.toolButton.setIcon(icon)
        # self.toolButton.setFixedSize(16,16)
        # self.toolButton.setChecked(True)
        self.caseCheckBox = QCheckBox()
        pixmap = QPixmap(":/images/images/case_16.png")
        self.caseLabel = QLabel()
        self.caseLabel.setPixmap(pixmap)

        self.regexCheckBox = QCheckBox()
        pixmap = QPixmap(":/images/images/regex_16.png")
        self.regexLabel = QLabel()
        self.regexLabel.setPixmap(pixmap)

        self.replaceAllCheckBox = QCheckBox()
        pixmap = QPixmap(":/images/images/replace-all_16.png")
        self.replaceAllLabel = QLabel()
        self.replaceAllLabel.setPixmap(pixmap)

        # self.enableCaseAction = QAction(
        #     QIcon(":/images/images/case_16.png"), "Case Sensitive", self)
        # self.enableRegExpressionAction = QAction(
        #     QIcon(":/images/images/regex_16.png"), "Use Regular Expression", self)
        # self.enableReplaceAllAction = QAction(
        #     QIcon(":/images/images/regex_16.png"), "Replace All", self)

        # self.enableCaseAction.setCheckable(True)
        # self.enableRegExpressionAction.setCheckable(True)
        # self.enableReplaceAllAction.setCheckable(True)
        # self.enableCaseAction.toggled.connect(self.findWord)

        # self.NextButton = QToolButton()
        # self.NextButton.setArrowType(Qt.RightArrow)
        # self.NextButton.setFixedWidth(10)
        # self.NextButton.clicked.connect(self.findWord)
        # edit_toolbar.addWidget(self.caseLabel)
        # edit_toolbar.addWidget(self.caseCheckBox)
        # edit_toolbar.addWidget(self.regexLabel)
        # edit_toolbar.addWidget(self.regexCheckBox)
        # edit_toolbar.addWidget(self.replaceAllLabel)
        # edit_toolbar.addWidget(self.replaceAllCheckBox)

        find_options_toolbar = QToolBar()
        find_options_toolbar.setIconSize(QSize(16, 16))
        self.enableCaseAction = QAction(
            QIcon(":/images/images/case_16.png"), "Case Sensitive", self)
        self.enableCaseAction.setCheckable(True)
        find_options_toolbar.addAction(self.enableCaseAction)
        self.enableRegExpressionAction = QAction(
            QIcon(":/images/images/regex_16.png"), "Use Regular Expression", self)
        self.enableRegExpressionAction.setCheckable(True)
        find_options_toolbar.addAction(self.enableRegExpressionAction)
        # find_options_toolbar.addWidget(self.caseLabel)
        # find_options_toolbar.addWidget(self.caseCheckBox)
        # find_options_toolbar.addWidget(self.regexLabel)
        # find_options_toolbar.addWidget(self.regexCheckBox)
        # find_options_toolbar.addWidget(self.replaceAllLabel)
        # find_options_toolbar.addWidget(self.replaceAllCheckBox)
        find_options_toolbar.setOrientation(Qt.Horizontal)
        find_options_toolbar.setOrientation(Qt.Vertical)
        edit_toolbar.addWidget(find_options_toolbar)
        # edit_toolbar.addAction(self.enableCaseAction)
        # edit_toolbar.addAction(self.enableRegExpressionAction)
        # edit_toolbar.addAction(self.enableReplaceAllAction)
        # edit_toolbar.addWidget(self.NextButton)

        self.replaceLineEdit = QLineEdit(self)
        if(globals.USE_STYLESHEETS_FOR_COLOR):
            self.replaceLineEdit.setStyleSheet(
                "background-color: #FFFFFF; padding:1px 1px 1px 1px")
        self.replaceLineEdit.setFixedWidth(120)
        self.replaceLineEdit.returnPressed.connect(self.replaceWord)
        edit_toolbar.addWidget(self.replaceLineEdit)

        preferences_action = QAction(
            QIcon(":/images/images/preferences.png"), "Lyrical Preferences", self)
        preferences_action.setStatusTip("Set Your Lyrical Preferences")
        preferences_action.triggered.connect(self.show_preferences)
        edit_menu.addAction(preferences_action)
        edit_toolbar.addAction(preferences_action)

    def define_file_toolbar(self):
        file_toolbar = QToolBar("File")
        file_toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(file_toolbar)
        file_menu = self.menuBar().addMenu("&File")

        # Actions
        # Actions can be added to menus and toolbars, and will automatically keep them in sync.
        # For example, in a word processor, if the user presses a Bold toolbar button, the Bold menu item will automatically be checked.
        open_file_action = QAction(
            QIcon(":/images/images/open-document.png"), "Open file...", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)

        new_project_action = QAction(
            QIcon(":/images/images/new-project.png"), "new Project...", self)
        # new_project_action = QAction('new Project...', self)
        new_project_action.triggered.connect(self.create_new_project)
        file_menu.addAction(new_project_action)
        file_toolbar.addAction(new_project_action)

        open_project_action = QAction(
            QIcon(":/images/images/open-project.png"), "Open Project...", self)
        # open_project_action = QAction('Open Project...', self)
        open_project_action.triggered.connect(self.choose_directory)
        file_menu.addAction(open_project_action)
        file_toolbar.addAction(open_project_action)

        save_file_action = QAction(
            QIcon(":/images/images/disk.png"), "Save", self)
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)

        saveas_file_action = QAction(
            QIcon(":/images/images/disk-pencil.png"), "Save As...", self)
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)

        print_action = QAction(
            QIcon(":/images/images/printer.png"), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)

        exit_action = QAction(
            QIcon(":/images/images/exit.png"), "Exit...", self)
        exit_action.setStatusTip("Close the application")
        exit_action.triggered.connect(self.exit_application)
        file_menu.addAction(exit_action)
        file_toolbar.addAction(exit_action)

    def define_about_toolbar(self):
        help_menu = self.menuBar().addMenu("&Help")
        about_action = QAction('&About', self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def get_syllable_count(self):
        cursor = QTextCursor(self.editor.textCursor())
        # word = cursor.selectedText() # enable for selected text
        text = self.editor.toPlainText()
        if utilities.isNotBlank(text):
            text = text.lower()
            # count = style.syllable_count(word)
            count = style.calculate_average_syllables_per_word(text)
            self.status.showMessage(
                "Average Syllable Length: " + str(count), 10000)
            logging.debug(
                "lyrical :Average Syllable Length: {0}".format(count))

    def findEchoes(self):

        cursor = QTextCursor(self.editor.textCursor())
        selectedText = cursor.selectedText()  # enable for selected text
        blockNumber = cursor.blockNumber()
        cursorStart = cursor.selectionStart()
        cursorEnd = cursor.selectionEnd()
        # selectedText = self.editor.toPlainText()
        if utilities.isNotBlank(selectedText):
            selectedText = selectedText.lower()
            result = ""
            # count = style.syllable_count(word)
            word_counts = style.findEchoes(selectedText)
            for word in word_counts:
                result = result + \
                    "{} is  repeated {} times, ". format(
                        word, word_counts[word])
            self.status.showMessage(
                "Repeats : {}".format(result), 10000)
            self.editor.highlightEchoes(
                selectedText, word_counts, blockNumber, cursorStart, cursorEnd)
            logging.debug(
                "Found {0} echoes in the selected text".format(len(word_counts)))
        else:
            self.status.showMessage(
                "You must make a selection first", 20000)

    def checkGrammar(self):
        cursor = QTextCursor(self.editor.textCursor())
        selectedText = cursor.selectedText()  # enable for selected text
        selection = cursor.selection()
        blockNumber = cursor.blockNumber()
        cursorStart = cursor.selectionStart()
        cursorEnd = cursor.selectionEnd()
        # selectedText = self.editor.toPlainText()
        if utilities.isNotBlank(selectedText):
            # selectedText = selectedText.lower()
            if(self.grammarCheck):
                self.grammarCheck.check(selection)
                self.grammarCheck.show()
                if self.grammarCheck.exec():
                    logging.debug("lyrical :Grammar Check get corrected text here {}".format(
                        self.grammarCheck.correctedText))
                    self.editor.replaceSelectedText(
                        self.grammarCheck.correctedText)

                    # parent.editor.insertSelectedWord(wordSelector.selectedWord)
                else:
                    logging.debug("lyrical :Canceled! Grammar check")
        else:
            self.status.showMessage(
                "You must make a selection first", 20000)

    def checkLint(self):
        cursor = QTextCursor(self.editor.textCursor())
        selectedText = cursor.selectedText()  # enable for selected text
        selection = cursor.selection()
        blockNumber = cursor.blockNumber()
        cursorStart = cursor.selectionStart()
        cursorEnd = cursor.selectionEnd()
        # selectedText = self.editor.toPlainText()
        if utilities.isNotBlank(selectedText):
            # selectedText = selectedText.lower()
            if(self.lintCheck):
                self.lintCheck.check(selection)
                self.lintCheck.show()
                if self.lintCheck.exec():
                    logging.debug("lyrical :Lint Check get corrected text here {}".format(
                        self.lintCheck.correctedText))
                    self.editor.replaceSelectedText(
                        self.lintCheck.correctedText)

                    # parent.editor.insertSelectedWord(wordSelector.selectedWord)
                else:
                    logging.debug("lyrical :Canceled! Lint check")
        else:
            self.status.showMessage(
                "You must make a selection first", 20000)

    def generate_test_text(self):
        self.editor.setText(TEST_TEXT)
        logging.debug("lyrical: Position is {} {}".format(
            self.pos().x(), self.pos().y()))

    def create_novel_structure(self, novelProperties):
        # create an outline for our novel
        logging.debug("lyrical :Success! for  novelProperties Prologue: {} Foreword {}".format(
            novelProperties.prologue, novelProperties.foreword))
        # We now need to get the name of the project and novelProperties
        directory = QFileDialog.getSaveFileName(
            caption="Create a new Project Directory",
            directory=self.projectHomeDirectory,
            filter=""
        )
        self.status.showMessage(
            "New Project Directory: " + str(directory[0]), 2000)
        try:
            os.mkdir(str(directory[0]))
        except OSError as error:
            self.status.showMessage(
                "Failed to create: " + str(directory[0]) + " " + str(error), 10000)
        # create the requested documents

        try:
            if(novelProperties.foreword):
                path = os.sep.join(
                    [directory[0], 'foreword.' + self.fileFormat])
                fp = open(path, 'x')
                fp.close()
        except OSError as error:
            self.status.showMessage(
                "Failed to create foreword: " + str(error), 10000)
        # self.foreword = False
        # self.preface = False
        # self.introduction = False
        # self.prologue = False
        # self.epilogue = False
        # self.numberOfChapters = 20
        try:
            if(novelProperties.preface):
                path = os.sep.join(
                    [directory[0], 'preface.' + self.fileFormat])
                fp = open(path, 'x')
                fp.close()
        except OSError as error:
            self.status.showMessage(
                "Failed to create preface: " + str(error), 10000)
        try:
            if(novelProperties.introduction):
                path = os.sep.join(
                    [directory[0], 'introduction.' + self.fileFormat])
                fp = open(path, 'x')
                fp.close()
        except OSError as error:
            self.status.showMessage(
                "Failed to create introduction: " + str(error), 10000)
        try:
            if(novelProperties.prologue):
                path = os.sep.join(
                    [directory[0], 'prologue.' + self.fileFormat])
                fp = open(path, 'x')
                fp.close()
        except OSError as error:
            self.status.showMessage(
                "Failed to create prologue: " + str(error), 10000)
        try:
            if(novelProperties.epilogue):
                path = os.sep.join(
                    [directory[0], 'epilogue.' + self.fileFormat])
                fp = open(path, 'x')
                fp.close()
        except OSError as error:
            self.status.showMessage(
                "Failed to create epilogue: " + str(error), 10000)
        for chapter in range(1, novelProperties.numberOfChapters+1):
            try:
                chapterName = "chapter_" + str(chapter) + "." + self.fileFormat
                path = os.sep.join([directory[0], chapterName])
                fp = open(path, 'x')
                fp.close()
            except OSError as error:
                self.status.showMessage(
                    "Failed to create chapter: " + str(chapter), 10000)

    def create_new_project(self):
        self.projectTypeDialog = projectTypeDialog.ProjectTypeDialog(self)

        if self.projectTypeDialog.exec():
            self.projectType = self.projectTypeDialog.project
            # self.projectHomeDirectory = self.projectTypeDialog.projectHomeDirectoryEdit.text()
            logging.debug("lyrical :Success! " + self.projectType)
            self.novelPropertiesDialog = novelPropertiesDialog.NovelPropertiesDialog(
                self)
            if self.novelPropertiesDialog.exec():
                self.create_novel_structure(
                    self.novelPropertiesDialog.properties)
            else:
                logging.debug("lyrical :Canceled! for novel properties {}".format(
                    self.novelPropertiesDialog.properties))
        else:
            logging.debug("lyrical :Canceled Novel Properties dialog " +
                          self.projectType)

        # Used when we create a new project or open an existing one

    def choose_directory(self):
        """
        Select a directory to display.
        """
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.Directory)
        directory = file_dialog.getExistingDirectory(self, "Open Directory",
                                                     self.projectHomeDirectory, QFileDialog.ShowDirsOnly)

        self.fileTreeView.setRootIndex(
            self.projectExplorerModel.index(directory))
        # update the current project preferences setting
        self.projectCurrentDirectory = directory
        self.status.showMessage(
            "Project Directory: " + str(directory), 2000)

    def get_functional_word_count(self):
        cursor = QTextCursor(self.editor.textCursor())
        # selection = QTextEdit.ExtraSelection()
        # selection.cursor = self.editor.textCursor()
        # word = cursor.selectedText()
        text = self.editor.toPlainText()
        if utilities.isNotBlank(text):
            text = text.lower()
            # count = style.syllable_count(word)
            count = style.calculate_functional_word_count(text)
            self.status.showMessage(
                "Functional Word Score: " + str(count), 6000)

    def showBeautifulWords(self):
        wordListManager = WordListManager(self.resourcePath)
        wordListManager.createBeautifulWordsList(self)

    def showWordsForColor(self):
        wordListManager = WordListManager(self.resourcePath)
        wordListManager.createWordsForColorList(self)

    def showWordsForSmell(self):
        wordListManager = WordListManager(self.resourcePath)
        wordListManager.createWordsForSmellList(self)

    def showWordsForSound(self):
        wordListManager = WordListManager(self.resourcePath)
        wordListManager.createWordsForSoundList(self)

    def showWordsForTouch(self):
        wordListManager = WordListManager(self.resourcePath)
        wordListManager.createWordsForTouchDescriptorsList(self)

    def showDescriptorsForColor(self):
        wordListManager = WordListManager(self.resourcePath)
        wordListManager.createWordsForColorDescriptorsList(self)
    # Create a dockable Project APIKey

    def openMenu(self, position):
        level = 0
        # This convenience function returns a list of all selected and non-hidden item indexes in the view. The list contains no duplicates, and is not sorted
        indexes = self.fileTreeView.selectedIndexes()
        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            fileName = self.projectExplorerModel.fileName(index)
            filePath = self.projectExplorerModel.filePath(index)
            info = self.projectExplorerModel.fileInfo(index)
            isFile = info.isFile()
            if(isFile):
                print("this is a file")
            else:
                print("This is a directory")
            print("Indexes {} level {} row {} column {} filename {} filepath  {} info {}".format(len(indexes),
                                                                                                 level, index.row(), index.column(), fileName, filePath, info))
            menu = QMenu()
            if not isFile:
                addDocumentAction = SpecialAction(
                    "Add New Document", menu
                )
                addDocumentAction.triggered.connect(
                    lambda: self.addDocument(index))
                menu.addAction(addDocumentAction)
                renameProjectAction = SpecialAction(
                    "Rename Project Document", menu
                )
                renameProjectAction.triggered.connect(
                    lambda: self.renameProject(index))
                menu.addAction(renameProjectAction)
            else:
                deleteAction = SpecialAction(
                    "Delete Document", menu
                )
                deleteAction.triggered.connect(
                    lambda: self.deleteDocument(index))
                menu.addAction(deleteAction)
                duplicateAction = SpecialAction(
                    "Duplicate Document", menu
                )
                duplicateAction.triggered.connect(self.duplicateDocument)
                menu.addAction(duplicateAction)
                renameAction = SpecialAction(
                    "Rename Document", menu
                )
                renameAction.triggered.connect(
                    lambda: self.renameDocument(index))
                menu.addAction(renameAction)
            menu.exec_(self.fileTreeView.viewport().mapToGlobal(position))

        # Returns true if this model index is valid; otherwise returns false. A valid index belongs to a model, and has non-negative row and column numbers.
        # while index.parent().isValid():
        #     index = index.parent()
        #     fileName = self.projectExplorerModel.fileName(index)
        #     filePath = self.projectExplorerModel.filePath(index)
        #     print("-- level {} row {} column {} filename {} filepath  {}".format(
        #         level, index.row(), index.column(), fileName, filePath))
        #     level += 1

    def renameProject(self, index):
        if(index):
            print("Renaming the project")
            if not index.isValid():
                return
            model = index.model()
            old_name = model.fileName(index)
            wasReadOnly = model.isReadOnly()
            model.setReadOnly(False)
            name, ok = QInputDialog.getText(
                self, "New Name", "Enter a project name", QLineEdit.Normal, old_name)
            if ok and name and name != old_name:
                model.setData(index, name)
            model.setReadOnly(wasReadOnly)
        else:
            return

    def renameDocument(self, index):
        if(index):
            print("Renaming the document")
            if not index.isValid():
                return
            model = index.model()
            old_name = model.fileName(index)
            wasReadOnly = model.isReadOnly()
            model.setReadOnly(False)
            name, ok = QInputDialog.getText(
                self, "New Name", "Enter a file name", QLineEdit.Normal, old_name)
            if ok and name and name != old_name:
                model.setData(index, name)
            model.setReadOnly(wasReadOnly)
        else:
            return

    def deleteDocument(self, index):
        if(index):
            print("Deleting the document")
            if not index.isValid():
                return
            model = index.model()
            old_name = model.fileName(index)
            wasReadOnly = model.isReadOnly()
            model.setReadOnly(False)
            ok = self.showDeleteConfirmationDialog()
            if ok:
                model.remove(index)
            model.setReadOnly(wasReadOnly)
        else:
            return

    def duplicateDocument(self):
        print("Duplicating the document")

    def addDocument(self, index):
        print("Adding a document")
        try:
            projectPath = self.projectExplorerModel.filePath(index)
            name, ok = QInputDialog.getText(
                self, "Document Name", "Enter a name for the document", QLineEdit.Normal, "new_document")
            if ok and name and name != "new_document":
                nameParts = name.split('.')
                path = os.sep.join(
                    [projectPath, nameParts[0] + "." + self.fileFormat])
                fp = open(path, 'x')
                fp.close()
            else:
                self.status.showMessage(
                    "We did not create a new document. Please enter a valid name", 10000)
        except OSError as error:
            self.status.showMessage(
                "Failed to create new Document: " + str(error), 10000)

    def msgButtonClick(self, i):
        print("Button clicked is:", i.text())

    def showDeleteConfirmationDialog(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure you want to delete this document?")
        msgBox.setWindowTitle("Delete Project Document")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.buttonClicked.connect(self.msgButtonClick)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            return True
        else:
            return False

    def defineFileExplorerTreeView(self):
        """
        Defines the file explorer tree view
        """
        """
        Set up the QTreeView so that it displays the contents
        of the Project.
        """
        self.projectExplorerModel = CustomFileSystemModel("Project Contents")
        self.projectExplorerModel.setHeaderData(
            0, Qt.Horizontal, 'Project Contents')
        # setRootPath
        # Sets the directory that is being watched by the model to newPath by installing a file system watcher on it.
        # Any changes to files and directories within this directory will be reflected in the model.
        # If the path is changed, the rootPathChanged() signal will be emitted.
        # Note: This function does not change the structure of the model or modify the data available to views.
        # In other words, the "root" of the model is not changed to include only files and directories within the directory
        # specified by newPath in the file system.
        self.projectExplorerModel.setRootPath(self.projectHomeDirectory)

        self.fileTreeView = QTreeView()
        self.fileTreeView.setIndentation(10)
        self.fileTreeView.setModel(self.projectExplorerModel)
        self.fileTreeView.setRootIndex(
            self.projectExplorerModel.index(self.projectHomeDirectory))
        self.fileTreeView.header().hideSection(1)
        self.fileTreeView.header().hideSection(2)
        self.fileTreeView.header().hideSection(3)
        self.projectExplorerModel.setHeaderData(
            0, Qt.Horizontal, 'Project Contents')
        self.fileTreeView.clicked.connect(self.onFileExplorerTreeViewClicked)
        self.fileTreeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.fileTreeView.customContextMenuRequested.connect(self.openMenu)
        # Set up container and layout
        frame = QFrame()  # The QFrame class is used as a container to group and surround widgets, or to act as placeholders in GUI
        # applications. You can also apply a frame style to a QFrame container to visually separate it from nearbywidgets.
        frameLayout = QVBoxLayout()
        frameLayout.addWidget(self.fileTreeView)
        frame.setLayout(frameLayout)
        # self.setCentralWidget(frame) # The central widget in the center of the window must be set if you are going to use QMainWindow as your
        # base class. For example, you could use a single QTextEdit widget or create a QWidget object to act as a parent
        # to a number of other widgets, then use setCentralWidget() , and set your central widget for the main
        # window.
        self.projectExplorerDock = QDockWidget("Project View", self)
        self.projectExplorerDock.setWidget(self.fileTreeView)
        self.projectExplorerDock.setFloating(False)
        self.projectExplorerDock.setAllowedAreas(
            Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.projectExplorerDock)

    # Create a dockable Style Bar

    def define_style_toolbar(self):
        """
        Defines the tools bar and actions associated with style analysis
        """
        style_toolbar = QToolBar("Style")
        style_toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(style_toolbar)
        style_menu = self.menuBar().addMenu("&Style")

        # generate_text_action = QAction(
        #     QIcon(":/images/images/generate-text.png"), "Generate Random Text", self)
        # generate_text_action.setStatusTip("Generate Random Text")
        # generate_text_action.triggered.connect(
        #     self.generate_test_text)
        # style_menu.addAction(generate_text_action)
        # style_toolbar.addAction(generate_text_action)

        count_syllable_action = QAction(
            QIcon(":/images/images/syllables.png"), "Average Syllable Length", self)
        count_syllable_action.setStatusTip("Average Syllable Length")
        count_syllable_action.triggered.connect(
            self.get_syllable_count)
        style_menu.addAction(count_syllable_action)
        style_toolbar.addAction(count_syllable_action)

        findEchoesAction = QAction(
            QIcon(":/images/images/echoes.png"), "Word Echoes", self)
        findEchoesAction.setStatusTip("Find Word Echoes")
        findEchoesAction.triggered.connect(
            self.findEchoes)
        style_menu.addAction(findEchoesAction)
        style_toolbar.addAction(findEchoesAction)

        checkGrammarAction = QAction(
            QIcon(":/images/images/grammar.png"), "Grammar Check", self)
        checkGrammarAction.setStatusTip("Find Grammatical Errors")
        checkGrammarAction.triggered.connect(
            self.checkGrammar)
        style_menu.addAction(checkGrammarAction)
        style_toolbar.addAction(checkGrammarAction)

        checkLintAction = QAction(
            QIcon(":/images/images/linting.png"), "Lint Check", self)
        checkLintAction.setStatusTip("Find common usage errors")
        checkLintAction.triggered.connect(
            self.checkLint)
        style_menu.addAction(checkLintAction)
        style_toolbar.addAction(checkLintAction)

        count_functional_words_action = QAction(
            QIcon(":/images/images/functional-words.png"), "Functional Word Count", self)
        count_functional_words_action.setStatusTip("Functional Word Count")
        count_functional_words_action.triggered.connect(
            self.get_functional_word_count)
        style_menu.addAction(count_functional_words_action)
        style_toolbar.addAction(count_functional_words_action)

        self.thesaurusLookupLabel = QLabel("  Thesaurus Search")
        style_toolbar.addWidget(self.thesaurusLookupLabel)

        self.thesaurusLookup = QLineEdit(self)
        if(globals.USE_STYLESHEETS_FOR_COLOR):
            self.thesaurusLookup.setStyleSheet(
                "background-color: #FFFFFF; padding:1px 1px 1px 1px")
        self.thesaurusLookup.setFixedWidth(120)
        self.thesaurusLookup.returnPressed.connect(self.lookupWord)
        style_toolbar.addWidget(self.thesaurusLookup)

        self.style_dock = QDockWidget("Style", self)
        self.style_dock.setWidget(style_toolbar)
        self.style_dock.setFloating(False)
        self.addDockWidget(Qt.TopDockWidgetArea, self.style_dock)

    def define_word_list_toolbar(self):
        """
        Defines the tools bar and actions associated with word_list analysis
        """
        word_list_toolbar = QToolBar("Word Lists")
        word_list_toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(word_list_toolbar)
        word_list_menu = self.menuBar().addMenu("&WordLists")

        beautiful_words_action = QAction(
            QIcon(":/images/images/beauty.png"), "Beautiful Words", self)
        beautiful_words_action.setStatusTip("Beautiful Words")
        beautiful_words_action.triggered.connect(
            self.showBeautifulWords)
        word_list_menu.addAction(beautiful_words_action)
        word_list_toolbar.addAction(beautiful_words_action)

        words_for_color_action = QAction(
            QIcon(":/images/images/colour.png"), "Words For Color", self)
        words_for_color_action.setStatusTip("Words For Color")
        words_for_color_action.triggered.connect(
            self.showWordsForColor)
        word_list_menu.addAction(words_for_color_action)
        word_list_toolbar.addAction(words_for_color_action)

        color_descriptor_action = QAction(
            QIcon(":/images/images/colour-descriptors.png"), "Words that Qualify Color", self)
        color_descriptor_action.setStatusTip("Words For Color")
        color_descriptor_action.triggered.connect(
            self.showDescriptorsForColor)
        word_list_menu.addAction(color_descriptor_action)
        word_list_toolbar.addAction(color_descriptor_action)

        words_for_smell_action = QAction(
            QIcon(":/images/images/smells.png"), "Words For Smell", self)
        words_for_smell_action.setStatusTip("Words For Smell")
        words_for_smell_action.triggered.connect(
            self.showWordsForSmell)
        word_list_menu.addAction(words_for_smell_action)
        word_list_toolbar.addAction(words_for_smell_action)

        words_for_sound_action = QAction(
            QIcon(":/images/images/sounds.png"), "Words For Sound", self)
        words_for_sound_action.setStatusTip("Words For Sound")
        words_for_sound_action.triggered.connect(
            self.showWordsForSound)
        word_list_menu.addAction(words_for_sound_action)
        word_list_toolbar.addAction(words_for_sound_action)

        words_for_touch_action = QAction(
            QIcon(":/images/images/touch.png"), "Words For Touch", self)
        words_for_touch_action.setStatusTip("Words For Touch")
        words_for_touch_action.triggered.connect(
            self.showWordsForTouch)
        word_list_menu.addAction(words_for_touch_action)
        word_list_toolbar.addAction(words_for_touch_action)

        self.word_list_dock = QDockWidget("Word Lists", self)
        self.word_list_dock.setWidget(word_list_toolbar)
        self.word_list_dock.setFloating(False)
        self.addDockWidget(Qt.TopDockWidgetArea, self.word_list_dock)

    def showFontFamilies(self):
        self.supportedFontFamilies = QFontDatabase().families()
        for font in self.supportedFontFamilies:
            logging.debug("Font: {}".format(font))

    # When the user selects some text we want the Font toolbar to reflect the format of their selection

    def update_format(self):
        """
        Update the Font format toolbar/actions when a new text selection is made. This is required to keep
        toolbars/etc. in sync with the current edit state.
        :return:
        """
        # Disable signals for all format widgets, so changing values here does not trigger further formatting.
        self.block_signals(self._format_actions, True)
        logging.debug("editor current font {}".format(
            self.editor.currentFont().toString()))
        self.fonts.setCurrentFont(self.editor.currentFont())
        self.fontSize.setCurrentText(str(int(self.editor.fontPointSize())))
        self.italic_action.setChecked(self.editor.fontItalic())
        self.underline_action.setChecked(self.editor.fontUnderline())
        self.bold_action.setChecked(self.editor.fontWeight() == QFont.Bold)

        self.align_left_action.setChecked(
            self.editor.alignment() == Qt.AlignLeft)
        self.alignc_action.setChecked(
            self.editor.alignment() == Qt.AlignCenter)
        self.align_right_action.setChecked(
            self.editor.alignment() == Qt.AlignRight)
        self.align_justify_action.setChecked(
            self.editor.alignment() == Qt.AlignJustify)

        self.block_signals(self._format_actions, False)

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def lookupWord(self):
        logging.debug("lyrical: lookupWord was called")
        suggestions = self.thesaurus.suggestions(self.thesaurusLookup.text())
        self.updateSuggestions(suggestions)

    def findWord(self):
        logging.debug("lyrical: findWord was called: {}".format(
            self.findLineEdit.text()))
        self.editor.find(self.findLineEdit.text(), "Normal")

    def replaceWord(self):
        logging.debug("lyrical: replaceWord was called: {}".format(
            self.replaceLineEdit.text()))

    def open_file(self, path):
        try:
            with open(path, 'r') as f:
                text = f.read()

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            # Qt will automatically try and guess the format as txt/html
            self.editor.setText(text)
            self.update_title()

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open file", "", "HTML documents (*.html);Text documents (*.txt);All files (*.*)")
        self.open_file(path)

    def file_save(self):
        if self.path is None:
            # If we do not have a path, we need to use Save As.
            self.removeMultipleFonts()
            return self.file_saveas()

        text = self.editor.toHtml() if splitext(
            self.path) in HTML_EXTENSIONS else self.editor.toPlainText()

        try:
            with open(self.path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save file", "", "HTML documents (*.html);Text documents (*.txt);All files (*.*)")

        if not path:
            # If dialog is cancelled, will return ''
            return
        # Depending on the extension, save as either html or plain text
        text = self.editor.toHtml() if splitext(
            path) in HTML_EXTENSIONS else self.editor.toPlainText()

        try:
            with open(path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            self.update_title()

    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())

    def exit_application(self):
        self.save_settings()
        sys.exit()

    def update_title(self):
        self.setWindowTitle(
            "%s - Lyrical" % (os.path.basename(self.path) if self.path else "Untitled"))

    def edit_toggle_wrap(self):
        self.editor.setLineWrapMode(
            1 if self.editor.lineWrapMode() == 0 else 0)

    def save_settings(self):
        settings = QSettings()
        # QSettings stores settings. Each setting consists of a QString that specifies the setting’s name (the key ) and a QVariant that stores the data associated with the key. To write a setting, use setValue()
        settings.setValue(SETTINGS_TRAY, False)  # self.check_box.isChecked()
        settings.beginGroup("MainWindow")
        # the current active project directory within the root
        settings.setValue("project_current", self.projectCurrentDirectory)
        settings.setValue("webster_api_key", self.websterAPIkey)
        settings.setValue("size", self.size())
        settings.setValue("pos", self.pos())
        logging.debug("lyrical save_settings: Position is {} {}".format(
            self.pos().x(), self.pos().y()))
        settings.setValue("file_format", self.fileFormat)
        settings.setValue("theme", self.theme)
        logging.debug(
            "lyrical: Saving the {} theme from settings ".format(self.theme))
        settings.setValue("language", self.language)
        settings.endGroup()
        settings.beginGroup("Preferences")
        # the default root directory for all projects
        settings.setValue("project_home", self.projectHomeDirectory)

        settings.endGroup()
        settings.sync()
        logging.info("lyrical: Saved Lyrical settings")

    def load_settings(self):
        settings = QSettings()
        settings.beginGroup("Preferences")
        self.projectHomeDirectory = settings.value("project_home")
        settings.endGroup()
        settings.beginGroup("MainWindow")
        self.projectCurrentDirectory = settings.value("project_current")
        self.websterAPIkey = settings.value("webster_api_key")
        if(self.websterAPIkey == None):
            self.websterAPIkey = "Get an API Key at www.dictionaryapi.com"
        self.applicationPosition = settings.value("pos")
        logging.debug("lyrical load_settings: Position is {} {}".format(
            self.applicationPosition.x(), self.applicationPosition.y()))
        if(self.applicationPosition == None):
            self.applicationPosition = QPoint(0, 0)
        self.applicationSize = settings.value("size")
        if(self.applicationSize == None):
            self.applicationSize = QSize(1400, 700)
        self.fileFormat = settings.value("file_format")
        if(self.fileFormat == None):
            self.fileFormat = "html"
        self.language = settings.value("language")
        if(self.language == None):
            self.language = "enu"
        self.theme = settings.value("theme")
        if(self.theme == None):
            self.theme = "light"
        logging.debug(
            "lyrical: Loading the {} theme from settings ".format(self.theme))
        self.language = settings.value("language")
        if(self.applicationPosition.x() < 0):
            self.applicationPosition.setX(0)
        if(self.applicationPosition.y() < 0):
            self.applicationPosition.setY(0)
        # These next lines appear to break the menu system  if the position becomes negative
        self.setGeometry(self.applicationPosition.x(), self.applicationPosition.y(
        ), self.applicationSize.width(), self.applicationSize.height())
        logging.debug("lyrical load_settings: Setting Position is {} {} width {} height {}".format(
            self.applicationPosition.x(), self.applicationPosition.y(), self.applicationSize.width(), self.applicationSize.height()))
        settings.endGroup()
        # logging.debug("lyrical :Checking for api key : " + os.environ.get("API_KEY"))
        logging.info("lyrical: Loaded Lyrical settings")

    def closeEvent(self, event):
        self.save_settings()
        event.accept()
# Used to set the project root directory

    def show_about_dialog(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec_()

    def set_directory(self):
        """
        Choose the directory.
        """
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.Directory)
        self.directory = file_dialog.getExistingDirectory(self, "Open \
        Directory", self.projectHomeDirectory, QFileDialog.ShowDirsOnly)
        if self.directory:
            self.preferencesDialog.projectHomeDirectoryEdit.setText(
                self.directory)

    def onFileExplorerTreeViewClicked(self, index):
        indexItem = self.projectExplorerModel.index(
            index.row(), 0, index.parent())
        fileName = self.projectExplorerModel.fileName(indexItem)
        filePath = self.projectExplorerModel.filePath(indexItem)
        if(os.path.isfile(filePath)):
            self.status.showMessage(
                "Selected File: " + str(filePath) + "   " + str(fileName), 10000)
            self.open_file(filePath)

    def updateSuggestions(self, suggestions):
        self.update_suggestions_toolbar(suggestions)

    def debugFontDetails(self):
        currentEditorFont = self.editor.currentFont().toString().split(
            ",")  # font of the current format
        documentDefaultFont = self.editor.document().defaultFont(
        ).toString().split(",")  # documents default font
        # QTextEditor.setFont sets the font for the underlying QTextWidget, QWidget only has one font type at a time
        # QTextEdit exposes an interface to set the font for different parts of the text via QTextCharFormat
        # QTextEditor.setCurrentFont allows one set the font for the active QTextCharFormat
        # for format in self.editor.document().allFormats():

    def cursorPosition(self):
        cursor = self.editor.textCursor()
        # Mortals like 1-indexed things
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()
        mode = self.editor.overwriteMode()
        if (not mode):
            editMode = "Insert"
        else:
            editMode = "Over Write"
        if(self.editor.currentFont()):
            currentFont = self.editor.currentFont().toString().split(",")
        else:
            currentFont = "none"
        if(self.editor.document().defaultFont()):
            defaultFont = self.editor.document().defaultFont().toString().split(",")
        else:
            defaultFont = "none"
        self.statusMode.setText(
            "Current Font: {} | Default Font: {} | Block: {} | Column: {} | Mode: {}".format(currentFont[0], defaultFont[0], line, col, editMode))
        # self.status.showMessage(
        #    "Block: {} | Column: {} | Mode: {}".format(line, col, editMode))

    @ pyqtSlot(str)
    def replace_word_in_editor(self, word: str):
        self.editor.replace_selected_word(word)


if __name__ == '__main__':
    print("Application starting")
    app = QApplication(sys.argv)  # create the main app
    splash = SplashScreen()
    print("Application Showing Splash Screen")
    splash.show()
    app.processEvents()
    # When creating a QSettings object, you must pass the name of your company or organization as well as the name of your application.
    QCoreApplication.setApplicationName(ORGANIZATION_NAME)
    # When the Internet domain is set, it is used on macOS and iOS instead of the organization name, since macOS and iOS applications conventionally use Internet domains to identify themselves.
    QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
    QCoreApplication.setApplicationName(APPLICATION_NAME)
    logging.basicConfig(level=logging.DEBUG, filename="lyrical.log", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s", force=True)
    logging.info("lyrical: Starting Lyrical Editor")
    app.setStyle("fusion")
    try:
        import importlib
        have_pyi_splash = importlib.util.find_spec("pyi_splash")
        if(have_pyi_splash):
            logging.info("using pyi_splash")
            if '_PYIBoot_SPLASH' in os.environ:
                logging.info("Detected _PYIBoot_SPLASH in enviroment")
                import pyi_splash
                # pyi_splash.update_text('UI Loaded ...')
                pyi_splash.close()
            else:
                logging.info(
                    "Did not detect _PYIBoot_SPLASH in environment {}".format(os.environ))
    except Exception as error:
        logging.info("Not running as a pyinstaller executable")
    window = MainWindow(app)
    window.loadInBackground()
    splash.delayedClose()
    print("Starting to show")
    window.show()
    style.updates()
    window.raise_()
    app.exec_()
