#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""wordLength.py:	Diese Datei ist Teil der Wortwahl"""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Julian Behringer"
__email__ = "julian.b@hringer.de"
__status__ = "dev"

import utils.textinit as TI
from .textfeature import Textfeature
import textstat.textstat as TS


class Wordlength(Textfeature):
    def __init__(self):
        super().__init__()
        self.text_statistics = TS.textstatistics()

    def analyse(self, text):
        cleantext = TI.cleantext(text)
        words = cleantext.split(' ')  # Split text into list of words
        max_length = max(len(word) for word in words)  # Longest word
        average = sum(len(word) for word in words) / len(words)  # Average wordlength
        difficult_words = self.text_statistics.difficult_words(text)
        return {"longest_word": max_length, "average_wordlenght": average,
                "words": TI.word_count(text), "difficult_words": difficult_words}
