import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import unittest
import numpy as np
import lib.helpers

class helpersTests(unittest.TestCase):
	def test_normalize_return_number(self):
		numbers = np.arange(50)
		for number in numbers:
			normalized = lib.helpers.normalize(number,100)
			self.assertIsInstance(normalized,int)
	def test_normalize_correct_range_in_range(self):
		numbers = np.arange(10)-5
		for number in numbers:
			normalized = lib.helpers.normalize(number,12)
			self.assertEqual(normalized,number + 6 )
	def test_normalize_correct_range_bigger(self):
		numbers = np.arange(10)+50
		for number in numbers:
			normalized = lib.helpers.normalize(number,40)
			self.assertEqual(normalized,39)
	def test_normalize_correct_range_lower(self):
		pass
	def test_normalize_max_odd(self):
		pass
	def test_normalize_max_even(self):
		pass
	def test_from_normalized_correct_range(self):
		pass
	def test_form_normalized_correct_values(self):
		numb = np.arange(78)-39
		normalized = np.empty((78,1))
		from_normalized = np.empty((78,1))
		for index in range(78):
			normalized[index,1] = normalize(numb[index,1],80)
			from_normalized[index] = from_normalized(normalized[index,1],80)

		for i in range(78):
			self.assertEqual( numb[i,1] , from_normalized[i,1] )

	# testy do
	# get coeficients, czy indeksowanie przy pobieraniu wspolczynnikow jest dobre
	# testy dct

def main():
    unittest.main()

if __name__ == '__main__':
    main()