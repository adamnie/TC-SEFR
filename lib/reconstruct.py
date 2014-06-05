"""
To do:
o mark blocks (based on checksum ) in watermark.py
o 

"""
from fractal import *

class reconstruct :

	def __new__(self):
		self.fractal = fractal()

	def fromA(self,base,compression_data,R_block_size=4):
		return self.fractal.decompression(compression_data,base,R_block_size)

	def fromB(self,coefficients,img_size,block):
		pass
	def fromC(self,coefficients,img_size,block):
		pass