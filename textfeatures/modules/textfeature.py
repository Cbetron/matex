#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""pythonfile.py:	Description of pythonfile.py"""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Raphael Kreft"
__email__ = "raphaelkreft@gmx.de"
__status__ = "dev"


class Textfeature(object):
    """
    Die Klasse, vonder jedes Textfeature erbt.
    Sie enthält die Grundsätzliche Struktur eines textfeature
    """
    __weight = None

    def get_weight(self):
        """
        """
        return self.__weight

    def set_weight(self, weight):
        """
        """
        self.__weight = weight

    def analyse(self, text):
        """
        """
        return
