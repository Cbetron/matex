# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""setup_parser.py: This util sets up Google Syntaxnet to work with our program"""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Nikodem Kernbach"
__email__ = "kernbach@phaenovum.de"
__status__ = "final"

import sys
import os
sys.path.append('../..')
import parser as PRS  # importing parser from main directory

os.chdir('../..')

PRS.setup_parser()  # setting up syntaxnet to work with maTex
print('Successfully installed')
