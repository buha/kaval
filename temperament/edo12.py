#!/usr/bin/python3
from temperament import Temperament
# Equal division of the octave in 12 parts (12-EDO)
class EDO12(Temperament):

    # a4freq - A4 frequency, currently defined as 440 in ISO 16.
    # ipn    - Scientific/International pitch notation.
    def __init__(self,
                 a4freq = 440, 
                 ipn = ['Do', 'Do#', 'Re', 'Re#', 'Mi', 'Fa',
                        'Fa#', 'Sol', 'Sol#', 'La', 'La#', 'Si']):
        l = len(ipn)
        if l != 12:
            raise ValueError('Wrong number of elements ({}) passed in ipn'.
                             format(l))
        self._a4freq = a4freq
        self._ipn = ipn

    def table(self):
        t = self.equal(12, self._a4freq, 16.0, 8000.0) 
        pos = t.index(self._a4freq)
        rem = pos % 12
        ipnidx = 9 - rem 
        div = (pos - 9) // 12 # 9 stands for 10th element in ipn - 'La'
        startname = self._ipn[ipnidx] + str(3 - div) # 3 stands for the octave of A4
        d = {}
        for i, note in enumerate(t):
            div = i // 12
            d[self._ipn[(ipnidx + i) % 12] + str(div)] = note
        return d
