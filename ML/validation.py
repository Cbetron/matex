#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""pythonfile.py:	A validation_class"""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Raphael Kreft"
__version__ = "Development v0.0"
__email__ = "raphaelkreft@gmx.de"
__status__ = "Dev"

import statistics
from operator import itemgetter
import copy

from ML.classifier import Classifier
from ML.profile import Profile
from ML.vectors_matrix import *
from utils.textinit import *


def base_validation(results, human_mark, classifyer_mark):
    """
    Look if the gradings of humans and classsifier fits. Increasing bNumbers in results-list
    :param human_mark: grading from a human person
    :param classifyer_mark: grading from the classifier to check
    :return: -
    """
    if human_mark is classifyer_mark:
        results["right"] += 1
    else:
        results["wrong"] += 1
    diff = abs(human_mark - classifyer_mark)
    return results, diff


def profile_validation(profile, validation_sets, rating, toexclude, setamountfactor=0.75, multitest=10):
    """
    Validation of a Profile made via Bayes-classification Check accuracy of normal, Factor-modified
    and Multivariant version of our Profile and saves the Accuracies in the profile.
    :param setamountfactor: The factor how to split the sets for correction and validation
    """
    correctionsets, testsets = personal_list(validation_sets, setamountfactor, 2, rating, occurekey="grade")
    # add factors and delete fature with factors == 0
    correctedprofile = adding_factors(correctionsets, profile)
    best_combi_profile = best_features(correctedprofile)
    acc_n, acc_c, acc_b, acc_bf = [], [], [], []
    var_n, var_c, var_b, var_bf = [], [], [], []
    for i in range(multitest):
        try:
            correctionsets, testsets = personal_list(validation_sets, setamountfactor, 2, rating,
                                                     occurekey="grade")
            percentage_n, vr_n = profile_test(profile, testsets, toexclude=toexclude)
            percentage_c, vr_c = profile_test(correctedprofile, testsets, factors=True, toexclude=toexclude)
            percentage_b, vr_b = profile_test(best_combi_profile, testsets,
                                              usedvalues=best_combi_profile.get_profile()["best-features"],
                                              factors=False, toexclude=toexclude)
            percentage_b_f, vr_b_f = profile_test(best_combi_profile, testsets,
                                                  usedvalues=best_combi_profile.get_profile()["best-features"],
                                                  factors=True, toexclude=toexclude)

        except ZeroDivisionError:
            continue
        except ValueError:
            continue
        acc_n.append(percentage_n)
        var_n.append(vr_n)
        acc_c.append(percentage_c)
        var_c.append(vr_c)
        acc_b.append(percentage_b)
        var_b.append(vr_b)
        acc_bf.append(percentage_b_f)
        var_bf.append(vr_b_f)
    accuracies = [statistics.mean(acc_n), statistics.mean(acc_c), statistics.mean(acc_b), statistics.mean(acc_bf)]
    variances = [statistics.mean(var_n), statistics.mean(var_c), statistics.mean(var_b), statistics.mean(var_bf)]
    best_combi_profile.insert("Accuracies(n,c,b,bf)", accuracies)
    best_combi_profile.insert("Variances(n,c,b,bf)", variances)
    return best_combi_profile, [accuracies, variances]


def profile_test(profile, valsets, usedvalues="", multivariant=False, factors=False, toexclude=None):
    """
    Test a Profile and return the accuracy and the variance of wrong classified Texts
    :param profile: The profile you want to test
    :param valsets: the validationsets that are used to test the profile
    :param multivariant: Want to check the multivariant version of the Profile?
    :return: percentage of accuracy, the variance
    """
    classifier = Classifier(profile.get_profile(), exclude=toexclude)
    results = {"wrong": 0, "right": 0}
    variances = []
    for valset in valsets:
        cls_mark, evidence = classifier.classify(valset["features"], usedvalues=usedvalues, multivariant=multivariant,
                                                 factors=factors)
        results, diff = base_validation(results, valset["grade"], cls_mark)
        variances.append(diff)
    return percentage(results["right"], sum([item for item in results.values()])), mean(variances)


