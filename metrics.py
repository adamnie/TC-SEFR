import numpy as np
from numpy import linalg as LA
from PIL import ImageFile

# y - vertical , x - horizontal

"""
	future optimization : instead of x and y indexes hash should be used
"""

def E(R,D):

	"""
	computes best match Domain block(D) for Range Block (R)

	E(R, D) = norm(R - (s*D + o*U))

	lowest E defines best match

	s = ( (R-R_average *U) dot (D-D_average *U) ) / ( (D-D_average *U) dot (D-D_average *U) )
	o = R_average - s*D_average
	
	"""

	R_average = np.mean(R) 
	D_average = np.mean(D)

	R_shape = np.shape(R)

	U = np.ones(R_shape)

	R_sub = np.subtract(R,np.multiply(R_average,U)) # R - R_average*U
	D_sub = np.subtract(D,np.multiply(D_average,U)) # D - D_average*U

	# if np.dot(D_sub,D_sub) != 0:
	if np.dot(D_sub.flatten(),D_sub.flatten()) == 0:
		s = 0
	else:
		s = np.divide( np.dot(R_sub.flatten(),D_sub.flatten()) , np.dot(D_sub.flatten(),D_sub.flatten()) ) # there will be problem if dot(D_sub,D_sub  == 0)
	# elif np.dot(R_sub,D_sub) != 0:
	  # s = float('inf') # number/0 = infinity
	# else:
	  # s = 0
	o = R_average - s * D_average

	E = LA.norm(np.subtract(R,np.multiply(s,D) + np.multiply(o,U)))

	return E

def block_coords(id,block_size,img_x_size,img_y_size):
	"""
		Calcucaltes x and y indexes of top left corner of the block
		and returns (a dictonary)
	"""
	coords = {}

	coords['x'] = (id-1)*block_size % img_x_size
	coords['y'] = ((id-1)*block_size / img_x_size)*block_size # there is only one left top corner line for each block_size


	if coords['y'] > img_y_size:
		print 'Error, fuck you!'
		return None
	return coords

def block(id,block_size,img):
	"""
		Based on id returns image block
	"""

	img_y_size = len(img)
	img_x_size = len(img[0])

	left_corner = block_coords(id,block_size,img_x_size,img_y_size)

	block = np.empty([block_size,block_size])

	for i in range(0,block_size-1):
			for j in range(0,block_size-1):
				block[i][j] = img[left_corner['y']+i[left_corner['x']+j]

	return block

def rotation(D):
	"""
	  possible rotations (in degrees): 0 , 90 , 180 , 270
	  rotation is clockwise

	  Is it possible to join 4 blocks and rotate the bigger one ?
	  joining speed vs rot speed
	"""

	rotated_D = []

	rotated_D.append(D)
	rotated_D.append(np.rot90(D,3))
	rotated_D.append(np.rot90(D,2))
	rotated_D.append(np.rot90(D,1))

	return rotated_D

def average(block):
	"""
		Averages four neighbouring pixels
	"""
	average = np.empty([len(block)/2,len(block)/2])
	ver = np.hsplit(block,2)
	for subArr in ver:
		np.append(average,np.hsplit(subArr,2))

	for subArr in average:
		subArr = np.mean(subArr)

	return average
			
def calculate_transformation():
	"""
		function finds best match Domain Block (D) for every Range Block (R)
		saves data (x,y,s,o,E,t) into transform_list(not yet)

	"""
	pixels = open_img_PGM()

	pixels_size_y = len(pixels)
	pixels_size_x = len(pixels[0])

	R_size = 2
	D_size = 4

	R_number = calculate_block_number(R_size,pixels_size_x,pixels_size_y)
	D_number = calculate_block_number(D_size,pixels_size_x,pixels_size_y)

	E_list = float('inf')* np.ones([R_size,1])


	for R in range(0,R_number):
		for D in range(0,D_number):
			E_ = E(block(R,R_size,pixels),average(block(D,D_size,pixels)))
			if (E_ < E_list[R]):
				E_list[R] = E_

	return E

def open_img_PGM():
	"""
	Opens .PGM image using pillow library

	should return 2D list / numpy.array of pixels in gray scale
	"""

	fp = open("lena.pgm",'rb')


	p = ImageFile.Parser()

	while True :
		s = fp.read(1024)
		if not s:
			break
		p.feed(s)

	im = p.close()

	pixels = np.asarray(im)
	return pixels

def calculate_block_number(block_size,img_size_x,img_size_y):
	return (img_size_y*img_size_x)*(block_size ** 2)

print calculate_transformation()
