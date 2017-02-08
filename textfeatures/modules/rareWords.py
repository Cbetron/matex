#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""rareWords.py: This file counts the rare words in a text."""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Julian Behringer"
__email__ = "julian.b@hringer.de"
__status__ = "rdy"

import textfeatures.databases.manage as DB
import utils.textinit
from .textfeature import Textfeature


class RareWords(Textfeature):
    """
    This class inherits from the Textfeature superclass. It is used for the rare words feature
    """
    def analyse(self, text):
        """
        This function returns the number of rare words in a text using the LookUpList database.
        :param text: The given text.
        :return dict: The dictionary entry with the number of rare words.
        """
        Database = DB.LookUpList()
        avg = Database.counter_average()
        limit = avg*0.5
        cleantext = utils.textinit.cleantext(text)
        words = cleantext.split(' ')
        rareWords = 0
        for word in words:
            v = Database.get_word_count(word)
            if v:
                if v[0] > limit:
                    pass
                else:
                    rareWords += 1
            else:
                rareWords += 1
        rareWords = rareWords / utils.textinit.word_count(text)
        return {"rareWords": rareWords}
