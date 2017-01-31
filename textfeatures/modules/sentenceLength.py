#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""satzlaenge.py:	Diese Datei ist Teil der Textanalyse"""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Raphael Kreft, Nikodem Kernbach"
__email__ = "raphaelkreft@gmx.de"
__status__ = "dev"

import statistics
import sys
from  .textfeature import Textfeature
import utils.textinit as TI


class Satzlaenge(Textfeature):
    """
    Dieses Textfeature erbt seine Struktur und einige Funktionen von .textfeature.Textfeature
    Analysieren der durchschnittl. Satzlänge und zusammenhängenden Größen
    """
    def analyse(self, text):
        """
        Extrahieren verschieder Informationen über die Satzlänge eines übergebenen Textes
        :param text: Der Text, der analysiert werden soll
        :return: Der berechnete Durchschnitt, Anzahl der Sätze, längster, kürzester und median
        """
        len_list = []
        for sentence in TI.get_sentence_generator(text):
            len_list.append(len(sentence))
        # Rückgabewerte berechnen
        durchschnitt = statistics.mean(len_list)
        anz = len(len_list)
        maximum = max(len_list)
        minimum = min(len_list)
        median = statistics.median(len_list)
        return {'sentence_lenght': durchschnitt, 'max_sentence_len': maximum, 'min_sentence_len': minimum, 'median_sentence_len': median, 'sentences_per_textlen': anz/TI.word_count(text)}


if __name__ == "__main__":
    """
    Aufgerufen wenn script vom Benutzer ausgeführt wird
    """
    try:
        with open(sys.argv[1], "r") as f:
            text = f.read()
            sl = Satzlaenge()
            sl.analyse(text)
            print(sl.get_value())

    except IndexError:
        print("No Argument given\n\n")
        sys.exit(1)
    except FileNotFoundError:
        print("Argument should be the Name of a File")
        sys.exit(1)
