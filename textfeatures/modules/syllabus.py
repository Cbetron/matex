#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""syllables.py:	Diese Datei ist Teil der Wortwahl"""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Julian Behringer"
__email__ = "julian.b@hringer.de"
__status__ = "dev"

import utils.textinit as TI
from .textfeature import Textfeature
import textstat.textstat as TS


class Syllabus(Textfeature):
    def __init__(self):
        self.text_statistics = TS.textstatistics()

    def analyse(self, text):
        syllables = self.text_statistics.syllable_count(text)/TI.word_count(text)
        return {"syllables": syllables}
