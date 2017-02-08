#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""training.py: This is a standart script to make a training."""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Raphael Kreft"
__email__ = "kreft@phaenovum.de"
__version__ = "0.0.1 alpha"
__status__ = "dev"

import os

from ML import validation, profile
from utils import textinit


def training(pname, trainingset_path, excludefeatures=None):
    if not excludefeatures:
        excludefeatures = ["paragraphs", "paragraph_lenght", 'paragraph_lenght_per_textlenght']
    # Trainingset extraktion
    trainingsets, removedfeatures = textinit.trainingset_extraction(trainingset_path)
    print("removed: {} because of untreatability".format(removedfeatures))
    # Save and validate one profile
    rating = list(set([trainingset["grade"] for trainingset in trainingsets]))
    if input("Rating Range {} correct?: ".format(rating)) is "y":
        pass
    else:
        return
    while True:
         try:
            tset, valset = textinit.personal_list_split(trainingsets, 0.6, 3, rating, occurekey="grade")
            print("try to make Profile....")
            myprofile = profile.Profile(pname, tset, trainingsets, excludefeatures=excludefeatures)
            print("validate and add Factors...")
            newprofile, ergs = validation.profile_validation(myprofile, valset, toexclude=excludefeatures, multitest=10, rating=rating)
            print("Safe Profile...")
            newprofile.dump_profile()
            break
         except ZeroDivisionError:
             continue
         except ValueError:
             continue
    print("Training successful!")


# Read In Parameters
profilename = input("Type in a Profilename for the new Profile: ")
tset_path = os.getcwd() + input("Path to Trainingsets: ")
# Execute Training
training(profilename, tset_path)