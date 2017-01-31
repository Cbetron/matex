#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""typetoken.py:	Diese Datei ist Teil der Wortwahl"""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Julian Behringer"
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
