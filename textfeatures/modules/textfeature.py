#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""pythonfile.py:	Description of pythonfile.py"""

__author__ = "Raphael Kreft"
__copyright__ = "Copyright (c) 2016 Raphael Kreft"
__version__ = "Development v0.0"
__email__ = "raphaelkreft@gmx.de"
__status__ = "Dev"


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
