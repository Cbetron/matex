#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""manager.py: This is the file which manages all textfeautures"""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Raphael Kreft"
__email__ = "raphaelkreft@gmx.de"
__status__ = "dev"

from textfeatures.parsing.parser import parse
from utils.pdfcreator import PDF
from textfeatures.modules.textfeature import Textfeature
from textfeatures.modules import wordLength
from textfeatures.modules import abbreviations
from textfeatures.modules import foreignWord
from textfeatures.modules import paragraph
from textfeatures.modules import parseAnalyse
from textfeatures.modules import rareWords
from textfeatures.modules import readability
from textfeatures.modules import sentenceLength
from textfeatures.modules import spellchecker
from textfeatures.modules import syllabus
from textfeatures.modules import typetoken


class Manager(object):
    def __init__(self, ignorefeature=None, pdf=""):
        if ignorefeature is None:
            ignorefeature = []
        self.ignorefeature = ignorefeature
        self.vars = globals()
        self.text = None
        self.features = []
        self.load_features()
        if pdf:
            self.pdf = pdf
        else:
            self.pdf = None

    def run(self):
        ergs = {}
        for feature in self.features:
            tempergs = feature().analyse(self.text)
            if tempergs is None:
                print("Keine Daten für Feature {}".format(feature))
                continue
            keys = list(tempergs.keys())
            for key in keys:
                if key in self.ignorefeature:
                    del tempergs[key]
            ergs.update(tempergs)
            if self.pdf:
                self.pdf.insert_featureextraction(ergs)
        return ergs

    def set_text(self, text):
        self.text = text
        parse(text)
        if self.pdf:
            self.pdf.insert_text(self.text)

    def get_text(self):
        return self.text

    def load_features(self):
        self.features = self.vars["Textfeature"].__subclasses__()

    def reset(self):
        self.text = None
        self.load_features()

if __name__ == "__main__":
    Tm = Manager()
    Tm.load_features()

