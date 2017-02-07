#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""wordLength.py: This file determines the average wordlenth and related values of a text."""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Julian Behringer"
__email__ = "julian.b@hringer.de"
__status__ = "dev"

import utils.textinit as TI
from .textfeature import Textfeature
import textstat.textstat as TS


class Wordlength(Textfeature):
    """ This class inherits from the Textfeature superclass. It is used for the wordlength feature
    """
    def __init__(self):
        """ An local Object of the textstat package is created before using analyse function
        """
        super().__init__()
        self.text_statistics = TS.textstatistics()

    def analyse(self, text):
        """ This function returns the average wordlenth and related values.
        :param text: The given text.
        :return dict: The dictionary entry with the length of the shortest and longest word, the textlength and number of difficult words.
        """
        cleantext = TI.cleantext(text)
        words = cleantext.split(' ')  # Split text into list of words
        max_length = max(len(word) for word in words)  # Longest word
        average = sum(len(word) for word in words) / len(words)  # Average wordlength
        difficult_words = self.text_statistics.difficult_words(text)
        return {"longest_word": max_length, "average_wordlenght": average,
                "words": TI.word_count(text), "difficult_words": difficult_words}
