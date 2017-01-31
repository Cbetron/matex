#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""absatze.py:	Diese Datei ist Teil der Textanalyse"""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Raphael Kreft, Nikodem Kernbach"
__email__ = "raphaelkreft@gmx.de"
__status__ = "dev"

import statistics
import sys
from .textfeature import Textfeature
import utils.textinit as TI

class Paragraphs(Textfeature):

    def analyse(self, text):
        """
        Diese funktion extrahiert die Absätze aus einem Text und analysiert Häufigkeit und Länge
        :param text: Der Text, von dem der Umgang mit Absätzen analysiert weren soll
        :return: anz_absaetze: Anzahl dr im text vorkommenden Absätze
                    abs_mean: Durchschnittliche Länge der Absätze
        """
        # Text nach Absätzen teilen
        abs_list = text.split("\n\n")
        # länge jedes Absatzes in neuer Liste
        result_list = []
        for absatz in abs_list:
            result_list.append(TI.word_count(absatz))
        # berechnen der Anzahl & Durchschn. Länge der Absätze
        anz_absaetze = len(result_list)
        abs_mean = statistics.mean(result_list)
        abs_per_word = anz_absaetze / TI.word_count(text)
        par_mean_per_lenght = abs_mean/TI.word_count(text)
        return {"paragraphs": abs_per_word, "paragraph_lenght": abs_mean, 'paragraph_lenght_per_textlenght': par_mean_per_lenght}


if __name__ == "__main__":
    """
    Aufgerufen wenn script vom Benutzer ausgeführt wird wird als Testfunktion verstanden
    """

    try:
        with open(sys.argv[1]) as f:
            Text = f.read()
            #print(absaetze(Text))

    except Exception as err:
        print("An Exception has occured...\n\n")
        print(err)
        sys.exit(1)


