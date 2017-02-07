#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""abbreviations.py: This file counts the used abbreviations in a text."""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Julian Behringer"
__email__ = "julian.b@hringer.de"
__status__ = "rdy"

import textfeatures.databases.manage as DB
from .textfeature import Textfeature
import utils.textinit as TI


class Abbreviations(Textfeature):
    """ This class inherits from the Textfeature superclass. It is used for the abbreviation feature
    """
    def analyse(self, text):
        """ This function returns the number of abbreviations in a text using the LookUpList database.
        :param text: The given text.
        :return dict: The dictionary entry with the number of abbreviations.
        """
        Database = DB.LookUpList()  # creating object. No need to connect manually
        words = text.split(' ')
        abbreviations = 0
        for word in words:
            v = Database.check_abbreviation(word)
            if not v:
                pass
            else:
                abbreviations += 1  # no need to disconnect manually
        abbreviations = abbreviations / TI.word_count(text)
        return {"abbreviations": abbreviations}
