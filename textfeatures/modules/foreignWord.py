#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""foreignWord.py:	Diese Datei ist Teil der Wortwahl"""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Julian Behringer"
__email__ = "julian.b@hringer.de"
__status__ = "dev"

import textfeatures.databases.manage as DB
import utils.textinit as TI
from .textfeature import Textfeature
import textfeatures.parsing.parser as PRS


class ForeignWord(Textfeature):
    def analyse(self, text):
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
