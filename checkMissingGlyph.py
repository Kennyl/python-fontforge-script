#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import fontforge
from io import open
import sys

# ignore warning
# import warnings
# warnings.filterwarnings("ignore")

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QFileDialog, QDialog, QPushButton,
                             QLineEdit, QLabel, QCheckBox,
                             QApplication, QVBoxLayout)


class askSetting(QDialog):

    def __init__(self,
                 app=None,
                 parent=None,
                 items=None):

        super(askSetting, self).__init__(parent)

        self.app = app
        self.items = items

        layout = QVBoxLayout()

        self.lineedits = collections.OrderedDict()
        self.buttons = collections.OrderedDict()

        for key in items.keys():
            if isinstance(items[key], bool):
                self.buttons[key] = QCheckBox(key)
                self.buttons[key].setChecked(items[key])
                self.buttons[key].setFocusPolicy(Qt.StrongFocus)
                layout.addWidget(self.buttons[key])
            else:

                layout.addWidget(QLabel(key))
                self.lineedits[key] = QLineEdit()
                if isinstance(items[key], int):
                    self.lineedits[key].setText(str(items[key]))
                    # self.lineedits[key].setInputMask("000")
                    self.lineedits[key].setMaxLength(3)
                    self.lineedits[key].setValidator(
                        QIntValidator(1, 999, self))

                else:
                    self.lineedits[key].setText(items[key])

                # enable ime input
                self.lineedits[key].inputMethodQuery(Qt.ImEnabled)
                layout.addWidget(self.lineedits[key])

        self.btn = QPushButton('TTF File to Read', self)
        self.btn.clicked.connect(lambda: (self.bye(items)))
        self.btn.setFocusPolicy(Qt.StrongFocus)

        layout.addWidget(self.btn)

        self.setLayout(layout)
        self.setWindowTitle(' Setting ')

    def bye(self, items):
        fileName = QFileDialog.getOpenFileName(
            self, 'Dialog Title', '~/', initialFilter='*.ttf')
        if fileName == (u'', u'*.ttf'):
            print("Must Provide an input TTF file.")
            sys.exit()

        for key in self.buttons.keys():
            self.items[key] = self.buttons[key].isChecked()
        for key in self.lineedits.keys():
            self.items[key] = self.lineedits[key].text()

        self.items['getOpenFileName'] = fileName[0]
        self.close()
        self.app.exit(1)


inFilePrompt = "File to read"
defaultInFile = "missingGlyphs"

items = collections.OrderedDict()
items[inFilePrompt] = defaultInFile

app = QApplication(sys.argv)
ask = askSetting(app=app, items=items)
ask.show()
rtnCode = app.exec_()
# If press OK button  rtnCode should be 1
if rtnCode != 1:
    print('User abort by closing Setting dialog')
    sys.exit

# print(items)
ttfFile = fontforge.open(items['getOpenFileName'])

f = open(items[inFilePrompt], 'r', encoding="utf-8")

ttfFile.selection.none()
###
# file contents
# ## start with "##" line will be ignore to read
# 問
# 问
# ie. \w
# ie. word
###
count = 0

for line in f:
    if line.startsWith("##"):
        continue
    words = line.encode("raw_unicode_escape").split()
    if len(words) == 1:
        if words[0].startswith(b'\u'):
            ttfFile.selection.select(words[0][1:])
        elif len(words[0]) == 1:
            ttfFile.selection.select(words[0])

        if sum(1 for _ in ttfFile.selection.byGlyphs) == 0:
            count += 1
            if count == 1:
                print("\n Missing Glyph for followings:")
                print("-１-２-３-４-５-６-７-８-９-⓵ -１-２-３-４-５-６-７-８-９-⓶ -")
                sys.stdout.write(" ")
            if words[0].startswith(b'\u'):
                sys.stdout.write(words[0].decode("raw_unicode_escape"))
                sys.stdout.write(" ")
                if count % 20 == 0:
                    sys.stdout.write("\n ")
                sys.stdout.flush()

if count > 0:
    print("\n-１-２-３-４-５-６-７-８-９-⓵ -１-２-３-４-５-６-７-８-９-⓶ -")
    # print("\n-ー-ー-ー-ー-ー-ー-ー-ー-ー-ー-ー-ー-ー-ー-ー-ー-ー-ー-ー-ー-")
    # print("\nーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー")
    print(" Total Missing Glyph: "+str(count))
else:
    print("\n No Missing Glyph")
