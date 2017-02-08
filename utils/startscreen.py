#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""startscreen.py: This util prints the start screen of our console program"""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Nikodem Kernbach, Raphael Kreft"
__email__ = "kernbach@phaenovum.de, kreft@phaenovum.de"
__status__ = "final"


def startscreen():
    return "                   ______         \n" \
        "   ____ ___  ____ /_  __/__  _  __\n" \
        "  / __ `__ \/ __ `// / / _ \| |/_/\n" \
        " / / / / / / /_/ // / /  __/>  <  \n" \
        "/_/ /_/ /_/\__,_//_/  \___/_/|_|  \n\n" \
    "maTex - Automated essay grading software\n" \
    "Copyright (C) 2017  The maTex Authors.  All rights reserved.\n\n" \
    "This program comes with ABSOLUTELY NO WARRANTY!\n" \
    "This is free software, and you are welcome to redistribute it\n" \
    "under certain conditions. It is licensed with GNU AGPLv3.\n" \
    "Please refer to <http://www.gnu.org/licenses/> or 'LICENSE'\n" \
    "file to find the license.\n"

if __name__ == '__main__':
    print(startscreen())

