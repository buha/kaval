#!/usr/bin/python3
from tuning.helper import *
class Temperament:
    def equal(self, divisions, centerfreq, minfreq, maxfreq):
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
            while True:
                f = centerfreq * 2 ** (denominator / divisions)
                denominator += 1
                if f <= maxfreq:
                    temperament.append(f)
                else:
                    break
        
        denominator = 1
        if(left):
            f = centerfreq
            while True:
                f = centerfreq / 2 ** (denominator / divisions)
                denominator += 1
                if f >= minfreq:
                    temperament.append(f)
                else:
                    break 


        temperament.sort()
        return temperament

