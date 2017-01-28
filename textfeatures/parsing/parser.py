# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""parser.py: This util contains functions that classify words with tensorflow syntaxnet and parsey mcParseface."""

__author__ = "Nikodem Kernbach"
__email__ = "kernbach@phaenovum.de"
__status__ = "dev"

import sys
import os
import utils.textinit as TI
import textfeatures.databases.manage as DB
import re

PARSING_FOLDER_PATH = 'textfeatures/parsing/'
INPUT_TEXT_PATH = PARSING_FOLDER_PATH+'input.tmp'
OUTPUT_CONLL_PATH = PARSING_FOLDER_PATH+'output.tmp'
POS_MAP_PATH = PARSING_FOLDER_PATH+'pos-to-speech.map'
TAG_MAP_PATH = PARSING_FOLDER_PATH+'tag-to-speech.map'
RELATION_MAP_PATH = PARSING_FOLDER_PATH+'relation-to-speech.map'
SYNTAXNET_PATH = PARSING_FOLDER_PATH+'models/syntaxnet/'
EXECUTING_PARSING_FILE_PATH = SYNTAXNET_PATH+'syntaxnet/gandalf_parse.sh'
CONTEXT_PBTXT_FILE_PATH = SYNTAXNET_PATH+'syntaxnet/models/parsey_mcparseface/context.pbtxt'
SETUP_PATH = PARSING_FOLDER_PATH+'setup/'
SETUP_FILE_PATH = SETUP_PATH+'setup_important.conf'
EXEC_SETUP_FILE_PATH = SETUP_PATH+'gandalf_parse.conf'


def setup_parser():
    # THIS SHOULD BE RUNNED ONLY ONCE ON EVERY NEW COMPUTER USING THE PROGRAM!
    setup_file = open(SETUP_FILE_PATH, 'r')
    setup = setup_file.read()
    setup_list = setup.split('\n\n')
    setup_string = setup_list[0]+"'"+os.getcwd()+'/'+INPUT_TEXT_PATH+"'\n"+setup_list[1]
    print(setup_string)
    parser_context_file = open(CONTEXT_PBTXT_FILE_PATH, 'a')
    parser_context_file.write(setup_string)
    setup_file.close()
    parser_context_file.close()
    exec_setup_file = open(EXEC_SETUP_FILE_PATH, 'r')
    content = exec_setup_file.read()
    exec_file = open(EXECUTING_PARSING_FILE_PATH, 'w')
    exec_file.write(content)
    exec_file.close()
    exec_setup_file.close()
    os.system("uxterm -e \"chmod +x " + SYNTAXNET_PATH + "syntaxnet/gandalf_parse.sh\"")


def parse(text):
    input_text = TI.get_sentence_generator(text)
    input_text_file = open(INPUT_TEXT_PATH, 'w')
    for sentence in input_text:
        input_text_file.write(sentence)
    input_text_file.close()

    output_conll_file = open(OUTPUT_CONLL_PATH, 'w')
    output_conll_file.close()
    cwd = os.getcwd()
    os.chdir(SYNTAXNET_PATH)
    current_os = sys.platform
    if current_os == 'linux':
        os.system("uxterm -e \"syntaxnet/gandalf_parse.sh >> ../../" + os.path.basename(OUTPUT_CONLL_PATH) + "\"")
    elif current_os == 'win32':
        print("Windows isn't supported by the parser module yet! QUITTING...")
        #sys.exit()
    elif current_os == 'darwin':
        print("OSX isn't supported by the parser module yet! QUITTING...")
        sys.exit()
    else:
        print("Your OS isn't supported! QUITTING...")
        sys.exit()
    os.chdir(cwd)

    try:
        os.remove(DB.DATABASES_PATH+DB.ParsingData_DATABASE_NAME+'.db')
    except Exception:
        print("Old database does not exist or could not remove it!")
    Database = DB.ParsingData()
    Database.create_table()

    output_conll_file = open(OUTPUT_CONLL_PATH, 'r')
    content = output_conll_file.read()
    sentences = content.split('\n\n')
    index = 0
    for sentence in sentences:
        index += 1
        #Database.create_sentence_table(index)
        word_data = sentence.split('\n')
        for word in word_data:
            if not word:
                print("No word data recieved!")
                #Database.delete_sentence_table(index)
            else:
                values = word.split('\t')
                count = int(values[0])
                word = values[1]
                wordtype = values[3]
                wordtag = values[4]
                worddep = int(values[6])
                worddeptype = values[7]
                Database.insert_parsed_word(index, count, word, wordtype, wordtag, worddep, worddeptype)


def translate(word, mode):
    if isinstance(word, str):
        translation_map = None
        if mode == 'pos':
            translation_map = open(POS_MAP_PATH, 'r')
        elif mode == 'tag':
            translation_map = open(TAG_MAP_PATH, 'r')
        elif mode == 'relation':
            translation_map = open(RELATION_MAP_PATH, 'r')
        else:
            print("invalid mode!")
        t_map_data = translation_map.read()
        lines = t_map_data.split('\n')
        for line in lines:
            line = line.split('\t')
            if word == line[0]:
                word = re.sub(r"\b"+line[0]+r"\b", line[1], word)
        translation_map.close()
    else:
        print("Not a string")
    return word


def get_verbinfo():
    Database = DB.ParsingData()
    verbs = Database.get_verbs()
    verbinfo = []
    for verb in verbs:
        verb = list(verb)
        verb[3] = translate(verb[3], 'pos')
        verb[4] = translate(verb[4], 'tag')
        verb[5] = translate(verb[5], 'relation')
        verbinfo.append(verb)
    return verbinfo


def foreign_word(word):
    Database = DB.ParsingData()
    foreign_words = Database.check_word('FW', word)
    if not foreign_words:
        return False
    else:
        return True
