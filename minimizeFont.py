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
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QFileDialog, QDialog, QPushButton,
                             QLineEdit, QLabel, QCheckBox,
                             QApplication, QVBoxLayout)

useUnichr = True
if not useUnichr:
    unichr = str


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
defaultInFile = "minifyGlyphs"

# outFilePrompt = "Minimize TTF File to write"
# defaultOutFile = "out.ttf"
generateGlyphAsEPS = "Generate Glyph As EPS"
generateGlyphAsPNG = "Generate Glyph As PNG"
defaultPNGSize = "PNG Pixel Size"

items = collections.OrderedDict()
items[inFilePrompt] = defaultInFile
# items[outFilePrompt] = defaultOutFile
items[generateGlyphAsEPS] = True
items[generateGlyphAsPNG] = True
items[defaultPNGSize] = 48

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
# Pseudo Old FontForge Script
# SelectNone()
# SelectMore(...)
# SelectInvert()
# Clear()
# Generate()
###
count = 0
for line in f:
    if line.startswith("##"):
        continue
    words = line.encode("raw_unicode_escape").split()
    # words = line.split()
    # print(len(words))
    if len(words) == 1:
        sys.stdout.write(words[0].decode('unicode_escape'))
        count += 1
        if count % 25 == 0:
            sys.stdout.write("\n")
        sys.stdout.flush()
        if words[0].startswith(b'\u'):
            # print(words[0].decode('unicode_escape'))
            ttfFile.selection.select(("more", None), words[0][1:])
        elif len(words[0]) == 1:
            # print(words[0].decode('unicode_escape'))
            ttfFile.selection.select(("more", None), words[0])

ttfFile.selection.invert()
ttfFile.clear()
ttfFile.fontname = ttfFile.fontname + "-SKIM"
ttfFile.familyname = ttfFile.familyname + "-SKIM"
if not os.path.exists("out"):
    os.makedirs("out")

ttfFile.generate("out/"+ttfFile.fontname+u".ttf")
print(u'\nGenerated '+ttfFile.fontname+u" as out/"+ttfFile.fontname+u".ttf \n")

ttfFile.selection.invert()

if items[generateGlyphAsEPS]:

    if not os.path.exists("out/eps"):
        os.makedirs("out/eps")

    count = 0
    print(u'\nGenerating EPS')
    for glyph in ttfFile.selection.byGlyphs:
        glyph.export("out/eps/"+unichr(glyph.unicode)+".eps")
        sys.stdout.write('.')
        sys.stdout.flush()
        count += 1

    print("\n"+str(count)+" elements export as out/eps/{unicode}.eps")

if items[generateGlyphAsPNG]:
    pngSize = items[defaultPNGSize]

    if int(pngSize) < 8:
        print("PNG Size should at least 8 pixel, set to 8 now.")
        pngSize = "8"

    if not os.path.exists("out/png"):
        os.makedirs("out/png")

    count = 0
    print(u'\nGenerating PNG @ '+pngSize)
    for glyph in ttfFile.selection.byGlyphs:
        glyph.export("out/png/"
                     + unichr(glyph.unicode)
                     + "."
                     + pngSize
                     + ".png",
                     int(pngSize),
                     1)
        sys.stdout.write('.')
        sys.stdout.flush()
        count += 1

    print("\n"
          + str(count)
          + " elements export as out/png/{unicode}."
          + pngSize
          + ".png")

if items[generateGlyphAsEPS] or items[generateGlyphAsPNG]:
    print(u'\nGenerated '+ttfFile.fontname +
          u" as out/"+ttfFile.fontname+u".ttf \n")
