#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""main.py: This is the main program."""

__author__ = "Raphael Kreft"
__email__ = "kreft@phaenovum.de"
__version__ = "0.0.1 alpha"
__status__ = "dev"

from math import sqrt
import pickle
import datetime
import os
import itertools
from ML.vectors_matrix import *


class Profile(object):
    """
    The feature vectors : {"grade":3, "features": {"f1": x1,"f2":x2,"f3":x3}}
    self.values: {1:{f1:[]},2:{f1:[]}} -> for every class there is a dict of featurevalues
    self.profile: {1:{"prior": 123, "covariancematrix": matr, "featurename": [mueh, standartdeviation, factor]}}
    self.histogram: the occurence of a class to determine the Prior
    """
    def __init__(self, name, valvecs, gesset):
        # getting rating range
        rating = list(set([valvec['grade'] for valvec in valvecs]))
        # Rating which is used in Traininsets
        self.rating = rating
        # Profile we want to build
        self.profile = {}
        self.profile.update({"rating": self.rating})
        self.histogram = {}
        # The Trainingsets
        self.givenvecs = valvecs
        self.values = {}
        self.profilename = name
        # Setup dicts and lists to insert values, learning-data and occurences
        for i in self.rating:
            self.histogram[str(i)] = 0
            self.profile[str(i)] = {}
            self.values[str(i)] = {}
            for key in self.givenvecs[0]["features"].keys():
                self.values[str(i)].update({key: []})
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
        #print(self.values)
        #self.values = self.uglyfunction_butworks(self.values)
        # Learning
        self.gen_contents()
        # Save Profile
        self.dump_profile()

    def add_values(self):
        """
        Add the content of the given Featurevectors to self.values
        """
        for valuevec in self.givenvecs:
            for key, val in valuevec["features"].items():
                self.values[str(valuevec["grade"])][str(key)].append(val)

    def make_histogram(self, sets):
        for s in sets:
            self.histogram[str(s["grade"])] += 1

    def get_specific_values(self, mark, featurename=""):
        """
        Get specific Values from self.values. You can get values for specific classes and
        for a specific feature in a specific class
        :param mark: The class whoms values you want to get
        :param featurename: optional featurename to get values for a specific feature in a class
        :return: Wanted Values
        """
        if featurename is "":
            return self.values[str(mark)]
        else:
            return sorted(self.values[str(mark)][featurename])

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
        return self.histogram[str(mark)]

    def make_matrix(self, featlist, entryfn, cls):
        """
        Build a Matrice
        :param featlist: A List of features we going through to get the amounts x, y
        :param entryfn: The entryfunction that builds the entries in the Matrix
        :param cls: The class whoms Covariancematrix we want to build
        :return:
        """
        return [[entryfn(self.get_specific_values(cls, i), self.get_specific_values(cls, j)) for j in featlist] for i in featlist]

    def covariancematrice(self, cls):
        """
        Function should build a Covariancematrix from a given classname
        :param cls: The Class whoms Matrice we want to build
        :return: The Covariancematrix
        """
        matrice = self.make_matrix(sorted(self.get_specific_values(cls).keys()), correlation, cls)
        if numpy.linalg.det(matrice) == 0:
            #print("No Valid cov-matrice for {}".format(cls))
            pass
        return numpy.matrix(matrice)

    def gen_contents(self):
        """
        This fuction extract the knowledge from all given values. For every class there is a prior a
        covariancematrix and [mueh, standartdeviation] for every feature in every class
        """
        normaldistribution = lambda mueh, values: sqrt(sum([(value - mueh) ** 2 for value in values]) / (len(values) - 1))
        mueh = lambda values: sum(values) / len(values)
        prior = lambda cls_occurence, gen_occurence: cls_occurence / gen_occurence
        for cls in self.rating:
            pr = prior(self.get_histogram(cls), sum([self.get_histogram(c) for c in self.rating]))
            self.profile[str(cls)] = {"prior": pr}
            self.profile[str(cls)].update({"covariancematrice": self.covariancematrice(cls)})
            for feature in self.get_specific_values(cls).keys():
                mh = mueh(self.get_specific_values(cls, feature))
                nd = normaldistribution(mh, self.get_specific_values(cls, feature))
                if nd == 0:
                    raise ZeroDivisionError
                self.profile[str(cls)][feature] = [mh, nd, None]

    def save_factors(self):
        with open("factors.dat", "w") as f:
            print(self.profile)
            features = list(self.profile[str(self.rating[0])].keys())
            f.write("# Num of Features: " + str(len(features)) + "\n")
            f.write("# Date: " + str(datetime.datetime.now()) + "\n")
            for feature in features:
                if feature in ["covariancematrice", "prior"]:
                    continue
                featurevals = []
                for cls in self.rating:
                    featurevals.append(self.profile[str(cls)][feature][2])
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
        nicestring = "\033[94mProfile:\n\n"
        for num, item in enumerate(self.profile.items()):
            nicestring += "{}:  {}\n".format(num + 1, item)
        return nicestring


def combis(l):
    length = len(l)
    combinelist = []
    for i in range(length +1):
        for templist in itertools.combinations(l, i):
            if templist:
                combinelist.append(list(templist))
    return combinelist

if __name__ == "__main__":
    # Test des Trainings
    dict_list = [{'grade': 1, 'features': {'alpha': 43, 'beta': 39, 'delta': 89, 'gamma': 5, 'eta': 50}},
                 {'grade': 1, 'features': {'alpha': 49, 'beta': 48, 'delta': 95, 'gamma': 11, 'eta': 59}},
                 {'grade': 2, 'features': {'alpha': 43, 'beta': 33, 'delta': 120, 'gamma': 13, 'eta': 44}},
                 {'grade': 2, 'features': {'alpha': 55, 'beta': 15, 'delta': 110, 'gamma': 0, 'eta': 120}},
                 {'grade': 2, 'features': {'alpha': 44, 'beta': 34, 'delta': 121, 'gamma': 14, 'eta': 45}},
                 {'grade': 2, 'features': {'alpha': 56, 'beta': 16, 'delta': 111, 'gamma': 1, 'eta': 121}},
                 {'grade': 3, 'features': {'alpha': 33, 'beta': 44, 'delta': 56, 'gamma': 7, 'eta': 22}},
                 {'grade': 3, 'features': {'alpha': 39, 'beta': 49, 'delta': 61, 'gamma': 10, 'eta': 27}},
                 {'grade': 4, 'features': {'alpha': 12, 'beta': 50, 'delta': 80, 'gamma': 6, 'eta': 20}},
                 {'grade': 4, 'features': {'alpha': 55, 'beta': 35, 'delta': 70, 'gamma': 11, 'eta': 27}},
                 {'grade': 5, 'features': {'alpha': 16, 'beta': 25, 'delta': 103, 'gamma': 1, 'eta': 19}},
                 {'grade': 5, 'features': {'alpha': 20, 'beta': 30, 'delta': 110, 'gamma': 4, 'eta': 25}},
                 {'grade': 6, 'features': {'alpha': 14, 'beta': 27, 'delta': 120, 'gamma': 0, 'eta': 12}},
                 {'grade': 6, 'features': {'alpha': 20, 'beta': 33, 'delta': 100, 'gamma': 4, 'eta': 18}}]
    print("Make Profile object")
    myProfile = Profile("Test", dict_list, dict_list)
    print(len(combis(myProfile.get_profile()["1"].keys())))
    print("Done!")
    print(myProfile)
