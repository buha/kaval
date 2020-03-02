import matplotlib.pyplot as plt
from acoustics import endcorrection
import numpy as np

e = endcorrection.EndCorrection()

xnew = np.arange(min(e.x), max(e.x), 0.01)
ynew = e.f(xnew)
plt.plot(e.x, e.y, 'o', xnew, ynew, '-')
plt.show()
