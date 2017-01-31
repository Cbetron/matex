#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""webcrawling.py: webcrawling..."""

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__author__ = "Raphael Kreft"
__email__ = "raphaelkreft@gmx.de"
__status__ = "dev"

import urllib.request
from bs4 import BeautifulSoup
import time
import contextlib
import multiprocessing
import lxml
import sys
import re
import os


def getHTML(Url):
    """
    Diese Funktion lädt den Seitenquelltext einer Website herunter

    :param Url: Die Url von der gelesen werden soll
    :return:
    """
    try:
        req = urllib.request.Request(Url, None, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0'})
        with contextlib.closing(urllib.request.urlopen(req, timeout=10)) as x:
            html = x.read()
            return html
    except Exception:
        print("Failed to etablish connection to {}".format(Url))
        raise ConnectionError


def link_filter(links, domainendings=None):
    """
    returns the link if it end with specific domainendings
    :param  link: The list of link or the link you want to check/flter
            domainendings: A list of Domainendings, you want to use to filter links
    :return link: The filtered link or list of links
    """
    links = list(links)
    if domainendings is None:
        # Domainendings for english links
        domainendings = [".com", ".en", ".co.uk", ".org", ".gi", ".ca", ".au"]
    for l in links:
        if not any([domainending + "/" in l for domainending in domainendings]):
            links.remove(l)
        else:
            pass
    return links


def handle_local_links(url, link):
    if link.startswith('/'):
        return ''.join([url, link])
    elif link.startswith("http"):
        return link
    else:
        pass


def get_links(url):
    """
    Search an url for existing links
    :param url: The url you want to search the links in.
    :return: links: a list of the found links
    """
    try:
        links = []
        if url:
            resp = getHTML(url)
            soup = BeautifulSoup(resp, 'lxml')
            html_links = soup.find_all('a', attrs={'href': re.compile("^http://")})
            for link in html_links:
                ergebnis = link.get("href")
                if ".com" or ".co.uk" or ".au" or ".gl" or ".gi" or ".ca" or ".org" or ".com.au" in ergebnis:
                    links.append(str(ergebnis))
                else:
                    continue
        return links
    except TypeError as e:
        print(e)
        print('Type Error occured!')
        return []
    except IndexError as e:
        print(e)
        print('We probably did not find any useful links, returning empty list')
        return []
    except ConnectionError:
        return []
    except Exception as e:
        print("unknown Exception, going to log at {}".format(os.getcwd()))
        with contextlib.closing(open("".join([time.ctime(), ".log"]), "w")) as file:
            file.write("Error occured:  {}".format(e))
        return []


def link_spider(filename, stages, filtering=True, processes=None):
    """
    take some starting urls and search links in it
    :param filename: Name of the file, you read/write the links
    :param stages: The stages the spider should process
    :return:
    """
    try:
        with contextlib.closing(open(filename, "r")) as file:
            content = file.readlines()
            if not processes:
                processes = len(content)
    except FileNotFoundError:
        print("couldnt find file: {}".format(filename))
        sys.exit(1)
    p = multiprocessing.Pool(processes=processes)
    print("starting to crawl for Links with {} Processes".format(processes))
    data = set()
    for counter in range(0, stages):
        print("processing stage {}".format(counter + 1))
        new_data = p.map(get_links, content)
        [data.add(link) for links in new_data for link in links if link not in data]
        content = [link for links in new_data for link in links]
    if data:
        with contextlib.closing(open(filename, "a")) as file:
            if filtering:
                data = link_filter(data)
                data = set(data)
            for link in data:
                file.write("{}\n".format(link))
    else:
        print("No Data!\nPlease check your Connection!\nexiting...")
        sys.exit(1)


def get_pure_text(url):
    """
    :param url: te url from that you want to get the text
    :return: ascitext: the extractet text
    """
    print("Try to get Text from {}".format(url))
    try:
        html = getHTML(url)
        soup = BeautifulSoup(html, "lxml")
        paragraphs = soup.find_all('p')
        ascitext = ""
        for paragraph in paragraphs:
            texts = re.findall("<.*>(.*)<", str(paragraph))
            for text in texts:
                ascitext += text
        return ascitext
    except TypeError as e:
        print(e)
        print('Type Error occured!')
        return []
    except IndexError as e:
        print(e)
        print('We probably did not find any useful links, returning empty list')
        return []
    except ConnectionError:
        return []
    except Exception as e:
        print("unknown Exception, going to log at {}".format(os.getcwd()))
        with contextlib.closing(open("".join([time.ctime(), ".log"]), "w")) as file:
            file.write("Error occured:  {}".format(e))
        return []


def text_spider(filename, mode="file", processes=10):
    """
    Read links from a file and writes all text in one file or returns it
    :param filename: The name, the links are read from...
           mode:    file to write text in a file, return to return data :)
    :return:
    """
    try:
        with contextlib.closing(open(filename, "r")) as file:
            links = file.readlines()
    except FileNotFoundError:
        print("couldnt find file: {}".format(filename))
        sys.exit(1)
    print("Starting to get Texts with {} Processes!...".format(processes))
    p = multiprocessing.Pool(processes=processes)
    data = p.map(get_pure_text, links)
    if [] in data:
        data.remove([])
    if mode is "file":
        with contextlib.closing(open("texts_{}.txt".format(time.ctime()), "w")) as file:
            file.write(data)
    elif mode is "return":
        return data


if __name__ == "__main__":
    print(get_pure_text("https://pythonprogramming.net/"))
