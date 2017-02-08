#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""main.py: This is the main program."""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Raphael Kreft"
__email__ = "kreft@phaenovum.de"
__version__ = "0.0.1 alpha"
__status__ = "dev"


import pickle
import datetime
import os
import numpy
import collections

from ML.vectors_matrix import *


class Profile(object):
    """
    The feature vectors : {"grade":3, "features": {"f1": x1,"f2":x2,"f3":x3}}
    self.values: {1:{f1:[]},2:{f1:[]}} -> for every class there is a dict of featurevalues
    self.profile: {1:{"prior": 123, "covariancematrix": matr, "featurename": [mueh, standartdeviation, factor]}}
    self.histogram: the occurence of a class to determine the Prior
    """

    def __init__(self, name, valvecs, gesset, excludefeatures=None):
        # Rating which is used in Traininsets
        if excludefeatures is None:
            excludefeatures = []
        self.rating = list(set([valvec['grade'] for valvec in gesset]))
        # Profile we want to build
        self.profile = {}
        self.profile.update({"rating": self.rating, "toexclude": excludefeatures})
        self.histogram = {}
        # The Trainingsets
        self.givenvecs = valvecs
        self.values = {}
        self.profilename = name
        # Setup dicts and lists to insert values, learning-data and occurences
        for i in self.rating:
            self.histogram[i] = 0
            self.profile[i] = {}
            self.values[i] = {}
            for key in self.givenvecs[0]["features"].keys():
                self.values[i].update({key: []})
        # Make and save Profile
        self.make_histogram(gesset)
        self.run()

    def run(self):
        """
        To be executed to make an Profile automated
        :return:
        """
        # Adding Values
        self.add_values()
        self.feature_treatability()
        # Learning
        self.gen_contents()
        # Save Profile
        #self.dump_profile()

    def feature_treatability(self):
        for feature in self.get_specific_values(self.rating[0]).keys():
            if feature in self.get_profile()["toexclude"]:
                continue
            values = collections.defaultdict(list)
            for cls in self.rating:
                values[cls].extend(self.values[cls][feature])
            if any([standartdeviation(values[cls]) == 0 for cls in self.rating]):
                raise ZeroDivisionError
            else:
                continue

    def add_values(self):
        """
        Add the content of the given Featurevectors to self.values
        """
        for valuevec in self.givenvecs:
            for key, val in valuevec["features"].items():
                self.values[valuevec["grade"]][key].append(val)

    def make_histogram(self, sets):
        for s in sets:
            self.histogram[s["grade"]] += 1

    def get_specific_values(self, mark, featurename=""):
        """
        Get specific Values from self.values. You can get values for specific classes and
        for a specific feature in a specific class
        :param mark: The class whoms values you want to get
        :param featurename: optional featurename to get values for a specific feature in a class
        :return: Wanted Values
        """
        if featurename is "":
            return self.values[mark]
        else:
            return sorted(self.values[mark][featurename])

    def get_profile(self):
        return self.profile

    def insert(self, key, value):
        self.profile[key] = value

    def insert_list(self, ls):
        for key, value in ls:
            self.insert(key, value)

    def set_profile(self, new_profile):
        self.profile = new_profile

    def get_histogram(self, mark):
        return self.histogram[mark]

    def make_matrix(self, featlist, entryfn, cls):
        """
        Build a Matrice
        :param featlist: A List of features we going through to get the amounts x, y
        :param entryfn: The entryfunction that builds the entries in the Matrix
        :param cls: The class whoms Covariancematrix we want to build
        :return:
        """
        return [[entryfn(self.get_specific_values(cls, i), self.get_specific_values(cls, j)) for j in featlist] for i in
                featlist]

    def covariancematrice(self, cls):
        """
        Function should build a Covariancematrix from a given classname
        :param cls: The Class whoms Matrice we want to build
        :return: The Covariancematrix
        """
        matrice = self.make_matrix(sorted(self.get_specific_values(cls).keys()), correlation, cls)
        if numpy.linalg.det(matrice) == 0:
            # print("No Valid cov-matrice for {}".format(cls))
            pass
        return numpy.matrix(matrice)

    def gen_contents(self):
        """
        This fuction extract the knowledge from all given values. For every class there is a prior a
        covariancematrix and [mueh, standartdeviation] for every feature in every class
        """
        normaldistribution = lambda mueh, values: math.sqrt(
            sum([(value - mueh) ** 2 for value in values]) / (len(values) - 1))
        mueh = lambda values: sum(values) / len(values)
        prior = lambda cls_occurence, gen_occurence: cls_occurence / gen_occurence
        for cls in self.rating:
            pr = prior(self.get_histogram(cls), sum([self.get_histogram(c) for c in self.rating]))
            self.profile[cls] = {"prior": pr}
            self.profile[cls].update({"covariancematrice": self.covariancematrice(cls)})
            for feature in self.get_specific_values(cls).keys():
                mh = mueh(self.get_specific_values(cls, feature))
                nd = normaldistribution(mh, self.get_specific_values(cls, feature))
                self.profile[cls][feature] = [mh, nd, None]

    def save_factors(self):
        with open("factors.dat", "w") as f:
            features = list(self.profile[self.rating[0]].keys())
            f.write("# Num of Features: " + str(len(features)) + "\n")
            f.write("# Date: " + str(datetime.datetime.now()) + "\n")
            for feature in features:
                if feature in ["covariancematrice", "prior"]:
                    continue
                featurevals = []
                for cls in self.rating:
                    featurevals.append(self.profile[cls][feature][2])
                f.write("Feature: {}\nAccuracy: {}\n".format(feature, mean(featurevals)))
            f.close()

    def dump_profile(self):
        """
        Save the profile which is saved in self.profile
        :return:
        """
        with open("{}.pkl".format(os.getcwd() + "/ML/profiles/" + self.profilename), "wb") as dumbfile:
            pickle.dump(self.profile, dumbfile, pickle.HIGHEST_PROTOCOL)

    def __repr__(self):
        return self.profilename

    def __str__(self):
        nicestring = "\033[94mProfile:\n\nFeatures:\t{}\nBestfeatures:\t{}\nAccuracies:\t{}".format(self.get_profile().keys(), self.get_profile()["best-features"], self.get_profile()["Accuracies(n,c,b,bf)"])
        return nicestring
