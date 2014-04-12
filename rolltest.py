# rolltest.py

import numpy as np

test = np.arange(16)
print test

test = np.reshape(test, (4,4))
print test

print np.roll(test,-1,axis=0) # przesuwanie w gore

print np.roll(test,-1,axis=1) # przesuwanie w lewo

