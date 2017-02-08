#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""pythonfile.py:	Description of pythonfile.py"""

__author__ = "Raphael Kreft"
__copyright__ = "Copyright (C) 2017  The maTex Authors.  All rights reserved."
__version__ = "Development v0.0"
__email__ = "raphaelkreft@gmx.de"
__status__ = "Dev"


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math

import numpy

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

