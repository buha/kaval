class Tube:
    def __init__(self, config):
        self.lt = config['lt']
        self.dt = config['dt']
        self.gt = config['gt']
        self.dle = config['dle']
        self.holes = config['holes']
        self.c = 346 * 1000 # TODO: move in config

    def analyze(self, registers=3):
        # On the Radiation of Sound from an Unflanged Circular Pipe
        # by HAROLD LEVINE AND JULIAN. SCHVINGER gives 0.6133 * radius 
        # as the end correction of a tube with diameter << wavelength.
        self.dlt = 0.6133 * self.dt / 2

        if self.dle == None:
            # In this case, we're dealing with a tube that is not blown by
            # player's lips but is somehow vibrating openly, so apply the
            # end correction for both ends.
            self.dle = 0
            self.dlt = self.dlt * 2

        # Cris Forster - Musical Mathematics, Eq. 8.20
        lengths = [self.dle + self.lt + self.dlt]
        
        # compute the acoustic lengths of air columns at each hole
        for i, h in enumerate(self.holes):
            # Cris Forster - Musical Mathematics, Eq. 8.14
            LBh = (self.gt + h[1]) * (self.dt / h[1]) ** 2 - 0.45 * self.dt
            # Cris Forster - Musical Mathematics, Eq. 8.23
            LL = h[0] + self.dle
            # Cris Forster - Musical Mathematics, Eq. 8.24 and 8.25
            LT = lengths[i]
            # Cris Forster - Musical Mathematics, Eq. 8.22
            # based on Nederveen, Acoustical Aspects of Woodwind instruments, Eq. 32.14
            LA = LL + LBh * (LT - LL) / (LT - LL + LBh)

            lengths.append(LA)
        
        frequencies = dict()
        for n in range(1, registers + 1):
            register = [n * self.c / 2 / l for l in lengths]
            register.sort()
            frequencies['register' + str(n)] = register

        return frequencies