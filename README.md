# python-fontforge-script

Python Script for Font Manipulation using FontForge Module

# Please install python-fontforge module first as well as PyQt5

# [minizeFont.py](../../blob/master/minizeFont.py)

Python script that minimize ttf font by input word list

Use [minifyTC](../../blob/master/minifyTC) as input word list

Word list format
```
A
B
C
```

# [copyReferenceAtoB.py](../../blob/master/copyReferenceAtoB.py)

Python script that copy glyph 'A' to glyph 'B' by Reference

Use [copyReferenceAtoB](../../blob/master/copyReferenceAtoB) as input word list

Word list format (Copy glyph 'A' to glyph 'B', copy glyph 'C' to glyph 'D')
```
A B
C D
```

# [checkMissingGlyph.py](../../blob/master/checkMissingGlyph.py)

Check Missing Glyph in word list [missingGlyph](../../blob/master/missingGlyph) 

Word list format
```
A
B
C
```