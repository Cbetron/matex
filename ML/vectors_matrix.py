#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."

import math
import numpy
import random

"""Vektor functions"""


def vector_add(v, w):
    return [vi + wi for vi, wi in zip(v, w)]


def vector_sub(v, w):
    return [vi - wi for vi, wi in zip(v, w)]


def skalarproduct(v, w):
    """Summer aller komponentenn der Vektoren, länge des Vektors v in richtung w"""
    return sum(v_i * w_i for v_i, w_i in zip(v, w))


def sum_of_squares(v):
    return skalarproduct(v, v)


def magnitude(v):
    """Betrag eines Vektors"""
    return math.sqrt(sum_of_squares(v))


"""Matrix Functions"""


def shape(m):
    numrows = len(m)
    numcols = len(m[0])
    return numrows, numcols


def get_row(m, num):
    return m[num]


def get_column(m, num):
    return [m_i[num] for m_i in m]


def make_matrix(num_rows, num_cols, entry_fn):
    return [[entry_fn(i, j) for j in num_cols] for i in num_rows]


"""Arbeit mit Daten"""


def mean(x):
    return sum(x) / len(x)


def percentage(part, amount):
    return part / (amount / 100)


def data_range(x):
    """Streuweite unserer Daten"""
    return max(x) - min(x)


def de_mean(x):
    """
    mittlere absolute Abweichung Normalisierte Werte zum besseren
    Ableses des Mittelwertes und der Verteilung der Werte
    """
    xbar = mean(x)
    return [x_i - xbar for x_i in x]


def variance(x):
    deviations = de_mean(x)
    return sum_of_squares(deviations) / (len(x) - 1)


def covariance(x, y):
    """Kovarianz von zwei Mengen an Daten --> Pearson-Kovarianz"""
    return skalarproduct(de_mean(x), de_mean(y)) / (len(x) - 1)


def standartdeviation(x):
    """Standartverteilung"""
    return math.sqrt(variance(x))


def correlation(x, y):
    stdx = standartdeviation(x)
    stdy = standartdeviation(y)
    if stdx > 0 and stdy > 0:
        return covariance(x, y) / stdx / stdy
    else:
        return 0


"""Learning"""


def mu(values):
    """Determine mu for an amount of values"""
    return sum(values) / len(values)


def gauss(x, mu=0, sigma=1):
    """Normalverteilung einer Variabeln x"""
    sqrt_two_pi = math.sqrt(2 * math.pi)
    return math.exp(-(x - mu) ** 2 / 2 / sigma ** 2) / (sqrt_two_pi * sigma)


def gauss_multivariant(valuevec, mu_vec, cov_matrice):
    """Multivariante Normalverteilung eines vektors v"""
    mahalanobisdistance = numpy.transpose(valuevec - mu_vec)
    dimensions = len(valuevec)
    print("Mahalanobis: " + str(mahalanobisdistance))
    print("Part1: " + str(1 / (math.sqrt(2 * math.pi) ** dimensions * numpy.linalg.det(cov_matrice))))
    print("Part2: " + str(numpy.exp(-0.5 * mahalanobisdistance)))
    return 1 / (math.sqrt(2 * math.pi) ** dimensions * numpy.linalg.det(cov_matrice)) * numpy.exp(
        numpy.multiply(-0.5,  mahalanobisdistance))


"""List-functionalities"""


# def check_treatability(l, occuring, template, key=False):
#     if key:
#         l = [item[key] for item in l]
#     for cls in template:
#         if l.count(cls) < occuring * 2:
#             return False
#     return True
#
#
# def personal_splice(l, factor, key=False, rand=False):
#     splicesize = round(len(l) * factor)
#     if rand:
#         random.shuffle(l)
#     if key:
#         l = [item[key] for item in l]
#     return l[:splicesize]
#
#
# def check_occurrences(l, occuring, template, occurekey=""):
#     if occurekey:
#         l = [item[occurekey] for item in l]
#     for i in template:
#         if l.count(i) < occuring:
#             return False
#     return True
#
#
# def personal_list_split(l, factor, occuring, template, key=False):
#     if not check_treatability(l, occuring, template, key):
#         print("list not treatable!")
#         return False
#     splice_one = []
#     splice_two = []
#     while not check_occurrences(splice_one, occuring, template):
#         splice_one = personal_splice(l, factor, key, True)
#     while not check_occurrences(splice_two, occuring, template):
#         if key:
#             splice_two = [item[key] for item in l if item not in splice_one]
#         else:
#             splice_two = [item for item in l if item not in splice_one]
#     return splice_one, splice_two


if __name__ == "__main__":
    samplelist = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6]
    splices = personal_list_split(samplelist, 0.7, 2, range(1, 7, 1))
    print(splices)
