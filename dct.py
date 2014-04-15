from scipy.fftpack import dct , idct
import numpy as np

class DCT:
	"""
		Wrapper class for scipy.fftpack.dct/idct
	"""
	def perform(self,block_list):
		dct_list = []
		for block in block_list:
			dct_list.append(dct(block,type=3,norm='ortho'))
		return dct_list

	def reverse(self,DCT_LIST):
		block_list = []
		for dct in DCT_LIST:
			block_list.append(idct(dct,type=3,norm='ortho'))
		return block_list

	def compare(self,R,D):
		diff = 0.0 
		R_DCT = dct(R,type=3,norm='ortho')
		D_DCT = dct(D,type=3,norm='ortho')

		for i in range(len(R_DCT)):
			for j in range(len(R_DCT[0])):
				diff += abs(R_DCT[i,j] - D_DCT[i,j])

		return diff




