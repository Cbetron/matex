#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""sentenceLength.py: This file analyses the sentences of a text."""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Raphael Kreft, Nikodem Kernbach"
__email__ = "raphaelkreft@gmx.de"
__status__ = "rdy"

import statistics

import utils.textinit
from  .textfeature import Textfeature


class Satzlaenge(Textfeature):
    """ This class inherits from the Textfeature superclass. It is used for the sentencelength feature.
    """
    def analyse(self, text):
        """ This function returns different values connected to sentence length and structure.
        :param text: The given text.
        :return dict: The dictionary entry with the average number of sentences, the maximal and minimal sentence length, the sentence length median and sentences per textlenth.
        """
        len_list = []
        for sentence in utils.textinit.get_sentence_generator(text):
            len_list.append(len(sentence))
        # Rückgabewerte berechnen
        durchschnitt = statistics.mean(len_list)
        anz = len(len_list)
        maximum = max(len_list)
        minimum = min(len_list)
        median = statistics.median(len_list)
        return {'sentence_lenght': durchschnitt, 'max_sentence_len': maximum, 'min_sentence_len': minimum, 'median_sentence_len': median, 'sentences_per_textlen': anz / utils.textinit.word_count(text)}
