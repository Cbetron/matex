#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""textinit.py: This module initializes and organizes the text."""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Nikodem Kernbach, Raphael Kreft"
__email__ = "kernbach@phaenovum.de"
__status__ = "dev"

import string
import contextlib
import re
import sys
import random
import os
import codecs
import textract
import textstat.textstat as TS
import textfeatures.databases.manage as DB


def getsets(path):
    try:
        return [[int(file.split("_")[0]), get_raw_text(path + file)] for file in os.listdir(path)]
    except FileNotFoundError:
        print("The Path {} doesnt exists...".format(path))
        sys.exit(1)


def personal_splice(l, factor, key=False, rand=False):
    splicesize = round(len(l) * factor)
    if rand:
        random.shuffle(l)
    if key:
        l = [item[key] for item in l]
    return l[:splicesize]


def check_occurrences(l, occuring, template, key=""):
    if key:
        l = [item[key] for item in l]
    for i in template:
        if l.count(i) < occuring:
            return False
    return True


def check_treatability(l, occuring, template, occurekey=False):
    if occurekey:
        l = [item[occurekey] for item in l]
    for cls in template:
        if l.count(cls) < occuring * 2:
            return False
    return True


def personal_list_split(l, factor, occuring, template, occurekey=False, selectkey=False):
    splice_one = []
    splice_two = []
    if not check_treatability(l, occuring, template, occurekey):
        raise ValueError
    while not check_occurrences(splice_one, occuring, template, key=occurekey) and not check_occurrences(splice_two, occuring, template, key=occurekey):
        splice_one = personal_splice(l, factor, rand=True, key=selectkey)
        if selectkey:
            splice_two = [item[selectkey] for item in l if item not in splice_one]
        else:
            splice_two = [item for item in l if item not in splice_one]
    return splice_one, splice_two


def personal_list(l, factor, occuring, template, occurekey=False):
    splice_one = []
    if not check_treatability(l, occuring / 2, template, occurekey):
        raise ValueError
    while not check_occurrences(splice_one, occuring, template, key="grade"):
        splice_one = random.sample(l, int(len(l)*factor))
    rest = [item for item in l if item not in splice_one]
    return splice_one, rest


def get_raw_text(filepath):
    """
    Funktion zum Extrahieren von Rohtext aus Pdf oder anderen Formaten die "plain Text" enthalten
    :param filepath: Der Name der Datei aus der extrahiert werden soll
    :return: text: Der extrahierte Rohtext
    """
    SUPPORTED_ENDINGS = ['.pdf', '.doc', '.docx', '.odt', '.rtf']
    if any(filepath.endswith(ending) for ending in SUPPORTED_ENDINGS):
        content = textract.process(filepath)
        text = content.decode('UTF-8')
        return text
    else:
        try:
            with contextlib.closing(open(filepath, 'r')) as file:
                text = codecs.open(filepath, encoding="utf-8-sig").read()
                return text
        except ValueError:
            print("Trainingssets have to be encoded in unicode!")


def cleantext(text):
    """ This function cleans a text from nonalphanumerical signs
    :param text: The text which is to be cleaned
    :return cleantext: The cleaned text
    """
    cleantxt = ""
    filtertxt = filter((string.ascii_letters + string.whitespace).__contains__, str(text))
    for letter in list(filtertxt):
        cleantxt += str(letter)
    return cleantxt


def get_sentence_generator(text):
    """ This function splits a text in its sentences and returns the separated lines
    :param text: The text which is to be sorted
    :return sentence: The separated sentences in a generator
    """
    Database = DB.LookUpList()
    abbreviations = Database.get_abbreviations()
    text = text.replace('\n', '%,%,%')
    wordlist = re.split(' |%,%,%', text)
    for i in range(len(wordlist)):
        if wordlist[i] in abbreviations:
            print('word is an abbreviation, doing nothing...')
        else:
            if '.' in wordlist[i]:
                wordlist[i] += '\n'
            if '?' in wordlist[i]:
                wordlist[i] += '\n'
            if '!' in wordlist[i]:
                wordlist[i] += '\n'
    text = ' '.join(wordlist)
    text = text.split('\n ')
    for sentence in text:
        sentence += '\n'
        yield sentence


def word_count(text):
    return TS.textstat.lexicon_count(text)


if __name__ == "__main__":
    print(check_occurences(
        [[0, 'd'], [0, 'df'], [0, 'dd'], [1, 'f'], [1, 'fd'], [1, 'gg'], [2, 'wq'], [2, 'qa'], [2, 'dsa']],
        [[0, 'd'], [0, 'df'], [0, 'dd'], [1, 'f'], [1, 'fd'], [1, 'gg'], [2, 'wq'], [2, 'qa'], [2, 'dsa']], 2,
        range(3)))
    print([range(3)])
