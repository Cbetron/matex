#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""main.py: This is the main program."""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Raphael Kreft"
__email__ = "kreft@phaenovum.de"
__version__ = "0.0.1 alpha"
__status__ = "dev"

import pickle
import os

import utils.textinit
import utils.pdfcreator
from ML.classifier import Classifier
from textfeatures.manager import Manager


def run_magic(filepath, profile, method=None, usefeatures=None):
    """
    Main Function to correct a Text. Saves
    :param filepath: Path to the file whose text is corrected
    :param profile: The Profile_Object which is used to classify the text
    :param method: A list of boolean Values, that describes the way of classifying [bestfeatures, factors, multivariant]
    :param usefeatures: The Features that will be used to classify
    :return: -
    """
    with open("{}/ML/profiles/{}.pkl".format(os.getcwd(), profile), "rb") as f:
        prof = pickle.load(f)
    if method is None:
        method = [True, False, False]
    bestfeatures, factors, multivariant = method[0], method[1], method[2]
    pdf = utils.pdfcreator.PDF(input("Outputfile: "), profile.profilename)
    MyManager = Manager(pdf=pdf)
    # Build Classifier
    MyClassifier = Classifier(prof)
    MyManager.set_text(utils.textinit.get_raw_text(filepath))
    if bestfeatures:
        usefeatures = prof.get_profile()["best-features"]
    Grade, evidence = MyClassifier.classify(MyManager.run(), factors=factors, multivariant=multivariant, usedvalues=usefeatures)
    pdf.insert_grade(Grade)
    pdf.save_pdf()
    print("Finished!\nGrade: {}\nEvidence: {}".format(Grade, evidence))


prof = input("Which Profile?: ")
filepath = input("path to File: ")
usefeatures = input("which features(Enter Nothing to use all): ")
run_magic(filepath, prof, usefeatures=usefeatures)