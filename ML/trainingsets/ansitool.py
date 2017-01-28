#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""pythonfile.py:	Description of pythonfile.py"""

__author__ = "Raphael Kreft"
__copyright__ = "Copyright (c) 2016 Raphael Kreft"
__version__ = "Development v0.0"
__email__ = "raphaelkreft@gmx.de"
__status__ = "Dev"

import codecs
import os

path = os.getcwd() + "/"
files = []
for (dirpath, dirnames, filenames) in os.walk(path):
    files.extend(filenames)
print(files)
for f in files:
    # read input file
    with codecs.open(path + f, 'r', encoding='Windows-1252') as filex:
        lines = filex.read()
    # write output file
    with codecs.open(path + f, 'w', encoding='utf8') as filex:
        filex.write(lines)
