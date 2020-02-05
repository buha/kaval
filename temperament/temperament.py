#!/usr/bin/python3

def isinteger(n):
    if isinstance(n, int):
        return True
    if isinstance(n, float):
        return n.is_integer()
    return False

def isfloat(n):
    return isinstance(n, float)

def equal_temperament(divisions, centerfreq, minfreq, maxfreq):
    if not isinteger(divisions) or divisions < 2:
        raise ValueError('Equal Temperament divides the octave in more than '
                         'two integer number of parts.')

    if (not isinteger(centerfreq)
        or centerfreq < 0):
        raise ValueError('Equal Temperament center frequency is invalid.')

    if (not isfloat(minfreq)
        or not isfloat(maxfreq)
        or minfreq < 0
        or maxfreq < 0
        or maxfreq < maxfreq):
        raise ValueError('Equal Temperament frequency range was incorrectly '
                         'specified.')

    right = False
    left = False
    if centerfreq <= maxfreq:
        right = True
    if centerfreq >= minfreq:
        left = True

    temperament = [centerfreq]
    denominator = 1
    if(right):
        f = centerfreq
        while f <= maxfreq:
            f = centerfreq * 2 ** (denominator / divisions)
            denominator += 1
            temperament.append(f)

    denominator = 1
    if(left):
        f = centerfreq
        while f >= minfreq:
            f = centerfreq / 2 ** (denominator / divisions)
            denominator += 1
            temperament.append(f)

    temperament.sort()
    return temperament


