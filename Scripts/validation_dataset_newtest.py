#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""validation_dataset.py:	A Script for the advanced use of the validation base_module"""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Raphael Kreft"
__version__ = "Development v0.0"
__email__ = "raphaelkreft@gmx.de"
__status__ = "Dev"

import statistics
import copy
import contextlib
import os

from ML import validation, profile
from utils import textinit


def trainingset_validation(path, name, toexclude=None, usefeatures=None):
    trainingsets, removedfeatures = textinit.trainingset_extraction(path)
    rating = list(set([trainingset["grade"] for trainingset in trainingsets]))
    featurelist = list(trainingsets[0]["features"].keys())
    if usefeatures:
        toexclude = [feature for feature in featurelist if feature not in usefeatures]
        featurelist = usefeatures
    results = []
    feature_accuracies = {}
    for feature in featurelist:
        feature_accuracies[feature] = []
    for i in range(100):
        print("{}. Test from {}".format(i + 1, 100))
        while True:
            try:
                tset, valset = textinit.personal_list_split(trainingsets, 0.6, 3, rating, occurekey="grade")
                myprofile = profile.Profile("Gandalfszauberhuette", tset, trainingsets, excludefeatures=toexclude)
                tmp_profile = copy.deepcopy(myprofile)
                new_profile, ergs = validation.profile_validation(tmp_profile, valset, rating=rating, multitest=2,
                                                                  toexclude=toexclude)
                for feature in featurelist:
                    feature_accuracies[feature].append(
                        validation.feature_accuracy(feature, valset, myprofile.get_profile())[1])
                break
            except ZeroDivisionError:
                continue
            except ValueError:
                continue
            except Exception:
                continue
        results.append(ergs)
    n = (statistics.mean([ergs[0][0] for ergs in results]), statistics.mean([ergs[1][0] for ergs in results]))
    c = (statistics.mean([ergs[0][1] for ergs in results]), statistics.mean([ergs[1][1] for ergs in results]))
    b = (statistics.mean([ergs[0][2] for ergs in results]), statistics.mean([ergs[1][2] for ergs in results]))
    bf = (statistics.mean([ergs[0][3] for ergs in results]), statistics.mean([ergs[1][3] for ergs in results]))
    # Write Results to file
    with contextlib.closing(open("traininset_validation_{}.txt".format(name), "w")) as f:
        f.write(
            "Feature Accuracy for all Features in your Trainingsets after removing Features, that makes no sense:\n\n")
        for feature in featurelist:
            erg = statistics.mean(feature_accuracies[feature])
            f.write("{}:\t{}\n".format(feature, erg))
        f.write("\n\nBest Features: {}".format("soon"))
        f.write("\nFeatures excluded by yourself: {}\n".format(toexclude))
        f.write("\nFeatures that were removed by the filter a cause of invalid values:\t{}\n".format(removedfeatures))
        f.write("\n\nProfiles with your trainingsets got an average Accuracy and Variance of:\n")
        f.write("Naive Bayes Normal: {}, {}\n".format(*n))
        f.write("Naive Bayes Faktoren: {}, {}\n".format(*c))
        f.write("Naive Bayes Best Features: {}, {}\n".format(*b))
        f.write("Naive Bayes Best Features with factors: {}, {}\n".format(*bf))


path = os.getcwd() + input("path to training Data: ")
exclude = []
sortedaccuracie = ["words", "difficult_words", "typetokenrelation", "smog_index", "longest_word", "verbs", "modifiers", "max_sentence_len", "markers_count", "adjectives", "sentences_per_textlen"]
for i in range(1, 12):
    use = sortedaccuracie[:i]
    trainingset_validation(path, i, exclude, use)
