#!/usr/bin/env python
# -*- coding: utf-8 -*-
import fontforge
import glob

fonts = glob.glob("*.ttf")

for f in fonts:
    ttfFile = fontforge.open(f, 5)
    chineseName = ""
    englishName = ttfFile.fullname.replace(' ', '_')
    for item in ttfFile.sfnt_names:
        (a, b, c) = item
        if a == 'English (US)' and b == 'Fullname':
            englishName = c.replace(' ', '_')
        if a == 'Chinese (PRC)' and b == 'Fullname':
            chineseName = c
        if a == 'Chinese (Taiwan)' and b == 'Fullname':
            chineseName = c
        if a == 'Chinese (Hong Kong)' and b == 'Fullname':
            chineseName = c

    # print("cp  shortname/" + f + "  " + c+'_' +
    #       (ttfFile.fullname).replace(' ', '') + ".ttf")
    print(f.replace(' ', '\\ ') + " as " + chineseName +
          "_" + englishName)
