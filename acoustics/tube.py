from .endcorrection import EndCorrection
from math import sqrt
class Tube:
    def __init__(self, config):
        self.lt = config['lt']
        self.dt = config['dt']
        self.gt = config['gt']
        self.holes = config['holes']
        self.c = 346 * 1000 # TODO: move in config
        self.dle = config['dle']
        self.EC = EndCorrection()

    def closed_correction(self, holes):
        return sum([1 / 4 * self.gt * (h[1] / self.dt) ** 2 for h in holes])

    def analyze(self, registers=3, blown=True):
        a = dict()
        for n in range(1, registers + 1):
            # End correction for the full length tube
            dlt = self.EC.get(self.dt / 2, 2 * self.lt / n)

            # Embouchure correction for the full length tube
            if not blown:
                # In this case, we're dealing with a tube that is not blown by
                # player's lips but is somehow vibrating openly, so apply the
                # end correction for both ends.
                dle = dlt
            else:
                dle = self.dle

            dlc = self.closed_correction(self.holes)

            # Account for wall loss
            # I never found a formula for this so I figured out this approximation.
            # Wall loss is more at smaller bore diameters and is naturally more
            # for longer tube lengths.
            dlw = (2 / self.dt) ** 2 * self.lt
            #print("adding dlw = {} with dlw / lt = {}".format(dlw, dlw / self.lt))

            # Cris Forster - Musical Mathematics, Eq. 8.20
            lengths = [dle + dlw + dlc + self.lt + dlt]
            endcorrections = [dlt]
            embouchures = [dle]
            holecorrections = [0]
            closedholes = [dlc]

            # compute the acoustic lengths of air columns at each hole
            for i, h in enumerate(self.holes):
                dlc = self.closed_correction(self.holes[i+1:])
                closedholes.append(dlc)

                # Cris Forster - Musical Mathematics, Eq. 8.14
                # LBh = (self.gt + h[1]) * (self.dt / h[1]) ** 2 - 0.45 * self.dt

                # Cris Forster - Musical Mathematics, Eq. 8.23
                LL = h[0] + dlc + dle
                # Cris Forster - Musical Mathematics, Eq. 8.24 and 8.25
                LT = lengths[i]

                if i > 0:
                    z = self.holes[i-1][0] - h[0]
                else:
                    z = self.lt - h[0]
                LBh = (z/2) * (sqrt(1 + (4/z) * (self.gt + 3/4 * h[1]) * (self.dt/h[1]) ** 2) -1)
                holecorrections.append(LBh)

                # Cris Forster - Musical Mathematics, Eq. 8.22
                # based on Nederveen, Acoustical Aspects of Woodwind instruments, Eq. 32.14
                LA = LL + LBh * (LT - LL) / (LT - LL + LBh)
                lengths.append(LA)

                dlt = self.EC.get(self.dt / 2, 2 * LA / n)
                endcorrections.append(dlt)
                if not blown:
                    dle = dlt
                else:
                    dle = self.dle
                embouchures.append(dle)

            frequencies = [n * self.c / 2 / l for l in lengths]
            frequencies.sort()
            b = dict()
            b['frequency'] = frequencies
            b['end'] = endcorrections
            b['embouchure'] = embouchures
            b['length'] = lengths
            b['hole'] = holecorrections
            b['closed'] = closedholes
            a['register' + str(n)] = b

        return a