def adding_factors(correctionsets, profile):
    # Determine factors and Add it to profile
    nprofile = profile.get_profile()
    factors = {}
    for cls in nprofile["rating"]:
        factors[cls] = {}
    for fname in list(nprofile[nprofile["rating"][0]].keys()):
        if fname in ["prior", "covariancematrice"]:
            continue
        fact, m = feature_accuracy(fname, correctionsets, nprofile)
        for cls in nprofile["rating"]:
            factors[cls][fname] = fact[cls]
    return correct_profile(profile, factors)


def feature_class(value, featurename, profile):
    """
    Gibt die Wahrscheinlichste Klasse für den wert eins bestimmtes Feature zurück
    :param value: Der Wert, der geprüft werden soll
           featurename: Name des Features, dessen Klasse ermittelt werden soll
    :return Wahrscheinlichste Klasse
    """
    likelyhoods = [(cls, Classifier(profile).feature_likelihood(value, *profile[cls][featurename])) for cls in
                   profile["rating"]]
    return max(likelyhoods, key=itemgetter(1))[0]


def feature_accuracy(featurename, validationsets, profile):
    """
    Berechnet den Genauigkeitsfaktor eines Features für jede Klasse
    :param featurename: Feature, dessen Faktoren ermittelt werden sollen
    """
    factors = {}
    for cls in profile["rating"]:
        factors[cls] = {}
    for cls in profile["rating"]:
        correct = 0
        cls_valsets = [valset for valset in validationsets if valset["grade"] == cls]
        for valset in cls_valsets:
            mark = valset["grade"]
            if mark == feature_class(valset["features"][featurename], featurename, profile):
                correct += 1
        factors[cls] = correct / len(cls_valsets)
    return [factors, mean([factors[cls] for cls in profile["rating"]])]


# def best_features(profile):
#     """
#     Save the best Features in the profile Factors zw: 0.04 - 0.03
#     :param profile: The Profile
#     :return:
#     """
#     rating = profile.get_profile()["rating"]
#     flist = []
#     for feature in list(profile.get_profile()[str(rating[0])].keys()):
#         if feature in ["covariancematrice", "prior"] or feature in profile.get_profile()["toexclude"]:
#             continue
#         featurevals = []
#         for cls in rating:
#             featurevals.append(profile.get_profile()[str(cls)][feature][2])
#         flist.append((feature, mean(featurevals)))
#     accurate_features = sorted(flist, key=lambda feature: feature[1], reverse=True)[:10]
#     print(accurate_features)
#     profile.insert("best-features", accurate_features)
#     return profile


def best_features(profile, threshold=0.003):
    """
    Save the best Features in the profile Factors zw: 0.04 - 0.03
    :param profile: The Profileobject
    :return:
    """
    rating = profile.get_profile()["rating"]
    accurate_features = []
    for feature in list(profile.get_profile()[rating[0]].keys()):
        if feature in ["covariancematrice", "prior"]:
            continue
        featurevals = []
        for cls in rating:
            featurevals.append(profile.get_profile()[cls][feature][2])
        if mean(featurevals) >= threshold:
            accurate_features.append(feature)
    profile.insert("best-features", accurate_features)
    return profile


def correct_profile(profile, factors):
    """
    Insert the Factors into the Profile. Delete Feature if Accuracy is zero percent
    :return: The Profile with deleted features and inserted factors
    """
    nprofile = profile.get_profile()
    factor_copy = copy.deepcopy(factors)
    skip = []
    for cls in nprofile["rating"]:
        for fname, factor in list(factor_copy[cls].items()):
            if fname in skip:
                continue
            nprofile[cls][fname][2] = factor
            if factor == 0:
                skip.append(fname)
                for c in nprofile["rating"]:
                    del nprofile[c][fname]
                    del factors[c][fname]
    profile.set_profile(nprofile)
    return profile
