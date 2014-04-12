from scipy.fftpack import dct , idct
import numpy as np


def calculate_DCT(mat_list):
	ans = []
	for mat in mat_list:
		ans.append(dct(mat,type=3,norm='ortho'))
	return ans
def reverse_DCT(DCT_LIST):
	ans = []
	for dct in DCT_LIST:
		ans.append(idct(dct,type=3,norm='ortho'))
	return ans

def compare_DCT(R,D):
	diff = 0.0 
	R_DCT = dct(R,type=3,norm='ortho')
	D_DCT = dct(D,type=3,norm='ortho')

	for i in range(len(R_DCT)):
		for j in range(len(R_DCT[0])):
			diff += abs(R_DCT[i,j] - D_DCT[i,j])

	return diff

lista = []

for i in range(3):
	lista.append(np.arange(16.0).reshape(4,4)-i)

print lista[0]

print compare_DCT(lista[0],lista[1])
print compare_DCT(lista[1],lista[2])




