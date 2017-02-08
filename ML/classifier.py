#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""classifier.py:	This file is Part of the maTex-Project. It contains the Classifier Class which is very important"""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Raphael Kreft"
__version__ = "Development v0.05"
__email__ = "raphaelkreft@gmx.de"
__status__ = "Dev"

from operator import itemgetter
import utils.textinit


class Classifier(object):
    """
    The Classifier classifies values after building the classifier out of a Profile

    Init the Classifier with the profile you want to classify with and
    Use the classify method to classify a given valuevector...
    """
    def __init__(self, profile, exclude=None):
        """
        pass some class variables
        :param profile: Must be a Profile as a dictionary
        """
        if exclude is None:
            exclude = []
        self.cls_profile = profile
        self.rating = self.cls_profile["rating"]
        self.exclude = exclude

    def muehvec(self, cls):
        muehvec = []
        for feature in sorted(self.cls_profile[cls].keys()):
            if feature is not "covariancematrice" and feature is not "prior":
                muehvec.append(self.cls_profile[cls][feature][0])
        return muehvec

    def cls_likelihood_multivariant(self, cls, valuevec):
        valuevec = utils.textinit.numpy.array([value for value in valuevec.values()])
        mueh = utils.textinit.numpy.array(self.muehvec(cls))
        matrice = self.cls_profile[cls]["covariancematrice"]
        if utils.textinit.numpy.linalg.det(matrice) == 0:
            return
        return utils.textinit.gauss_multivariant(valuevec, mueh, matrice)

    @staticmethod
    def feature_likelihood(value, mueh, nd, factor=1.0, factors=False):
        likelihood = utils.textinit.gauss(value, mueh, nd)
        return factor * likelihood if factors else likelihood

    def cls_likelihood(self, cls, valuevec, usedvalues, factors):
        likelyhood = 1.0
        for featurename in self.cls_profile[cls].keys():
            if featurename not in usedvalues or featurename in self.exclude:
                continue
            singlelikelyhood = self.feature_likelihood(valuevec[featurename], *self.cls_profile[cls][featurename],
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
        prior = self.cls_profile[cls]["prior"]
        evidence = self.evidence(prior, valuevec, usedvalues, multivariant, factors)
        return lh * prior / evidence

    def classify(self, valuevec, usedvalues="", multivariant=False, factors=False):
        posterior_ergs = []
        if not usedvalues:
            usedvalues = [item for item in valuevec.keys()]
        for cls in self.rating:
            posterior_ergs.append((cls, self.posterior(cls, valuevec, usedvalues, factors, multivariant)))
        most_common_class = max(posterior_ergs, key=itemgetter(1))
        cls = most_common_class[0]
        evidence = (1 - most_common_class[1])*100
        return cls, evidence

    def set_profile(self, new_profile):
        self.cls_profile = new_profile.get_profile()

