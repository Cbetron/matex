#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""setup.py: Execute this file to Install maTex"""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Nikodem Kernbach"
__email__ = "kernbach@phaenovum.de"
__status__ = "rdy"

import os
import sys

UBUNTU_TOINSTALL = ["swig", "python-pip", "python3-pip", "python2-pip"]
PYTHON_TOINSTALL = [("2", "-U protobuf==3.0.0b2"), ("2", "mock"), ("2", "asciitree"), ("2", "numpy"), ("3", "numpy"),
                    ("3", "textstat"), ("3", "pyenchant"), ("", "asciitree"), ("3", "flask"), ("3", "textract")]


def install(option):
    """Setting up our program"""
    if option == '-installjdk8':
        # Installing Oracje JDK 8 if wished
        install_jdk()
    else:
        print("None or invalid option, continuing...")

    # Installing bazel with supported version
    install_bazel()

    # Install Packages
    print("Installing packages")
    for package in UBUNTU_TOINSTALL:
        os.system("sudo apt-get install {}".format(package))
    for version, package in PYTHON_TOINSTALL:
        os.system("pip{} install {}".format(version, package))

    # build SyntaxNet
    matex_directory = os.getcwd()
    os.chdir("textfeatures/parsing/models/syntaxnet/tensorflow")
    os.system("./configure")
    os.chdir("..")
    os.system("bazel test syntaxnet/... util/utf8/...")
    os.chdir(matex_directory)

    # setting up Parsey McParseface to work with maTex
    import textfeatures.parsing.parser as PRS
    PRS.setup_parser()


def install_jdk():
    print("Installing Oracle JDK 8 as you wished...")
    os.system("sudo apt-get install software-properties-common")
    os.system("sudo add-apt-repository ppa:webupd8team/java && sudo apt-get update && sudo apt-get install oracle-java8-installer")


def install_bazel():
    print("Installing bazel...")
    os.system("echo \"deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8\" | sudo tee /etc/apt/sources.list.d/bazel.list")
    os.system("curl https://bazel.build/bazel-release.pub.gpg | sudo apt-key add -")
    os.system("sudo apt-get update && sudo apt-get install bazel=0.4.3")


if __name__ == "__main__":
    if os.getuid() is 0:
        print("Welcome to maTex!")
    else:
        print("Not Running as root! Make sure to use 'sudo' before command!")
        sys.exit(1)

    try:
        option = sys.argv[1]
    except IndexError:
        option = None

    install(option)
