#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""readability.py: This textfeature chechs the readability of the text using the textstat module"""

__author__ = "Nikodem Kernbach"
__email__ = "kernbach@phaenovum.de"
__status__ = "dev"

from textfeatures.modules.textfeature import Textfeature
import textstat.textstat as TS


class SemiColon(Textfeature):
    """SemiColon is a textfeauture class which analyzed the text for good spelling
    """
    def __init__(self):
        super().__init__()
        self.text_statistics = TS.textstatistics()

    def analyse(self, text):
        """" This is the main function of the semi_colon module which includes all other functions
        :param text: The text that should be checked
        :return The dictionaries of the respective functions
        See following functions for further information
        """
        ret_dict = {'flesch_index': self.flesch_reading_ease_index(text),
                    'flesch_grade': self.flesch_kincaid_grade(text),
                    'fog_scale': self.fog_scale(text),
                    'smog_index': self.smog_index(text),
                    'coleman_index': self.coleman_liau_index(text),
                    'automated_readability': self.automated_readability_index(text),
                    'linsear_formula': self.linsear_write_formula(text),
                    'dale_score': self.dale_chall_readability_score(text)
                    }
        #print("Successful!")
        return ret_dict

    def flesch_reading_ease_index(self, text):
        flesch_index = self.text_statistics.flesch_reading_ease(text)
        return flesch_index

    def flesch_kincaid_grade(self, text):
        flesch_grade = self.text_statistics.flesch_kincaid_grade(text)
        return flesch_grade

    def fog_scale(self, text):
        fog_scale = self.text_statistics.gunning_fog(text)
        return fog_scale

    def smog_index(self, text):
        smog_index = self.text_statistics.smog_index(text)
        return smog_index

    def coleman_liau_index(self, text):
        coleman_index = self.text_statistics.coleman_liau_index(text)
        return coleman_index

    def automated_readability_index(self, text):
        automated_readability = self.text_statistics.automated_readability_index(text)
        return automated_readability

    def linsear_write_formula(self, text):
        linsear_formula = self.text_statistics.linsear_write_formula(text)
        return linsear_formula

    def dale_chall_readability_score(self, text):
        dale_score = self.text_statistics.dale_chall_readability_score(text)
        return dale_score
