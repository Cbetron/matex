#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""syllables.py: This file counts the syllables in a text."""


__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Julian Behringer"
__email__ = "julian.b@hringer.de"
__status__ = "dev"

import utils.textinit as TI
from .textfeature import Textfeature
import textstat.textstat as TS


class Syllabus(Textfeature):
    """ This class inherits from the Textfeature superclass. It is used for the syllables feature
    """
    def __init__(self):
        """ Creating textstat object for analyse function
        """
        self.text_statistics = TS.textstatistics()

    def analyse(self, text):
        """ This function returns the number of syllables in a text.
        :param text: The given text.
        :return dict: The dictionary entry with the number syllables.
        """
        syllables = self.text_statistics.syllable_count(text)/TI.word_count(text)
        return {"syllables": syllables}
