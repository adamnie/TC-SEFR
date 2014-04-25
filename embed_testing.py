from fractal import *
from wm_img import *
from helpers import *
import numpy as np
import math
"""
	A blocks: 7(x) + 7(y) + 3(t) + s(7) + o(8)
	B blocks: 40 bits quantzation table
	C blocks: 40 bits quantization table
	Checksum: 16 bits

	========
	128 bits

	1) convert information into structure in which all data will be binary
	2) Divide binary data in a consistent way
	3) Clean bits
	4) Embed binary data
	5) retrieve binary data

	TO DO:
	make converting functions dependent on the size of x and y

"""

def to_bin_str(A_blocks,B_blocks,C_blocks,checksum):
	"""
		Converts data from A,B,C blocks and checksum into 1 128 bits long 
		string (len(string) == 128)
	"""
	x = "{0:07b}".format(A_blocks['x'])
	y = "{0:07b}".format(A_blocks['y'])
	t = "{0:03b}".format(A_blocks['t'])
	s = "{0:07b}".format(A_blocks['s'])
	o = "{0:08b}".format(A_blocks['o'])

	B = "{0:040b}".format(B_blocks)
	C = "{0:040b}".format(C_blocks)

	check = "{0:016b}".format(checksum)
	return x + y + t + s + o + B + C + check

def to_data(bin_string):

	"""
		Retrieves data from binary string:
		- transform list (A blocks) 32 bits
		- JPEG like data (B and C blocks) each 40 bits
		- checksum 16 bits
	"""
	data = []
	transform = {}
	transform['x'] = int(bin_string[:7],2)
	transform['y'] = int(bin_string[7:14],2)
	transform['t'] = int(bin_string[14:17],2)
	transform['s'] = int(bin_string[17:24],2)
	transform['o'] = int(bin_string[24:32],2)
	data.append(transform)

	B_blocks = int(bin_string[32:72],2)
	C_blocks = int(bin_string[72:112],2)
	data.append(B_blocks)
	data.append(C_blocks)

	checksum = int(bin_string[112:128],2)
	data.append(checksum)

	return data

def embed(block,A_blocks_data,B_blocks_data=0,C_blocks_data=0,checksum=0):
	"""
		Inserts data from 3 block types and checksum into 2 last bits of every pixel(grey scale)
		and returns watermarked block (type numpy.array)
	"""
	bin_data = to_bin_str( A_blocks_data, B_blocks_data, C_blocks_data, checksum)
	size = int(math.sqrt(block.size))
	wm_block = np.empty([size,size])

	for i in range(size):
		for j in range(size):
			pixel = block[i,j] - block[i,j] % 4 # seting 2 last bit to 0
			wm_block[i,j] = pixel + int(bin_data[2*(i*size+j):2*(i*size+j+1)],2) # seting 2 last bits to those from watermark
	return wm_block
		

def retrive(wm_block):
	"""
		Retrieves data from watermarked image, then converts it from binary to decimal
	"""
	size = int(math.sqrt(wm_block.size))
	bin_data = ""

	for i in range(size):
		for j in range(size):
			bin_data += "{0:02b}".format(int(wm_block[i,j]) % 4)
	data = to_data(bin_data)
	return 	data
