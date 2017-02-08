#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""pdfcreator.py:	Ein Modul, zugeschnitten auf die Erstellung des Ausgabe-End-Pdfs"""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Raphael Kreft"
__version__ = "0.2"
__email__ = "raphaelkreft@gmx.de"
__status__ = "dev"

import os
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, PageBreak, SimpleDocTemplate
from reportlab.lib.colors import yellow, black, red
from reportlab.lib.pagesizes import A4



class PDF(object):
    """
    Diese Klasse Dient zum erstellen eines Ausgabepdfs unseres Programms
    """
    Pdf = None
    style = getSampleStyleSheet()
    story = []
    PATH = "UI/static/files/"

    def __init__(self, name, subtitle, method, profile, evidence, accuracy, timestring):
        """
        Weisst die Klassenvariabeln zu
        :param name: Der Name, der die Pdf haben soll
        """
        self.pdf_name = name
        self.define_styles()
        self.create_pdf(subtitle=subtitle, method=method, profile=profile, evidence=evidence, accuracy=accuracy, timestring=timestring)

    def define_styles(self):
        """
        EFügt einige styles hinzu
        :return:
        """
        try:
            self.style.add(ParagraphStyle(name='Subtitle', fontSize=14, alignment=TA_CENTER, spaceAfter=3))
            self.style.add(ParagraphStyle(name='Date', fontsize=12, fontName='Courier', alignment=TA_CENTER))
            self.style.add(ParagraphStyle(name='Grade', fontsize=20, alignment=TA_CENTER))
            self.style.add(ParagraphStyle(name='Infobox', fontsize=12, alignment=TA_LEFT, textColor=black, backColor=yellow, borderColor=yellow))
            self.style.add(ParagraphStyle(name='Errorbox', fontsize=12, alignment=TA_LEFT, textColor=black, backColor=red, borderColor=red))
        except KeyError:
            print("style already defined")

    def create_pdf(self, title="Textkorrektur - Wordchecker", subtitle="", method="", profile="", evidence="", accuracy="", timestring=""):
        """
        Erstellt ein Pdf mit dem Namen, der der Klasse übergeben wurde
        """
        outfilename = self.pdf_name + ".pdf"
        print(outfilename)
        outfilepath = os.path.join(self.PATH, outfilename)
        print(outfilepath)
        self.Pdf = SimpleDocTemplate(outfilepath, pagesize=A4)
        # Create Titlepage
        self.story.append(Paragraph(title, self.style['Title']))
        self.story.append(Paragraph(subtitle, self.style['Subtitle']))
        self.story.append(Paragraph(method, self.style['Date']))
        self.story.append(Paragraph(profile, self.style['Date']))
        self.story.append(Paragraph(evidence, self.style['Date']))
        self.story.append(Paragraph(accuracy, self.style['Date']))
        self.story.append(Paragraph(timestring, self.style['Date']))
        self.story.append(PageBreak())

    def insert_text(self, text, lines=True):
        """
        Fügt den zu korrigierenden Text formatiert in die Pdf ein
        """
        self.story.append(Paragraph("Text-Source", self.style['h1']))
        if lines:
            lines = text.split("\n")
            for num, line in enumerate(lines):
                self.story.append(Paragraph(str(num) + " " + str(line), self.style['BodyText']))
        else:
            self.story.append(Paragraph(str(text), self.style['BodyText']))

    def insert_info(self, infotext, style="Info"):
        """
        insert an infotextobject with specific text
        :param infotext: the text you want to have in your infobox
        :param style: Info or erroer for different colours
        :return:    -
        """
        if style is "Info":
            style = "Infobox"
        elif style is "Error":
            style = "Errorbox"
        # finally add Infobox to the story
        self.story.append(Paragraph(infotext, self.style[style]))

    def insert_featureextraction(self, valuevec):
        """
        Fügt den Namen eines Textfeatures und dessen werte formatiert in eine PDF ein. Diese werte werden aus einem
        Dictionary gelesen.
        :param analyse: Ein Dictionary welches das Rating enthält
        """
        tabledata = []
        self.story.append(Paragraph('Featureextraktions Ergebnisse', self.style['Heading1']))
        for name, value in valuevec.items():
            tabledata.append([str(name), str(value)])
        t = Table(tabledata)
        self.story.append(t)

    def insert_grade(self, grade):
        """
        Einfügen der Note
        :param grade: Endnote als string oder Integer
        :return:
        """
        self.story.append(Paragraph("Notentechnische Bewertung", self.style['h1']))
        # Note
        self.story.append(Paragraph(str(grade), self.style['Grade']))

    def save_pdf(self):
        """
        Sichert die Pdf bzw. Speichert diese
        """
        self.Pdf.build(self.story)

    def __str__(self):
        """
        Löscht das Objekt, Sichert die Pdf
        """
        print("Name: {}\nStory: {}".format(self.pdf_name, self.story))

    def __repr__(self):
        return self.story


if __name__ == "__main__":
    print("Test of PDF Library...")
    print("Init..")
    mypdf = PDF("newpdf")
    print("insert Text...")
    mypdf.insert_text("This is a sampletext of myself. its very glorios and nice. nikodem is a nice polish guy, which argues with cosima")
    print("Insert Grade...")
    mypdf.insert_grade(1)
    print("Insert Info...")
    mypdf.insert_info("Your Text is Bullshit!")
    print("Insert Featureextraction...")
    mypdf.insert_featureextraction({"value1": 123, "value2": 456})
    print("Try to save Pdf...")
    mypdf.save_pdf()
