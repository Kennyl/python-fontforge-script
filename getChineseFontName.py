#!/usr/bin/env python
# -*- coding: utf-8 -*-
import fontforge
import glob

fonts = glob.glob("*.ttf")

for f in fonts:
    ttfFile = fontforge.open(f, 5)
    chinesename = ""
    for item in ttfFile.sfnt_names:
        (a, b, c) = item
        if a == 'Chinese (PRC)' and b == 'Fullname':
            chinesename = c
        if a == 'Chinese (Taiwan)' and b == 'Fullname':
            chinesename = c
        if a == 'Chinese (Hong Kong)' and b == 'Fullname':
            chinesename = c

    # print("cp  shortname/" + f + "  " + c+'_' +
    #       (ttfFile.fullname).replace(' ', '') + ".ttf")
    print(f.replace(' ', '\\ ') + " as " + chinesename +
          "_" + ttfFile.fullname.replace(' ', '_'))
