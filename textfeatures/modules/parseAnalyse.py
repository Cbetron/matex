# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""parseAnalyze.py: This textfeauture analyses the text extracting information from the 'parsed' databse"""

__author__ = "Nikodem Kernbach"
__email__ = "kernbach@phaenovum.de"
__status__ = "dev"

import textfeatures.modules.textfeature as TF
import textfeatures.databases.manage as DB
import utils.textinit as TI


class ParseAnalyse(TF.Textfeature):
    """This class is the Textfeauture class of the parseAnalyse module
    """
    modifier_relations_list = ['nn', 'amod', 'advmod', 'num', 'poss', 'rcmod', 'advcl', 'possesive', 'appos',
                               'partmod', 'neg', 'quantmod', 'tmod', 'infmod', 'npadvmod']

    word_type_list = [
        ['conjunctions', 'CONJ'],
        ['nouns', 'NOUN'],
        ['verbs', 'VERB']
    ]

    word_tag_list = [
        ['comma_count', ','],
        #['cardinal_numbers', 'CD'],
        #['hyphen_count', 'HYPH'],
        #['superlative_adjectives', 'JJS'],
        #['comparative_adjectives', 'JJR'],
        ['adjectives', ['JJ', 'JJS', 'JJR']],
        #['list_item_markers', 'LS'],
        ['modal_verbs', 'MD'],
        #['predeterminers', 'PDT'],
        #['superlative_adverbs', 'RBS'],
        #['comparative_adverbs', 'RBR'],
        ['adverbs', ['RB', 'RBS', 'RBR']],
        #['symbols', 'SYM'],
        #['interjections', 'UH'],
        ['gerunds_and_ing-form', 'VBG'],
        #['proper_nouns', ['NNP', 'NNPS']],
        ['possessive_pronouns', ['PRP$', 'WP$']]
    ]

    word_relation_list = [
        ['auxiliaries', 'aux'],
        ['conjuncts', 'conj'],
        ['coordinations', 'cc'],
        ['markers_count', 'mark'],
        #['passive_auxiliaries', 'auxpass'],
        #['passive_nominal_subjects(passive_sentences)', 'nsubjpass'],
        #['compound_numbers', 'number'],
        #['parataxes', 'parataxis'],
        #['multi_word_expressions', 'mwe'],
        #['expletives', 'expl'],
        #['discourse_elements', 'discourse'],
        #['preconjuncts', 'preconj'],
        ['negation_modifiers', 'neg'],
        ['modifiers', modifier_relations_list]
    ]

    def __init__(self):
        super().__init__()
        self.Database = DB.ParsingData()

    def analyse(self, text):
        textlen = TI.word_count(text)
        ret_dict = {}
        for wordtype in self.word_type_list:
            ret_dict.update(self.count_words_prepare_dictionary(wordtype[0], 'wordtype', wordtype[1], textlen))
        for tag in self.word_tag_list:
            ret_dict.update(self.count_words_prepare_dictionary(tag[0], 'wordtag', tag[1], textlen))
        for relation in self.word_relation_list:
            ret_dict.update(self.count_words_prepare_dictionary(relation[0], 'worddeptype', relation[1], textlen))
        return ret_dict

    def count_words_prepare_dictionary(self, name, tag_column, tags, textlen):
        ret_dict = {}
        words = self.Database.get_words_from_database(tag_column, tags)
        count = len(words)
        ret_dict[name] = count/textlen
        return ret_dict
