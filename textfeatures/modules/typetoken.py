#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""typetoken.py:	Diese Datei ist Teil der Wortwahl"""

__author__ = "Julian Behringer"
__copyright__ = ""
__credits__ = ""

__license__ = ""
__version__ = "0.1"
__email__ = "julian.b@hringer.de"
__status__ = "dev"

import utils.textinit as TI
from .textfeature import Textfeature


class TypeToken(Textfeature):
    def analyse(self, text):
        cleantext = TI.cleantext(text).lower()
        words = cleantext.split(' ')
        token = len(words)
        woerter_type = set(words)
        type = len(woerter_type)
        typetokenrelation = type / token * 100
        return {"typetokenrelation": typetokenrelation}
