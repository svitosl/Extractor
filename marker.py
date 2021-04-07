from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtGui import QTextCursor

import re

class MyMarker():

    color_list = ['aqua', 'blue', 'blueviolet', 'peru', 'chocolate', 'darkgreen', 'darkgrey',
                  'darkkhaki', 'darkorange', 'deeppink', 'gold', 'mediumvioletred', 'olive', 'red',
                  'salmon', 'teal', 'palevioletred', 'lightcoral', 'darkred', 'goldenrod']

    def __init__(self):
        self.color = 0

    def fill(self, text, keyword, parent):
        self.text = self.str_details(text)
        self.word = self.str_details(keyword)
        self.cursor = parent.textCursor()
        self.format = QtGui.QTextCharFormat()
        self.clear_selection(parent)

    def change_color(self):
        self.format.setBackground(QtGui.QColor(self.color_selection()))

        if self.word[0] > 1 and self.word[1] != self.word[2]: coff = 1
        else: coff = 2
        for i in range(coff,3):
            pattern = self.word[i]
            regex = QtCore.QRegExp(pattern)
            pos = 0
            index = regex.indexIn(self.text, pos)
            while (index != -1):
                pos = index + regex.matchedLength()

                if index-1 >= 0:
                    if re.search('[а-яА-Яa-zA-Z]', self.text[index - 1]):
                        result = False
                    else:
                        result = True
                else:
                    result = True

                if result:
                    if pos+1 <= len(self.text):
                        if re.search('[а-яА-Яa-zA-Z]', self.text[pos]):
                            result = False
                        else:
                            result = True
                    else:
                        result = True

                if result:
                    self.cursor.setPosition(index)
                    self.cursor.setPosition(pos, QTextCursor.KeepAnchor)
                    self.cursor.mergeCharFormat(self.format)
                index = regex.indexIn(self.text, pos)

    def color_selection(self):
        if self.color > 19: self.color = 0
        self.color = self.color + 1
        return self.color_list[self.color - 1]

    def str_details(self, string):
        if isinstance(string, str):
            string = string.replace('ё', 'е')
            string = string.lower()
        elif isinstance(string, list):
            for i in range(1, 3):
                string[i] = string[i].replace('ё', 'е')
                string[i] = string[i].lower()
        return string

    def clear_selection(self, clr_parent):
        clr_cursor = clr_parent.textCursor()
        clr_format = QtGui.QTextCharFormat()
        clr_format.setBackground(QtGui.QColor('white'))
        clr_cursor.setPosition(0)
        clr_cursor.setPosition(len(clr_parent.toPlainText()), QTextCursor.KeepAnchor)
        clr_cursor.mergeCharFormat(clr_format)