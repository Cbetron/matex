#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""main.py: This is the main program."""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Raphael Kreft"
__email__ = "kreft@phaenovum.de"
__version__ = "1.2 stable"
__status__ = "dev"

import argparse
import datetime
import os
import pickle
import sys

from ML import profile, classifier, validation
from textfeatures.manager import *
from utils import startscreen
from UI.website import *


def parse_arguments():
    """
    Parsing Arguments given to the program. Build and setup the Parser
    :return: -
    """
    # Parser erstellen
    arg_parser = argparse.ArgumentParser(prog="Project Gandalf", description="Process the Run-Options for %(prog)",
                                         formatter_class=argparse.RawDescriptionHelpFormatter,
                                         usage="%(prog) [options]",
                                         epilog="For More Information look at the Readme!")
    # Argumente Hinzufügen
    arg_parser.add_argument("-log", default=False, action='store_true', help="Give this Argument to activate logging")
    arg_parser.add_argument("-gui", action='store_true', help="give this Argument to use the Graphical-Userinterface")
    args = arg_parser.parse_args()
    return args


def execute(path):
    with open(path) as f:
        code = compile(f.read(), path, 'exec')
        exec(code, globals())


def run_magic_web(text, profile, method=None, usefeatures=None):
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
    MyManager = Manager()
    # Build Classifier
    MyClassifier = classifier.Classifier(prof)
    MyManager.set_text(text)
    if bestfeatures:
        usefeatures = prof["best-features"]
    Grade, evidence = MyClassifier.classify(MyManager.run(), factors=factors, multivariant=multivariant,
                                            usedvalues=usefeatures)
    print("Finished!")
    return Grade, evidence


if __name__ == "__main__":
    try:
        arguments = parse_arguments()
    except ValueError:
        print("Missing argument [-runmode]....")
        sys.exit(1)
    if arguments.log:
        log = open("{:%Y-%m-%d_%H:%M:%S}".format(datetime.datetime.now()) + ".log", 'a')
        sys.stdout = log
    if arguments.gui:
        """
        Starting Graphical-Userinterface Mode
        """
        url = 'http://127.0.0.1:5000'
        webbrowser.open_new(url)
        app.run()
    elif not arguments.gui:
        """
        Starting Shell-Mode
        """
        print(startscreen.startscreen())
        while True:
            command = input("maTex >>> ").lower()
            if command == "run":
                """The Run Mode"""
                execute("./Scripts/run.py")
            elif command == "training":
                """The Training Mode"""
                execute("./Scripts/training.py")
            elif command == "validation":
                """Validate a Dataset"""
                execute("./Scripts/validation_dataset.py")
            elif command == "script":
                src = "./Scripts/{}".format(input("scriptname: "))
                execute(src)
            elif command == "profileinfo":
                profilepath = "{}/ML/profiles/{}".format(os.getcwd(), input("Welches Profil?: "))
                try:
                    with open(profilepath, "rb") as f:
                        prof = pickle.load(f)
                        print(prof)
                except FileNotFoundError:
                    print("file {} not found!".format(profilepath))
                except KeyError as err:
                    print(err)
            elif command == "help":
                print("run\tcorrect your text\ntraining\tMake a Profile\nprofileinfo\tget some Information of your "
                      "Profile\nexit\texit maTex")
            elif command == "exit":
                sys.exit(0)
            else:
                print("{}   is no command...".format(command))
