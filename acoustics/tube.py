from .endcorrection import EndCorrection
class Tube:
    def __init__(self, config):
        self.lt = config['lt']
        self.dt = config['dt']
        self.gt = config['gt']
        self.holes = config['holes']
        self.c = 346 * 1000 # TODO: move in config
        self.dleratio = 1.059
        self.EC = EndCorrection()

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
                dle = (self.dleratio - (self.lt + dlt) / (self.lt + 2 * dlt)) * (self.lt + 2 * dlt)

            # Cris Forster - Musical Mathematics, Eq. 8.20
            lengths = [dle + self.lt + dlt]
            endcorrections = [dlt]
            embouchures = [dle]

            # compute the acoustic lengths of air columns at each hole
            for i, h in enumerate(self.holes):
                # Cris Forster - Musical Mathematics, Eq. 8.14
                LBh = (self.gt + h[1]) * (self.dt / h[1]) ** 2 - 0.45 * self.dt
                # Cris Forster - Musical Mathematics, Eq. 8.23
                LL = h[0] + dle
                # Cris Forster - Musical Mathematics, Eq. 8.24 and 8.25
                LT = lengths[i]
                # Cris Forster - Musical Mathematics, Eq. 8.22
                # based on Nederveen, Acoustical Aspects of Woodwind instruments, Eq. 32.14
                LA = LL + LBh * (LT - LL) / (LT - LL + LBh)
                lengths.append(LA)

                dlt = self.EC.get(self.dt / 2, 2 * LA / n)
                endcorrections.append(dlt)
                if not blown:
                    dle = dlt
                else:
                    dle = (self.dleratio - (LA + dlt) / (LA + 2 * dlt)) * (LA + 2 * dlt)
                embouchures.append(dle)

            frequencies = [n * self.c / 2 / l for l in lengths]
            frequencies.sort()
            b = dict()
            b['frequency'] = frequencies
            b['end'] = endcorrections
            b['embouchure'] = embouchures
            b['length'] = lengths
            a['register' + str(n)] = b

        return a
