#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""textfeature.py: The superclass of all Textfeatures"""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Raphael Kreft"
__email__ = "raphaelkreft@gmx.de"
__status__ = "dev"


class Textfeature(object):
    """
    The superclass of every textfeature class with the analyse function.
    It is used to get instances of all Subclasses
    """

    def analyse(self, text):
        """
        This function is the analyse function of every textfeature, which analyses the text under one specific aspect
        :param text: The text to be analysed
        """
        return
