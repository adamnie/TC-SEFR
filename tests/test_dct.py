# fixing path
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import unittest
import numpy as np
import lib.dct

class dctTests(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		super(dctTests, self).__init__(*args, **kwargs)
		self.dct = lib.dct.DCT()
	def test_perform_zero(self):
		zero  = np.zeros((4,4))

		zero_dct = self.dct.perform(zero)
		zero_idct = self.dct.reverse(zero)

		np.testing.assert_allclose(zero,zero_idct,rtol=1e-5,atol=0) 
	def test_perform_positive(self):
		positive  = np.arange(16.0).reshape((4,4))

		positive_dct = self.dct.perform(positive)
		positive_idct = self.dct.reverse(positive)

		np.testing.assert_allclose(positive,positive_idct,rtol=1e-5,atol=0)
	def test_perform_negative(self):
		negative  = np.arange(64.0).reshape((8,8))-64

		negative_dct = self.dct.perform(negative)
		negative_idct = self.dct.reverse(negative)

		np.testing.assert_allclose(negative,negative_idct,rtol=1e-5,atol=0)

	def test_perform_mixed(self):
		mixed  = np.arange(100.0).reshape((10,10))-50

		mixed_dct = self.dct.perform(mixed)
		mixed_idct = self.dct.reverse(mixed)

		np.testing.assert_allclose(mixed,mixed_idct,rtol=1e-5,atol=0)

def main():
    unittest.main()

if __name__ == '__main__':
    main()