#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""readability.py: This textfeature checks the readability of the text using the textstat module"""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Nikodem Kernbach"
__email__ = "kernbach@phaenovum.de"
__status__ = "rdy"

from textfeatures.modules.textfeature import Textfeature
import textstat.textstat as TS


class SemiColon(Textfeature):
    """SemiColon is a textfeauture class which analyses the text for good spelling
    """
    def __init__(self):
        super().__init__()
        self.ts = TS.textstatistics()

    def analyse(self, text):
        """" This is the main function of the semi_colon module which includes all other functions
        :param text: The text that should be checked
        :return The dictionary with the readability score entries
        See the following dictionary for the names of readability functions
        """
        ret_dict = {'flesch_index': self.ts.flesch_reading_ease(text),
                    'flesch_grade': self.ts.flesch_kincaid_grade(text),
                    'fog_scale': self.ts.gunning_fog(text),
                    'smog_index': self.ts.smog_index(text),
                    'coleman_index': self.ts.coleman_liau_index(text),
                    'automated_readability': self.ts.automated_readability_index(text),
                    'linsear_formula': self.ts.linsear_write_formula(text),
                    'dale_score': self.ts.dale_chall_readability_score(text)
                    }
        #print("Successful!")
        return ret_dict
