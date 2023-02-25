from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


white = QColor(255, 255, 255)
red = QColor(255, 0, 0)
black = QColor(0, 0, 0)

# Pale green lyrical = #E6E9CC
# Dark Green lyrical = #314B4A


def dark():
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(
        53, 53, 53))  # a dark grey, almost black A general background color.
    # A general foreground color.
    dark_palette.setColor(QPalette.WindowText, white)
    dark_palette.setColor(QPalette.Base, QColor(
        25, 25, 25))  # a dark grey, almost black Used mostly as the background color for text entry widgets, but can also be used for other painting - such as the background of combobox drop down lists and toolbar handles. It is usually white or another light color.
    dark_palette.setColor(QPalette.AlternateBase,
                          QColor(53, 53, 53))  # a dark grey, almost black Used as the alternate background color in views with alternating row colors
    dark_palette.setColor(QPalette.ToolTipBase, white)
    dark_palette.setColor(QPalette.ToolTipText, white)
    # The foreground color used with Base. This is usually the same as the WindowText, in which case it must provide good contrast with Window and Base.
    dark_palette.setColor(QPalette.Text, white)
    dark_palette.setColor(QPalette.Button, QColor(
        53, 53, 53))  # a dark grey, almost black
    # A foreground color used with the Button color.
    dark_palette.setColor(QPalette.ButtonText, white)
    # A text color that is very different from WindowText, and contrasts well with e.g. Dark. Typically used for text that needs to be drawn where Text or WindowText would give poor contrast, such as on pressed push buttons. Note that text colors can be used for things other than just words; text colors are usually used for text, but it's quite common to use the text color roles for lines, icons, etc.
    dark_palette.setColor(QPalette.BrightText, red)
    dark_palette.setColor(QPalette.Link, QColor(
        42, 130, 218))  # a mid range blue
    dark_palette.setColor(QPalette.Highlight, QColor(
        42, 130, 218))  # a mid range blue
    dark_palette.setColor(QPalette.HighlightedText, black)
    return dark_palette


def light():
    light_palette = QPalette()
    light_palette.setColor(QPalette.Window, QColor(
        202, 202, 202))  # a light grey
    light_palette.setColor(QPalette.WindowText, QColor(
        53, 53, 53))  # a dark grey, almost black
    light_palette.setColor(QPalette.Base, QColor(
        230, 230, 230))  # a light grey
    light_palette.setColor(QPalette.AlternateBase,
                           QColor(202, 202, 202))
    light_palette.setColor(QPalette.ToolTipBase, QColor(
        53, 53, 53))  # a dark grey, almost black
    light_palette.setColor(QPalette.ToolTipText, QColor(
        53, 53, 53))  # a dark grey, almost black
    light_palette.setColor(QPalette.Text, QColor(
        53, 53, 53))  # a dark grey, almost black
    light_palette.setColor(QPalette.Button, QColor(
        202, 202, 202))  # a light grey
    light_palette.setColor(QPalette.ButtonText, QColor(53, 53, 53))
    light_palette.setColor(QPalette.BrightText, red)
    light_palette.setColor(QPalette.Link, QColor(
        42, 130, 218))  # a mid range blue
    light_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    light_palette.setColor(QPalette.HighlightedText,
                           QColor(202, 202, 202))  # a light grey
    return light_palette


def grey():
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(
        53, 53, 53))  # a dark grey, almost black
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(
        35, 35, 35))  # a darker grey, almost black
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(
        25, 25, 25))  # a dark grey, almost black
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(
        42, 130, 218))  # a mid range blue
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.Active, QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
    dark_palette.setColor(
        QPalette.Disabled, QPalette.Light, QColor(53, 53, 53))
    return dark_palette
