# test
import numpy as np

a = np.arange(16)
a = a.reshape(4,4)
b = np.arange(16)
b = b.reshape(4,4)
c = np.vstack((a,b))
print c