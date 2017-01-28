#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""rareWords.py:	Diese Datei ist Teil der Wortwahl"""

__author__ = "Julian Behringer"
__copyright__ = ""
__credits__ = ""

__license__ = ""
__version__ = "0.1"
__email__ = "julian.b@hringer.de"
__status__ = "dev"

import textfeatures.databases.manage as DB
import utils.textinit as TI
from .textfeature import Textfeature


class RareWords(Textfeature):
    def analyse(self, text):
        Database = DB.LookUpList()
        avg = Database.counter_average()
        limit = avg*0.5
        cleantext = TI.cleantext(text)
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
        rareWords = rareWords/TI.word_count(text)
        return {"rareWords": rareWords}
