#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""paragraph.py: This file counts the used abbreviations in a text."""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Raphael Kreft, Nikodem Kernbach"
__email__ = "raphaelkreft@gmx.de"
__status__ = "rdy"

import statistics

import utils.textinit
from .textfeature import Textfeature


class Paragraphs(Textfeature):
    """ This class inherits from the Textfeature superclass. It is used for the foreign words feature
    """
    def analyse(self, text):
        """ This function returns the number of paragraphs in a text using space recognition.
        :param text: The given text.
        :return dict: The dictionary entry with the number of paragraphs, paragraph mean length and the paragraph mean length per textlength.
        """
        abs_list = text.split("\n\n")
        result_list = []
        for absatz in abs_list:
            result_list.append(utils.textinit.word_count(absatz))

        anz_absaetze = len(result_list)
        abs_mean = statistics.mean(result_list)
        abs_per_word = anz_absaetze / utils.textinit.word_count(text)
        par_mean_per_lenght = abs_mean / utils.textinit.word_count(text)
        return {"paragraphs": abs_per_word, "paragraph_lenght": abs_mean, 'paragraph_lenght_per_textlenght': par_mean_per_lenght}
