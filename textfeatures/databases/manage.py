#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""manage.py: This file contains all functions that are used to communicate with the sqlite3 databases."""

__author__ = "Nikodem Kernbach"
__email__ = "kernbach@phaenovum.de"
__status__ = "dev"

import sqlite3
import statistics

DATABASES_PATH = "textfeatures/databases/"
LookUpList_DATABASE_NAME = "lookuplist"
ParsingData_DATABASE_NAME = "parsed"


class DataBase(object):
    def __init__(self, dbname):
        self.dbname = dbname
        self.connection = sqlite3.connect(DATABASES_PATH + self.dbname + '.db')
        self.cursor = self.connection.cursor()
        #print("connection with database " + self.dbname + " established")

    def __del__(self):
        self.commit()
        self.cursor.close()
        self.connection.close()
        #print("disconnected from database "+self.dbname+'.db')

    def commit(self):
        """ This function applies the changes to the current database
        """
        self.connection.commit()
        #print("changes committed")


class LookUpList(DataBase):

    def __init__(self):
        super().__init__(LookUpList_DATABASE_NAME)

    def insert_word(self, word):
        """ This function inserts a new word into the 'lookuplist' database
        :param word: The word to be inserted
        The function has an integrated check if the word is really a word
        This function is normally not called from other modules, but used in insert_data(), that's why
        there is no check needed if the program is connected to the right database
        """
        if len(word) < 20 and word.isalpha() and\
                (word == word.upper() or word == word.lower() or word == word.capitalize()):
            print("inserting " + word + " into database")
            self.cursor.execute("INSERT INTO words VALUES(?, 0)", [word])
        else:
            print("word is too long or not a word")

    def update_data(self, word):
        """ This function inserts a new word into the 'lookuplist' database (using insertword())
         or counts the counter one up
         :param word: The word to be inserted or which counter to be increased
        """
        self.cursor.execute("SELECT count FROM words WHERE word = (?)", [word])
        data = self.cursor.fetchall()
        if not data:
            self.insert_word(word)
        else:
            print("counting "+word)
            list = [i[0] for i in data]
            count = list[0]
            count += 1
            self.cursor.execute("UPDATE words SET count = (?) WHERE word = (?)", [count, word])
            self.commit()

    def get_word_count(self, word):
        """ This function returns the count of a given word from the 'lookuplist' database
        :param word: The word to be checked
        :return value: The value of the count
        The function returns nothing if the word isn't in the database
        """
        self.cursor.execute("SELECT count FROM words WHERE word = (?)", [word])
        valuetuple = self.cursor.fetchall()
        value = [i[0] for i in valuetuple]
        if not value:
            pass
        else:
            return value

    def counter_average(self):
        self.cursor.execute("SELECT count FROM words")
        valuetuple = self.cursor.fetchall()
        values = [i[0] for i in valuetuple]
        average = sum(values)/len(values)
        return average

    def insert_abbreviation(self, abbreviation, full_name):
        """ This function writes a set of data (abbreviation and word) into the 'abbreviation' database
        :parameter abbreviation: The abbreviation
                   full_name: The full word
        """
        self.cursor.execute("INSERT INTO abbreviations VALUES(?,?)", [abbreviation, full_name])

    def check_abbreviation(self, abbreviation):
        """ This function checks if the given parameter is an abbreviation and returns the full word
            :parameter abbreviation: The abbreviation to be checked
            :return word: The full word
        """
        self.cursor.execute("SELECT full_name FROM abbreviations WHERE abbreviation = (?)", [abbreviation])
        wordtuple = self.cursor.fetchall()
        word = [i[0] for i in wordtuple]
        if not word:
            pass
        else:
            return word

    def get_abbreviations(self):
        self.cursor.execute("SELECT abbreviation FROM abbreviations")
        abbreviations = self.cursor.fetchall()
        abbreviations = [i[0] for i in abbreviations]
        return abbreviations


class ParsingData(DataBase):

    def __init__(self):
        super().__init__(ParsingData_DATABASE_NAME)

    def create_table(self):
        """ This function creates a table in the 'parsed' database
        :param count: The index and count of the table. Every sentence in a trainingset has its own table
        """
        self.cursor.execute("CREATE TABLE NewText\
                    (sentence INTEGER, count INTEGER, word TEXT, wordtype TEXT, wordtag TEXT, "
                            "worddep INTEGER, worddeptype TEXT, PRIMARY KEY (sentence, count))")

    def insert_parsed_word(self, index, count, word, wordtype, wordtag, worddep, worddeptype):
        """ This function writes a set of data (of a word) into the 'parsed' database
        :parameter index:       The index of the table and the count of the sentence in which the word occures
                   count:       The place of the word in the sentence
                   word:        The word itself
                   wordtype:    The type of the word
                   wordtag:     The tag of the word (after parsing)
                   worddep:     The place of the word in the sentence from which the inserted word is dependent
                   worddeptype: The type of this dependency
        """
        self.cursor.execute("INSERT INTO NewText VALUES(?,?,?,?,?,?,?)",
                            (index, count, word, wordtype, wordtag, worddep, worddeptype))

    def get_sentence_count(self):
        self.cursor.execute("SELECT MAX(sentence) FROM NewText")
        sentences = self.cursor.fetchall()
        count = sentences[0]
        return count

    def check_word(self, wordtag, word):
        self.cursor.execute("SELECT word FROM NewText WHERE wordtag = (?) AND word = (?)", (wordtag, word))
        words = self.cursor.fetchall()
        words = list(words)
        return words

    def get_verbs(self):
        self.cursor.execute("SELECT sentence,count,word,wordtype,wordtag,worddeptype "
                            "FROM NewText WHERE wordtype = 'VERB'")
        verbs = self.cursor.fetchall()
        return verbs

    def get_words_from_database(self, column, tags):
        words = []
        if isinstance(tags, str):
            tags = [tags]
        for tag in tags:
            self.cursor.execute("SELECT word FROM NewText WHERE %s = (?)" % column, [tag])
            words_tuple = self.cursor.fetchall()
            words_list = [i[0] for i in words_tuple]
            words.extend(words_list)
        return words
