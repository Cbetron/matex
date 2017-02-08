#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
pythonfile.py:	Checking all combinatons of features in a profile and saves its validationresults
                The Resultfile could have a size of 42 KB the Computing could take a lot of time c.a. 6-8h
"""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Raphael Kreft"
__version__ = "Development v0.0"
__email__ = "raphaelkreft@gmx.de"
__status__ = "Dev"

import datetime
import gzip
import itertools
import pickle
import statistics

from ML.validation import Validation
from ML.profile import Profile
from utils.textinit import *


def percentage(part, amount):
    return part / (amount / 100)


def combis(l):
    length = len(l)
    combinelist = []
    for i in range(length + 1):
        for templist in itertools.combinations(l, i):
            combinelist.append(list(templist))
    return combinelist


def validation(combination, valsets, profile):
    accuracies = [[], []]
    variances = [[], []]
    for i in range(10):
        print(str(i))
        validationsets = random.sample(valsets, round(len(valsets) / 2))
        print("Valsets gen")
        an, vn = Validation().profile_test(profile, validationsets, usedvalues=combination, factors=False)
        print("Profiletest1")
        ac, vc = Validation().profile_test(profile, validationsets, usedvalues=combination, factors=True)
        accuracies[0].append(an)
        accuracies[1].append(ac)
        variances[0].append(vn)
        variances[1].append(vc)
    accuracies[0], accuracies[1] = statistics.mean(accuracies[0]), statistics.mean(accuracies[1])
    return {"Combination": combination, "Accuracies": accuracies, "Variances": variances}


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def dicts(dumpname):
    with open(dumpname, "rb") as f:
        return pickle.load(f)


def save_results(filename, results):
    print("\033[92mWrite results to File...\033[0m")
    file = gzip.open(str(filename), "wb")
    # Write the header of the File
    file.write(bytes("# Number of Combinations: " + str(len(results)) + "\n", "utf-8"))
    file.write(bytes("# Date: " + str(datetime.datetime.now()) + "\n", "utf-8"))
    file.write(bytes("# Encoding:   utf-8\n", "utf-8"))
    # Write the Results to the File
    for result in results:
        file.write(bytes(
            "-\nCombination:{}\nAccuracy:{}\nVariance:{}\n".format(result["Combination"], result["Accuracies"],
                                                                   result["Variances"])))
        file.flush()
    file.close()


def combinations(basis, featureamount):
    ll = []
    for combination in combis([item for item in featureamount if item not in basis]):
        templist = basis
        templist.extend(combination)
        ll.append(templist)
    return ll


if __name__ == "__main__":
    print("Starting")
    num_threads = 4
    sets = dicts("trainingsets/pickleddicts/kaggle_one_six.pkl")
    allfeatures = [item for item in sets[0]["features"].keys()]
    print("split Sets")
    trainingsets, vsets = personal_list_split(sets, 0.7, 3, range(1, 7, 1), occurekey="grade")
    print("make Profile and add factors to it")
    myProfile = Validation().adding_factors(vsets, Profile("Validationprofile", trainingsets, sets).get_profile())
    conclusion = []
    featurebase = ["comma_count", "other_adjectives", "modal_verbs", "other_adverbs", "gerunds_and_ing-form",
                   "auxiliaries", "negation_modifiers", "flesch_index", "flesch_grade", "automated_readability",
                   "sentence_length", "sentences_per_textlen", "typetokenrelation", "words", "spellcheck_pyenchant",
                   "difficult_words", "foreignWord", "conjunctions", "possessive_pronouns", "conjuncts",
                   "coordinations"]
    print("Determine Combinations")
    comb = combinations(featurebase, allfeatures)
    for num, combi in enumerate(comb):
        print("At Percentage: {}".format(percentage(num, len(comb))))
        conclusion.append(validation(combi, vsets, myProfile))
        print(conclusion)
    # Save The results in a zipfile
    save_results("results.txt", conclusion)
