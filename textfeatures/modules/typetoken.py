#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""typetoken.py: This file determines the type-token-relation of a text."""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Julian Behringer"
__email__ = "julian.b@hringer.de"
__status__ = "dev"

import utils.textinit
from .textfeature import Textfeature


class TypeToken(Textfeature):
    """
    This class inherits from the Textfeature superclass. It is used for the type-token feature
    """
    def analyse(self, text):
        """
        This function returns the type-token-relation.
        :param text: The given text.
        :return dict: The dictionary entry with the type-token-relation.
        """
        cleantext = utils.textinit.cleantext(text).lower()
        words = cleantext.split(' ')
        token = len(words)
        woerter_type = set(words)
        type = len(woerter_type)
        typetokenrelation = type / token * 100
        return {"typetokenrelation": typetokenrelation}
