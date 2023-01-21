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
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase,
                          QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, white)
    dark_palette.setColor(QPalette.ToolTipText, white)
    dark_palette.setColor(QPalette.Text, white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, white)
    dark_palette.setColor(QPalette.BrightText, red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, black)
    return dark_palette


def light():
    light_palette = QPalette()
    light_palette.setColor(QPalette.Window, QColor(202, 202, 202))
    light_palette.setColor(QPalette.WindowText, QColor(53, 53, 53))
    light_palette.setColor(QPalette.Base, QColor(230, 230, 230))
    light_palette.setColor(QPalette.AlternateBase,
                           QColor(202, 202, 202))
    light_palette.setColor(QPalette.ToolTipBase, QColor(53, 53, 53))
    light_palette.setColor(QPalette.ToolTipText, QColor(53, 53, 53))
    light_palette.setColor(QPalette.Text, QColor(53, 53, 53))
    light_palette.setColor(QPalette.Button, QColor(202, 202, 202))
    light_palette.setColor(QPalette.ButtonText, QColor(53, 53, 53))
    light_palette.setColor(QPalette.BrightText, red)
    light_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    light_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    light_palette.setColor(QPalette.HighlightedText, QColor(202, 202, 202))
    return light_palette


def grey():
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.Active, QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
    dark_palette.setColor(
        QPalette.Disabled, QPalette.Light, QColor(53, 53, 53))
    return dark_palette
