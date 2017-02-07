#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""foreignWord.py: This file counts the used foreign words in a text."""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Julian Behringer"
__email__ = "julian.b@hringer.de"
__status__ = "rdy"

import textfeatures.databases.manage as DB
import utils.textinit as TI
from .textfeature import Textfeature
import textfeatures.parsing.parser as PRS


class ForeignWord(Textfeature):
    """ This class inherits from the Textfeature superclass. It is used for the foreign words feature
    """
    def analyse(self, text):
        """ This function returns the number of foreign words in a text using the LookUpList database.
        :param text: The given text.
        :return dict: The dictionary entry with the number of foreign words.
        """
        Database = DB.LookUpList()
        cleantext = TI.cleantext(text)
        words = cleantext.split(' ')
        foreignWord = 0
        for word in words:
            v = Database.get_word_count(word)
            if v:
                if PRS.foreign_word(word):
                    foreignWord += 1
                else:
                    pass
            else:
                foreignWord += 1
        return {"foreignWord": foreignWord}
