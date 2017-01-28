#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""abbreviations.py:	Diese Datei ist Teil der Wortwahl"""

__author__ = "Julian Behringer"
__copyright__ = ""
__credits__ = ""

__license__ = ""
__version__ = "0.1"
__email__ = "julian.b@hringer.de"
__status__ = "dev"

import textfeatures.databases.manage as DB
from .textfeature import Textfeature
import utils.textinit as TI


class Abbreviations(Textfeature):
    def analyse(self, text):
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
