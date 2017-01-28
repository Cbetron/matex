#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""spellchecker.py: This textfeauture checks the spelling of the text"""

__author__ = "Nikodem Kernbach"
__email__ = "kernbach@phaenovum.de"
__status__ = "rdy"

import utils.textinit as TI
import textfeatures.modules.textfeature as TF
import textfeatures.databases.manage as DB
import enchant

class Spellchecker(TF.Textfeature):
    def __init__(self):
        super().__init__()

    def analyse(self, text):
        """ This function checks if the words in the given text are correct
        :param text: The text that should be checked
        :return ret_dict: The dictionary for ML
        The function writes directly into the pdf and uses the 'lookuplist' database to check the words
        """
        Database = DB.LookUpList()
        counter = 0
        cleantext = TI.cleantext(text)
        words = cleantext.split(' ')
        for word in words:
            check = Database.get_word_count(word)
            if not check:
                counter += 1  # The word is not recognized and an warning will be raised... pdfoutput...
            else:
                pass  # Word is recognized, nothing else happens
        counter = counter/TI.word_count(text)
        word_dictionary = enchant.Dict('en_US')
        enchant_counter = 0
        for word in words:
            if word:
                if not word_dictionary.check(word):
                    enchant_counter += 1
        enchant_counter = enchant_counter/TI.word_count(text)
        ret_dict = {'spelling_mistakes': counter, 'spellcheck_pyenchant': enchant_counter}
        #print("SPELLCHECKER:\t successfully finished")
        return ret_dict
