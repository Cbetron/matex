#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""main.py: This is the main program."""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Raphael Kreft"
__email__ = "kreft@phaenovum.de"
__status__ = "dev"

import os
import argparse
import datetime
import sys
import pickle
import contextlib
import statistics
from textfeatures.manager import *
from textfeatures.modules.textfeature import Textfeature
from utils import textinit, pdfcreator, startscreen
from ML import profile, Classifier, Validation



def parse_arguments():
    """
    Parsing Arguments given to the program. Build and setup the Parser
    :return: -
    """
    # Parser erstellen
    parser = argparse.ArgumentParser(prog="Project Gandalf", description="Process the Run-Options for %(prog)",
                                     formatter_class=argparse.RawDescriptionHelpFormatter, usage="%(prog) [options]",
                                     epilog="For More Information look at the Readme!")
    # Argumente Hinzufügen
    parser.add_argument("-log", default=False, action='store_true', help="Give this Argument to activate logging")
    parser.add_argument("-GUI", action='store_true', help="give this Argument to use the Graphical-Userinterface")
    parser.add_argument("-hexhex", action='store_true', default=False, help="Special feature")
    args = parser.parse_args()
    return args


def training(profilename, tset_path):
    print("Start Training!")
    # Trainingset extraktion
    if tset_path.endswith(".pkl"):
        with open(tset_path, "rb")as f:
            trainingsets = pickle.load(f)
    elif os.path.isdir(tset_path):
        TF_Manager = Manager()
        trainingsets = []
        for file in os.listdir(tset_path):
            TF_Manager.set_text(textinit.get_raw_text(tset_path + file))
            trainingsets.append(TF_Manager.run())
    else:
        print("{} could not be used for training")
        return
    # Profilerstellung
    print("Make Profile!")
    rating = list(set([valvec["grade"] for valvec in trainingsets]))
    print(rating)
    while True:
        try:
            tset, valset = textinit.personal_list_split(trainingsets, 0.6, 3, rating, occurekey="grade")
            myprofile = profile.Profile(profilename, tset, trainingsets)
            break
        except ZeroDivisionError as err:
            print("Zero Division Error!\n{}".format(err))
            continue
        except ValueError as err:
            print("Value Error!\n{}".format(err))
            continue
    # Validation
    print("Validation!")
    results = []
    feature_accuracies = {}
    for feature in list(valset[0]["features"].keys()):
        feature_accuracies[feature] = []
    for i in range(100):
        print("{}. Test from {}".format(i, 100))
        while True:
            try:
                tset, valset = textinit.personal_list_split(trainingsets, 0.6, 3, rating, occurekey="grade")
                myprofile = profile.Profile(profilename, tset, trainingsets)
                new_profile, ergs = Validation.validation(myprofile, valset)
                for feature in list(valset[0]["features"].keys()):
                    feature_accuracies[feature].append(Validation.feature_accuracy(feature, valset, myprofile.get_profile())[1])
                break
            except ZeroDivisionError:
                continue
            except ValueError:
                continue
        results.append(ergs)
    acc_n, var_n = statistics.mean([ergs[0][0] for ergs in results]), statistics.mean([ergs[0][1] for ergs in results])
    acc_c, var_c = statistics.mean([ergs[1][0] for ergs in results]), statistics.mean([ergs[1][1] for ergs in results])
    acc_b, var_b = statistics.mean([ergs[2][0] for ergs in results]), statistics.mean([ergs[2][1] for ergs in results])
    # Safe Profile
    print("Safe results in Profile and Resultfile!")
    new_profile, ergs = Validation.validation(myprofile, valset)
    new_profile.insert_list([("Accuracy_n", acc_n), ("Accuracy_c", acc_c), ("Accuracy_b", acc_b), ("Variance_n", var_n), ("Variance_c", var_c), ("Variance_b", var_b)])
    # Write Results to file
    f = open("trainingresults.txt", "w")
    f.write("Feature Accuracy for your Trainingsets:\n\n")
    for feature in list(valset[0]["features"].keys()):
        erg = statistics.mean(feature_accuracies[feature])
        f.write("{}:\t{}\n".format(feature, erg))
    f.write("\n\nProfiles with your trainingsets got an average Accuracy and Variance of:\n")
    f.write("Naive Bayes Normal: {}, {}\n".format(acc_n, var_n))
    f.write("Naive Bayes Faktoren: {}, {}\n".format(acc_c, var_c))
    f.write("Naive Bayes Best Features: {}, {}\n".format(acc_b, var_b))
    f.close()
    new_profile.dump_profile()


def run_magic(text, profile, factors=True, bestfeatures=True, multivariant=False):
    """
    Hauptfunktion zur Korrektur von Texten. Für jede Datei wird die Korrektur durchgeführt.
    Diese Funktion enthält die Korrekturfunktion
    :param path: Der Pfad zu der/den Dateien/Dokumenten, die Korrigiert werden sollen
    :param filenames: Die Namen der Dateien, die korrigiert werden sollen
    :return: -
    """
    with open('ML/profiles/'+profile+'.pkl', 'rb') as profilefile:
        profile = pickle.load(profilefile)
    pdf = PDF('name', 'name'+'.pdf')
    MyManager = Manager(pdf=pdf)
    # Build Classifier
    MyClassifier = Classifier.Classifier(profile)
    # pdf.insert_info("New Text!")
    MyManager.set_text(text)
    if bestfeatures:
        bestfeatures = profile["best-features"]
    Grade = MyClassifier.classify(MyManager.run(), factors=factors, multivariant=multivariant, usedvalues=bestfeatures)
    # pdf.insert_grade(Grade)
    # pdf.save_pdf()
    evidence = 'Not available yet!'
    print("Finished!")
    return Grade, evidence


def hexhex():
    """
    The Special_Feature of our Program
    :return: -
    """
    print("HexHex... Your Pc will shutdown now!")
    os.system("shutdown -t now")


if __name__ == "__main__":
    try:
        arguments = parse_arguments()
    except ValueError:
        print("Missing argument [-runmode]....")
        sys.exit(1)
    if arguments.hexhex:
        hexhex()
    if arguments.log:
        log = open("{:%Y-%m-%d_%H:%M:%S}".format(datetime.datetime.now()) + ".log", 'a')
        sys.stdout = log
    if arguments.GUI:
        """
        Starting Graphical-Userinterface Mode
        """
        pass

    elif not arguments.GUI:
        """
        Starting Shell-Mode
        """
        print(startscreen.startscreen())
        while True:
            command = input("maTex >>> ")
            if command == "run":
                """The Run Mode"""
                filepath = input("path to File: ")
                run_magic(filepath, input("Profile you want to use: "))
            elif command == "training":
                """The Training Mode"""
                profilename = input("Type in a Profilename for the new Profile: ")
                tset_path = str(os.getcwd() + input("Path to Trainingsets: "))
                training(profilename, tset_path)
            elif command == "exit":
                sys.exit(0)
            else:
                print("{}   is no command...".format(command))
