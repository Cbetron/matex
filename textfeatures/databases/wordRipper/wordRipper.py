#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""wordRipper.py: Dieses Script/Modul dient zum Downloaden der Wörter für die Lookuplist"""

__author__ = "Raphael Kreft"
__version__ = "0.2.0"
__email__ = "raphaelkreft@gmx.de"
__status__ = "dev"

import string
import sys
import datetime
from webcrawling import link_spider, text_spider
import argparse
import time
import sqlite3


class Database(object):
    def __init__(self, dbname, dbpath):
        self.dbname = dbname
        self.connection = sqlite3.connect(dbpath + self.dbname + '.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE Words (word TEXT PRIMARY KEY, count INTEGER)")
        print(">> connection with database " + self.dbname + " established <<")

    def __del__(self):
        self.commit()
        self.cursor.close()
        self.connection.close()
        print("disconnected from database "+self.dbname+'.db')

    def commit(self):
        """ 
        This function applies the changes to the current database
        """
        self.connection.commit()
        print(">> changes committed <<")

    def insert_word(self, word, besafe=False):
        """
        Insert new word in Database
        """
        # look if the word already exists
        self.cursor.execute("SELECT count FROM words WHERE word = (?)", [word])
        data = self.cursor.fetchall()
        # if word doesnt exists
        if not data:
            if len(word) < 20 and word.isalpha() and (word == word.upper() or word == word.lower() or word == word.capitalize()):
                print("inserting " + word + " into database")
                self.cursor.execute("INSERT INTO words VALUES(?, 0)", [word])
            else:
                print("word is too long or not a word")
        # if word already exists
        else:
            print("counting "+word)
            list = [i[0] for i in data]
            count = list[0]
            count += 1
            self.cursor.execute("UPDATE words SET count = (?) WHERE word = (?)", [count, word])
            if besafe:
                self.commit()


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
    parser.add_argument("-runmode", default="file", choices=["file", "print", "database"], required=True,
                        help="Choose between [file] or [gen] Runmode")
    parser.add_argument("-log", default=False, action='store_true', help="Give this Argument to activate logging")
    # Versuche Argumente zu parsen
    try:
        args = parser.parse_args()
        return args
    except Exception:
        print("No valid Arguments Found")
        sys.exit(1)


def readlinks(filename="links.txt"):
    """
    Liest Links aus einer Datei
    :param: filename: Der Name der Datei, aus der die links gelesen werden sollen
    :return: line: Gibt zeile für Zeile jeden link der Datei Zurrück
    """
    File = open(str(filename), "r")
    links = []
    for line in File.readlines():
        if line.isspace() or line.startswith(""):
            continue
        links.append(line)
    File.close()
    return links


def cleantext(text):
    """
    Entfernt alle Sonderzeichen und Zahlen aus einem String
    :param text: Text, der von Sonderzeichen und Zahlen gereinigt werden soll
    :return:
    """
    cleantxt = ""
    text.replace('.', " ")
    filtertxt = filter((string.ascii_letters + string.whitespace).__contains__, str(text))
    for letter in list(filtertxt):
        cleantxt += str(letter)
    return cleantxt


def main():
    """
    Hauptfunktion, die aufgerufen werden sollte, wenn man dieses script nutzen will. Sammlung von Wörtern und dessen
    Ausgabe als Return oder in eine Datei
    :return:
    """

    def collect_links(stages):
        """
        Diese Funktion sammelt Links aus Webseiten und speichert diese ab
        :return: -
        """
        link_spider(input("Give the Filename to read/write links from/in: "), stages, filtering=True)

    def collect_words():
        """
        Diese Funktion öffnet jeden der Gespeicherten links und extrahiert die einzelnen Wörter und gibt sie als
        Generator zurrück
        :return:
        """
        content = text_spider("links.txt", mode="return")
        if content:
            content = cleantext(str(content))
            words = content.split(" ", maxsplit=-1)
            print("I found\t" + str(len(words)) + "\tWords!")
            for word in words:
                yield word

    while True:
        stages = int(input("How deep should i search?: "))
        if stages >= 1:
            collect_links(stages)
            break
        if stages == 0:
            break
        if stages < 1:
            print("The Number of stages cant be negative or zero!")
            continue
    for word in collect_words():
            yield word


if __name__ == "__main__":

    welcomestring = "\n\n" \
                    "                          ______  _                       \n" \
                    " _      ______  _________/ / __ \(_)___  ____  ___  _____ \n" \
                    "| | /| / / __ \/ ___/ __  / /_/ / / __ \/ __ \/ _ \/ ___/ \n" \
                    "| |/ |/ / /_/ / /  / /_/ / _, _/ / /_/ / /_/ /  __/ /     \n" \
                    "|__/|__/\____/_/   \__,_/_/ |_/_/ .___/ .___/\___/_/      \n" \
                    "                               /_/   /_/                  \n" \
                    "\n\n\t\tDeveloped by " + __author__ + "\n\t\tVersion " + __version__ + "\n\n\n"

    print(welcomestring)
    try:
        tstart = time.clock()
        arguments = parse_arguments()
        if arguments.runmode == "print":
            wordgenerator = main()
            for word in wordgenerator:
                print(word)
        elif arguments.runmode == "file":
            output = open("yourwords_" + str(datetime.date) + ".txt", "w")
            words = main()
            for word in words:
                output.write(str(word) + "\n")
            output.close()
        elif arguments.runmode == "database":
            dbname = str(input("Insert a name for your Database: "))
            dbpath = str(input("A path where your database should be saved: "))
            words = main()
            MyDatabase = Database(dbname, dbpath)
            for word in words:
                MyDatabase.insert_word(word)
            MyDatabase.commit()
        tend = time.clock()
        print("\n\n**************\n\tDone!\n**************\ncomputingtime: {}".format(tend-tstart))
          
    except ValueError as e:
        print("ValueError occured...\nErrormessage:\n\t{}".format(e))
    except KeyboardInterrupt:
        MyDatabase.commit()
        print("\n\tKey Pressed, killed process")
        sys.exit(1)
