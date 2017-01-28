#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""pythonfile.py:	Description of pythonfile.py"""

__author__ = "Raphael Kreft"
__version__ = "Development v0.0"
__email__ = "raphaelkreft@gmx.de"
__status__ = "Dev"

import pickle
import numpy
import itertools
import sys
from operator import itemgetter
from ML.vectors_matrix import *
from utils.textinit import *


class Classifier(object):
    def __init__(self, profile):
        """
        init cls profile and its rating
        :param profile: Must be a Profile as a dictionary
        """
        self.cls_profile = profile
        self.rating = self.cls_profile["rating"]

    def gen_muehvec(self, cls):
        muehvec = []
        for feature in sorted(self.cls_profile[str(cls)].keys()):
            if feature is not "covariancematrice" and feature is not "prior":
                muehvec.append(self.cls_profile[str(cls)][feature][0])
        return muehvec

    def cls_likelihood_multivariant(self, cls, valuevec):
        valuevec = numpy.array([value for value in valuevec.values()])
        mueh = numpy.array(self.gen_muehvec(cls))
        matrice = self.cls_profile[str(cls)]["covariancematrice"]
        if numpy.linalg.det(matrice) == 0:
            return
        return gauss_multivariant(valuevec, mueh, matrice)

    @staticmethod
    def feature_likelihood(value, mueh, nd, factor=1.0, factors=False):
        likelihood = gauss(value, mueh, nd)
        return factor * likelihood if factors else likelihood

    def cls_likelihood(self, cls, valuevec, usedvalues, factors):
        likelyhood = 1.0
        for featurename in self.cls_profile[str(cls)].keys():
            if featurename not in usedvalues:
                continue
            singlelikelyhood = self.feature_likelihood(valuevec[featurename], *self.cls_profile[str(cls)][featurename],
                                                       factors)
            likelyhood *= singlelikelyhood
        return likelyhood

    def evidence(self, prior, valuevec, usedvalues, multivariant, factors):
        """Evidence for one specific class"""
        evidence = 0
        for cls in self.rating:
            if multivariant:
                evidence += prior * self.cls_likelihood_multivariant(cls, valuevec)
            else:
                evidence += prior * self.cls_likelihood(cls, valuevec, usedvalues, factors)
        return evidence

    def posterior(self, cls, valuevec, usedvalues, factors, multivariant=False):
        """Gen the Posterior for one specific class"""
        if multivariant:
            lh = self.cls_likelihood_multivariant(cls, valuevec)
        else:
            lh = self.cls_likelihood(cls, valuevec, usedvalues, factors)
        prior = self.cls_profile[str(cls)]["prior"]
        evidence = self.evidence(prior, valuevec, usedvalues, multivariant, factors)
        return lh * prior / evidence

    def classify(self, valuevec, usedvalues="", multivariant=False, factors=False):
        posterior_ergs = []
        if not usedvalues:
            usedvalues = [item for item in valuevec.keys()]
        for cls in self.rating:
            posterior_ergs.append((cls, self.posterior(cls, valuevec, usedvalues, factors, multivariant)))
        most_common_class = max(posterior_ergs, key=itemgetter(1))[0]
        return most_common_class

    def set_profile(self, new_profile):
        self.cls_profile = new_profile.get_profile()


if __name__ == "__main__":
    import ML.profile as PRF
    import ML.Validation as VAL
    with open("trainingsets/pickleddicts/kaggle_600_newfeat.pkl", "rb") as dumbfile:
        dict_list = pickle.load(dumbfile)
    result = 0
    valsetlen = 0
    for i in range(100):
        tsets, valsets = personal_list(dict_list, 0.6, 2, range(1, 7, 1), occurekey="grade")
        # Profil erstellen
        myProfile = PRF.Profile("Test", tsets, dict_list)
        newprofile, ergs = VAL.validation(myProfile, valsets)
        print(myProfile.get_profile())
        print(list(dict_list[0]["features"].keys()))
        # Validation
        try:
            MyClassifier = Classifier(newprofile.get_profile())
            for valset in valsets:
                valsetlen += 1
                vec = valset["features"]
                grade = valset["grade"]
                Note = MyClassifier.classify(vec, multivariant=False, factors=True)
                print("Note: {}".format(Note))
                print("Korrektor Note: {}".format(grade))
                if Note == grade:
                    result += 1
        except:
            valsetlen -= 1
            continue
    print("The Classifier classified {} percent correct".format(result / valsetlen * 100))
