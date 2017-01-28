#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""pythonfile.py:	A validation_class"""

__author__ = "Raphael Kreft"
__copyright__ = "Copyright (c) 2016 Raphael Kreft"
__version__ = "Development v0.0"
__email__ = "raphaelkreft@gmx.de"
__status__ = "Dev"

import pickle
import datetime
from operator import itemgetter
import copy
from collections import defaultdict
from utils.textinit import *
from ML.Classifier import Classifier
from ML.profile import Profile
from ML.vectors_matrix import *


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


def validation(profile, validation_sets, setamountfactor=0.75):
    """
    Validation of a Profile made via Bayes-classification Check accuracy of normal, Factor-modified
    and Multivariant version of our Profile and saves the Accuracies in the profile.
    :param setamountfactor: The factor how to split the sets for correction and validation
    """
    correctionsets, testsets = personal_list(validation_sets, setamountfactor, 2, range(1, 7, 1), occurekey="grade")
    # Test profile with normal gauss-distribution
    percentage_n, var_n = profile_test(profile, testsets)
    # test profile with multivariant Gauss-distribution
    # percentange_m = self.profile_test(self.profile, testsets, multivariant=True)
    correctedprofile = adding_factors(correctionsets, profile)
    percentage_c, var_c = profile_test(correctedprofile, testsets, factors=True)
    # Determine best features and test classification with that combination
    best_combi_profile = best_features(correctedprofile)
    best_combi_profile.dump_profile()
    percentage_b, var_b = profile_test(best_combi_profile, testsets, usedvalues=best_combi_profile.get_profile()["best-features"], factors=True)
    return best_combi_profile, [[percentage_n, var_n], [percentage_c, var_c], [percentage_b, var_b]]


def profile_test(profile, valsets, usedvalues="", multivariant=False, factors=False):
    """
    Test a Profile and return the accuracy and the variance of wrong classified Texts
    :param profile: The profile you want to test
    :param valsets: the validationsets that are used to test the profile
    :param multivariant: Want to check the multivariant version of the Profile?
    :return: percentage of accuracy, the variance
    """
    classifier = Classifier(profile.get_profile())
    results = {"wrong": 0, "right": 0}
    variances = []
    for valset in valsets:
        cls_mark = classifier.classify(valset["features"], usedvalues=usedvalues, multivariant=multivariant,
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
    for fname in list(nprofile[str(nprofile["rating"][0])].keys()):
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
    likelyhoods = [(cls, Classifier(profile).feature_likelihood(value, *profile[str(cls)][featurename])) for cls in
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
        factors[cls] = (4 - correct / len(cls_valsets))*0.01
    return [factors, mean([factors[cls] for cls in profile["rating"]])]


def best_features(profile):
    """
    Save the best Features in the profile Factors zw: 0.04 - 0.03
    :param profile: The Profile
    :return:
    """
    threshold = 0.036
    rating = profile.get_profile()["rating"]
    accurate_features = []
    for feature in list(profile.get_profile()[str(rating[0])].keys()):
        if feature in ["covariancematrice", "prior"]:
            continue
        featurevals = []
        for cls in rating:
            featurevals.append(profile.get_profile()[str(cls)][feature][2])
        if mean(featurevals) <= threshold:
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
            nprofile[str(cls)][fname][2] = factor
            if factor == 0:
                skip.append(fname)
                for c in nprofile["rating"]:
                    del nprofile[str(c)][fname]
                    del factors[c][fname]
    profile.set_profile(nprofile)
    return profile


if __name__ == "__main__":
    print("starting Validationtest...")
    with open("trainingsets/pickleddicts/kaggle_one_six.pkl", "rb") as dumbfile:
        dict_list = pickle.load(dumbfile)
    print("Split Trainingsets...")
    tsets, valsets = personal_list_split(dict_list, 0.7, 4, range(1, 7, 1), occurekey="grade")
    print("Make Profile object")
    profile = Profile("Test", tsets, dict_list)
    print("Done!")
    print("Validation")
    ergs = validation(profile, dict_list)
    print(ergs)
    # newprofile = adding_factors(valsets, Profile("Test", tsets, dict_list, rating=range(1, 7, 1)))
    # myprofile = best_features(newprofile)
    # newprofile.save_factors()
    # accuracies, variances = Validation().validation(myProfile.get_profile(), valsets)
