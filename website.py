#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""website.py:	Diese Datei ist dient des Webinterfaces des Programms maTex"""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Julian Behringer"
__email__ = "julian.b@hringer.de"
__status__ = "dev"

import flask
import random
import time
import webbrowser
import os
import main as MN

PATH = os.getcwd()
x = 1
timestr = time.strftime("%Y%m%d-%H%M%S")
app = flask.Flask(__name__, static_folder=PATH+"/UI/static", template_folder=PATH+"/UI/templates")
mobile_devices = ["iphone", "android"]


@app.route("/contact")
def contact_email():
    return flask.render_template('contact.html')


@app.route("/contact_en")
def contact_email_en():
    return flask.render_template('contact_en.html')


@app.route("/contact_pl")
def contact_email_pl():
    return flask.render_template('contact_pl.html')


@app.route("/about")
def info():
    return flask.render_template('info.html')


@app.route("/about_en")
def info_en():
    return flask.render_template('info_en.html')


@app.route("/about_pl")
def info_pl():
    return flask.render_template('info_pl.html')


@app.route("/contact_submit", methods=['POST'])
def contact_submit():
    global x
    file_contact = "UI/static/files/" + str(x) + "_contactrequest_" + timestr + ".txt"
    x += 1
    file = open(file_contact, "w", encoding="utf-8")
    file.write("Name: " + flask.request.form['NameInputEmail1'] + "\n")
    file.write("E-Mail: " + flask.request.form['exampleInputEmail1'] + "\n")
    file.write("Thema: " + flask.request.form['subjectEmail1'] + "\n")
    file.write("Datum: " + time.asctime(time.localtime(time.time())) + "\n")
    file.write("Text: " + flask.request.form['textEmail1'])
    file.close()
    return flask.render_template('contact_submit.html')


@app.route("/contact_submit_en", methods=['POST'])
def contact_submit_en():
    global x
    file_contact = "UI/static/files/" + str(x) + "_contactrequest_" + timestr + ".txt"
    x += 1
    file = open(file_contact, "w", encoding="utf-8")
    file.write("Name: " + flask.request.form['NameInputEmail1'] + "\n")
    file.write("E-Mail: " + flask.request.form['exampleInputEmail1'] + "\n")
    file.write("Thema: " + flask.request.form['subjectEmail1'] + "\n")
    file.write("Datum: " + time.asctime(time.localtime(time.time())) + "\n")
    file.write("Text: " + flask.request.form['textEmail1'])
    file.close()
    return flask.render_template('contact_submit_en.html')


@app.route("/contact_submit_pl", methods=['POST'])
def contact_submit_pl():
    global x
    file_contact = "UI/static/files/" + str(x) + "_contactrequest_" + timestr + ".txt"
    x += 1
    file = open(file_contact, "w", encoding="utf-8")
    file.write("Name: " + flask.request.form['NameInputEmail1'] + "\n")
    file.write("E-Mail: " + flask.request.form['exampleInputEmail1'] + "\n")
    file.write("Thema: " + flask.request.form['subjectEmail1'] + "\n")
    file.write("Datum: " + time.asctime(time.localtime(time.time())) + "\n")
    file.write("Text: " + flask.request.form['textEmail1'])
    file.close()
    return flask.render_template('contact_submit_pl.html')


@app.route("/")
def index():
    ip = flask.request.remote_addr
    print(ip)
    user_agent = flask.request.user_agent.platform
    for i in mobile_devices:
        if i == user_agent:
            return flask.render_template('index_mobile.html')
    return flask.render_template('index.html')


@app.route("/en")
def index_en():
    ip = flask.request.remote_addr
    print(ip)
    user_agent = flask.request.user_agent.platform
    for i in mobile_devices:
        if i == user_agent:
            return flask.render_template('index_mobile_en.html')
    return flask.render_template('index_en.html')


@app.route("/pl")
def index_pl():
    ip = flask.request.remote_addr
    print(ip)
    user_agent = flask.request.user_agent.platform
    for i in mobile_devices:
        if i == user_agent:
            return flask.render_template('index_mobile_pl.html')
    return flask.render_template('index_pl.html')



@app.route("/download", methods=['POST'])
def files_download():
    file_used = flask.request.form["data2"]
    response = flask.make_response(file_used)
    response.headers["Content-Disposition"] = "attachment; filename=file.txt"
    response.mimetype = 'text/plain'
    return response


@app.route("/grade", methods=['POST'])
def echo():
    try:
        text = flask.request.form['data']
        factors = False
        filtered = False
        profile = 'US8'
        validity = '0%'
        if flask.request.form['Methode'] == "Naive Bayes":
            filtered = False
            if flask.request.form['Profil'] == "Amerika: 8. Klasse (Note: 1-6)":
                profile = "US8_6"
                validity = '52.89%'
            elif flask.request.form['Profil'] == "Amerika: 8. Klasse (Note: 0-15)":
                profile = "US8_16"
                validity = '25.63%'
        elif flask.request.form['Methode'] == "Gefilterte Naive Bayes":
            filtered = True
            if flask.request.form['Profil'] == "Amerika: 8. Klasse (Note: 1-6)":
                profile = "US8_6"
                validity = '61.12%'
            elif flask.request.form['Profil'] == "Amerika: 8. Klasse (Note: 0-15)":
                profile = "US8_16"
                validity = '27.37%'
        text_grade, evidence = MN.run_magic(text, profile, factors=factors, bestfeatures=filtered)
        file_name = "UI/static/files/file_" + timestr + ".txt"
        file = open(file_name, "w", encoding="utf-8")
        file.write("===ANFANG TEXT===" + "\n" + text + "\n" + "===ENDE TEXT===")
        usedtime = time.asctime(time.localtime(time.time()))
        file.write("\n" + "Ihre Note: " + str(text_grade))
        file.write("\n" + "Benutzte Methode: " + flask.request.form['Methode'])
        file.write("\n" + "Benutztes Profil: " + flask.request.form['Profil'])
        file.write("\n" + "Evidence: " + evidence)
        file.write("\n" + "Genauigkeit des Profils: " + validity)
        file.write("\n" + "Datum der Korrektur: " + usedtime)
        file.close()
        file = open(file_name, "r", encoding="utf-8")
        file_used = file.read()
        return flask.render_template('grade.html', text_grade=text_grade, method=flask.request.form['Methode'],
                                     profile=flask.request.form['Profil'], evidence=evidence, validity=validity, file_used=file_used)
    except:
        return flask.render_template('error.html')


