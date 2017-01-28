#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""syllables.py:	Diese Datei ist Teil der Wortwahl"""

__author__ = "Julian Behringer"
__copyright__ = ""
__credits__ = ""

__license__ = ""
__version__ = "0.1"
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
