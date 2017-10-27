#!/usr/bin/env python
# -*- coding: utf-8 -*-

from io import open
import sys
import os
import collections
import fontforge

# ignore warning
# import warnings
# warnings.filterwarnings("ignore")

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFileDialog, QDialog, QPushButton,
                             QLineEdit, QLabel,
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

        self.lineedits = {}

        for key in items.keys():
            layout.addWidget(QLabel(key))
            self.lineedits[key] = QLineEdit()
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

        for key in self.lineedits.keys():
            self.items[key] = self.lineedits[key].text()

        self.items['getOpenFileName'] = fileName[0]
        self.close()
        self.app.exit(1)


inFilePrompt = "File to read"
defaultInFile = "copyReferenceAtoB"

outFilePrompt = "TTF File to write"
defaultOutFile = "out.ttf"

items = collections.OrderedDict()
items[inFilePrompt] = defaultInFile
items[outFilePrompt] = defaultOutFile

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
# file contents
# 問
# 问
# ie. \w
## ie. word
count = 0
for line in f:
    words = line.encode("raw_unicode_escape").split()
    # words = line.split()
    # print(len(words))
    if len(words) == 2:
        sys.stdout.write(words[0].decode('unicode_escape'))
        count += 1
        if count % 25 == 0:
            sys.stdout.write("\n")
        sys.stdout.flush()
        if words[0] == words[1]:
            pass
        elif words[0].startswith(b'\u') and words[1].startswith(b'\u'):
            ttfFile.selection.select(words[0][1:])
            ttfFile.copyReference()
            if words[1].startswith(b'\u'):
                ttfFile.selection.select(words[1][1:])
            else:
                ttfFile.selection.select(words[1])

            ttfFile.paste()
        else:
            ttfFile.selection.select(words[0])
            ttfFile.copyReference()
            if words[1].startswith(b'\u'):
                ttfFile.selection.select(words[1][1:])
            else:
                ttfFile.selection.select(words[1])
            ttfFile.paste()

ttfFile.fontname = ttfFile.fontname + "-TWEAK"
if not os.path.exists("out"):
    os.makedirs("out")

ttfFile.generate("out/"+defaultOutFile)

print(u'\nGenerated '+ttfFile.fontname+u" as out/"+defaultOutFile+u"\n")