@app.route("/grade_en", methods=['POST'])
def echo_en():
    try:
        text = flask.request.form['data']
        factors = False
        filtered = False
        profile = 'US8'
        validity = '0%'
        if flask.request.form['Methode'] == "Naive Bayes":
            filtered = False
            if flask.request.form['Profil'] == "America: 8th Grade (Grades: 1-6)":
                profile = "US8_6"
                validity = '52.89%'
            elif flask.request.form['Profil'] == "America: 8th Grade (Grades: 0-15)":
                profile = "US8_16"
                validity = '25.63%'
        elif flask.request.form['Methode'] == "Filtered Naive Bayes":
            filtered = True
            if flask.request.form['Profil'] == "America: 8th Grade (Grades: 1-6)":
                profile = "US8_6"
                validity = '61.12%'
            elif flask.request.form['Profil'] == "America: 8th Grade (Grades: 0-15)":
                profile = "US8_16"
                validity = '27.37%'
        text_grade, evidence = MN.run_magic(text, profile, factors=factors, bestfeatures=filtered)
        file_name = "UI/static/files/file_" + timestr + ".txt"
        file = open(file_name, "w", encoding="utf-8")
        file.write("===BEGIN TEXT===" + "\n" + text + "\n" + "===END TEXT===")
        usedtime = time.asctime(time.localtime(time.time()))
        file.write("\n" + "Your Grade: " + str(text_grade))
        file.write("\n" + "Used Method: " + flask.request.form['Methode'])
        file.write("\n" + "Used Profile: " + flask.request.form['Profil'])
        file.write("\n" + "Evidence: " + evidence)
        file.write("\n" + "Validity of the Profile: " + validity)
        file.write("\n" + "Date of the Correction: " + usedtime)
        file.close()
        file = open(file_name, "r", encoding="utf-8")
        file_used = file.read()
        return flask.render_template('grade_en.html', text_grade=text_grade, method=flask.request.form['Methode'],
                                     profile=flask.request.form['Profil'], evidence=evidence, validity=validity, file_used=file_used)
    except:
        return flask.render_template('error_en.html')


@app.route("/grade_pl", methods=['POST'])
def echo_pl():
    try:
        text = flask.request.form['data']
        factors = False
        filtered = False
        profile = 'US8'
        validity = '0%'
        if flask.request.form['Methode'] == "Naiwny Bayes":
            filtered = False
            if flask.request.form['Profil'] == "Ameryka: 8. Klasa (Oceny: 1-6)":
                profile = "US8_6"
                validity = '52.89%'
            elif flask.request.form['Profil'] == "Ameryka: 8. Klasa (Oceny: 0-15)":
                profile = "US8_16"
                validity = '25.63%'
        elif flask.request.form['Methode'] == "Filtrowany Naiwny Bayes":
            filtered = True
            if flask.request.form['Profil'] == "Ameryka: 8. Klasa (Oceny: 1-6)":
                profile = "US8_6"
                validity = '61.12%'
            elif flask.request.form['Profil'] == "Ameryka: 8. Klasa (Oceny: 0-15)":
                profile = "US8_16"
                validity = '27.37%'
        text_grade, evidence = MN.run_magic(text, profile, factors=factors, bestfeatures=filtered)
        file_name = "UI/static/files/file_" + timestr + ".txt"
        file = open(file_name, "w", encoding="utf-8")
        file.write("===POCZĄTEK TEKSTU===" + "\n" + text + "\n" + "===KONIEC TEKSTU===")
        usedtime = time.asctime(time.localtime(time.time()))
        file.write("\n" + "Twoja Ocena: " + str(text_grade))
        file.write("\n" + "Użyta Metoda: " + flask.request.form['Methode'])
        file.write("\n" + "Użyty Profil: " + flask.request.form['Profil'])
        file.write("\n" + "Evidence: " + evidence)
        file.write("\n" + "Dokładność Profilu: " + validity)
        file.write("\n" + "Data Korekcji: " + usedtime)
        file.close()
        file = open(file_name, "r", encoding="utf-8")
        file_used = file.read()
        return flask.render_template('grade_pl.html', text_grade=text_grade, method=flask.request.form['Methode'],
                                     profile=flask.request.form['Profil'], evidence=evidence, validity=validity, file_used=file_used)
    except:
        return flask.render_template('error_pl.html')


if __name__ == "__main__":
    url = 'http://127.0.0.1:5000'
    webbrowser.open_new(url)
    app.run()
