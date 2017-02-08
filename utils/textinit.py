#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""textinit.py: This module initializes and organizes the text."""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Raphael Kreft, Nikodem Kernbach"
__email__ = "kernbach@phaenovum.de, raphaelkreft@gmx.de"
__status__ = "dev"

import string
import pickle
import re
import sys
import random
import os
import codecs
import collections
import copy
import textract
import textstat.textstat as TS

import textfeatures.databases.manage as DB
from utils.datascience import *
from textfeatures.manager import Manager


def trainingset_extraction(trainingset_path):
    """

    :param trainingset_path:
    :return:
    """
    trainingsets = []
    if trainingset_path.endswith(".pkl"):
        with open(trainingset_path, "rb")as file:
            trainingsets = pickle.load(file)
    elif os.path.isdir(trainingset_path):
        TF_Manager = Manager()
        for tset in getsets(trainingset_path):
            TF_Manager.set_text(tset[1])
            trainingsets.append({"grade": tset[0], "features": TF_Manager.run()})
    return trainingset_treatability(trainingsets)


def trainingset_treatability(tset):
    """

    :param tset:
    :return:
    """
    removedfeatures = []
    for feature in copy.deepcopy(tset)[0]["features"].keys():
        values = collections.defaultdict(list)
        for ts in tset:
            values[ts["grade"]].append(ts["features"][feature])
        if any([standartdeviation(values[cls]) == 0 for cls in values.keys()]):
            removedfeatures.append(feature)
            for ts in tset:
                del ts["features"][feature]
        else:
            continue
    return tset, removedfeatures


def getsets(path):
    """
    Load all raw texts from a given path
    :param path: read texts from all files in it
    :return list of lists: [grade, text]
    """
    try:
        return [[int(file.split("_")[0]), get_raw_text(path + file)] for file in os.listdir(path)]
    except FileNotFoundError:
        print("The Path {} doesnt exists...".format(path))
        sys.exit(1)


def personal_splice(l, factor, key=False, rand=False):
    """
    Make a personal splice from a list
    :param l: list to make slice from
    :param factor: Factor which defines the size
    :param key: if items are dicts -> get items by key
    :param rand: Shuffle list to make it random
    :return: personal splice
    """
    splicesize = round(len(l) * factor)
    if rand:
        random.shuffle(l)
    if key:
        l = [item[key] for item in l]
    return l[:splicesize]


def check_occurrences(l, occuring, template, key=""):
    """

    :param l:
    :param occuring:
    :param template:
    :param key:
    :return:
    """
    if key:
        l = [item[key] for item in l]
    for i in template:
        if l.count(i) < occuring:
            return False
    return True


def check_treatability(l, occuring, template, occurekey=False):
    """

    :param l:
    :param occuring:
    :param template:
    :param occurekey:
    :return:
    """
    if occurekey:
        l = [item[occurekey] for item in l]
    for cls in template:
        if l.count(cls) < occuring * 2:
            return False
    return True


def personal_list_split(l, factor, occuring, template, occurekey=False, selectkey=False):
    """
    Split a List into two slices, both of them will be userdefined with following Parameters
    :param l: The list to be splitted
    :param factor: Factor which defines the size of the first splice Bsp: 0.7 = 70%
    :param occuring: defines how many items from one template-item have to be in splice_one
    :param template: a list of occurings that will be checked
    :param occurekey: if the items in template are packed in a dict you need to define a key
    :param selectkey: make splices with items extracting from l by a key
    :returns splice_one: a list which fits the requirements splice_two: the rest of list l(also fits the requirements)
    """
    splice_one = []
    splice_two = []
    if not check_treatability(l, occuring, template, occurekey):
        raise ValueError
    while not check_occurrences(splice_one, occuring, template, key=occurekey) and not check_occurrences(splice_two,
                                                                                                         occuring,
                                                                                                         template,
                                                                                                         key=occurekey):
        splice_one = personal_splice(l, factor, rand=True, key=selectkey)
        if selectkey:
            splice_two = [item[selectkey] for item in l if item not in splice_one]
        else:
            splice_two = [item for item in l if item not in splice_one]
    return splice_one, splice_two


def personal_list(l, factor, occuring, template, occurekey=False):
    """
    Split a List into two slices, one of them will be userdefined with following Parameters
    :param l: The list to be splitted
    :param factor: Factor which defines the size of the first splice Bsp: 0.7 = 70%
    :param occuring: defines how many items from one template-item have to be in splice_one
    :param template: a list of occurings that will be checked
    :param occurekey: if the items in template are packed in a dict you need to define a key
    :returns splice_one: a list which fits the requirements rest: the rest of list l
    """
    splice_one = []
    if not check_treatability(l, occuring / 2, template, occurekey):
        raise ValueError
    while not check_occurrences(splice_one, occuring, template, key="grade"):
        splice_one = random.sample(l, int(len(l) * factor))
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
            #print('word is an abbreviation, doing nothing...')
            pass
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
    """
    Count words in a string
    :param text: string to be analysed
    :return Count of words as int
    """
    return TS.textstat.lexicon_count(text)
