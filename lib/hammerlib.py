from __future__ import division


def levenshtein_distance(x1, x2):
    """
    Finds a match between mis-spelt string based on the lavenhtein
    distance formula
    """

    if len(x1) > len(x2):
        x1, x2 = x2, x1

    distances = range(len(x1) + 1)
    for i2, c2 in enumerate(x2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(x1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1],
                    distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]


def spellmatch(x, y):
    """
    Returns the match percentage between two given strings
    using lavenhstein distance
    """

    distance = levenshtein_distance(x, y)
    return round(float(-(((distance/(len(x) + len(y)))*100)-100)),2)


def abbrmatch(x, y):
    """
    Returns the match percentage between two strings assuming one of
    the strings is the abbreviation for the other.
    """

    sl = ['-', '&', ',', ', ', ' - ', ';', '; ', '/', '/ ', ' / ']

    if len(x) > len(y):
        x, y = y, x

    for n in sl:
        x = x.replace(n, ' ')
        y = y.replace(n, ' ')

    xl = [n.lower().strip() for n in x.split()]
    yl = [n.lower().strip() for n in y.split()]

    ps = []
    for i, n in enumerate(xl[0]):
        ps.append(levenshtein_distance(n, ''.join([z[0] for z in yl])))

    return ps
