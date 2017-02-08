#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""text.py: This module contains functions for editing .txt files."""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Raphael Kreft"
__email__ = "kernbach@phaenovum.de"
__status__ = "rdy"

import logging
import os
import datetime

LOGGING_PATH = "{}/logs/".format(os.getcwd())


class Logger(object):
    def __init__(self, filename="", level=logging.INFO):
        if filename is "":
            filename = "{:%Y-%m-%d_%H:%M:%S}.log".format(datetime.datetime.now())
            f = open(LOGGING_PATH + filename, "w")
            f.close()
        logging.basicConfig(filename=LOGGING_PATH + filename, format='%(asctime)s (levelname)s:%(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p', level=level)

    def log(self, message, level=logging.INFO):
        logging.log(message, level)
        print(message)


if __name__ == "__main__":
    myLogger = Logger()
    myLogger.log("This is a Warning")
