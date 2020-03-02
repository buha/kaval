from scipy.interpolate import interp1d
import scipy

# On the Radiation of Sound from an Unflanged Circular Pipe
# by HAROLD LEVINE AND JULIAN. SCHVINGER gives 0.6133 * radius 
# as the end correction of a tube with diameter << wavelength.
# They also present a plot of l/a versis ka. I graphically
# sampled this plot and obtained a few x/y value pairs which
# this class interpolates to provide in-between values for any
# ka.
class EndCorrection:
    def __init__(self):
        self.x = [0.0,0.105,0.181,0.257,0.356,0.461,0.566,0.695,0.818,0.923,1.08,1.401,1.711,2.038,2.336,2.616,2.82,2.978,3.165,3.328,3.48,3.597,3.708,3.784,3.832]
        self.y = [0.6133,0.610,0.607,0.603,0.596,0.586,0.576,0.563,0.549,0.538,0.519,0.484,0.451,0.415,0.382,0.353,0.331,0.314,0.292,0.271,0.25,0.228,0.203,0.176,0.14]
        self.f = interp1d(self.x, self.y, kind='cubic')

    def get(self, radius, wavelength):
        index = 2 * scipy.pi * radius / wavelength
        ratio = self.f(index)
        ret = ratio * radius
        print("Using end correction {0:.2f} with a radio of {1:.2f} for wavelength {2} at index {3}".format(ret, ratio, wavelength, index))
        return ret

