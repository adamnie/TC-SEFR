import numpy as np
from numpy import linalg as LA
from PIL import ImageFile
from PIL import Image
from img import *

# y - vertical , x - horizontal

"""
	future optimization : instead of x and y indexes hash should be used

	C should be used to improve compare function
"""
def compare(R,D):

	"""
	computes best match Domain block(D) for Range Block (R)

	E(R, D) = norm(R - (s*D + o*U))

	lowest E defines best match
	s = ( (R-R_average *U) dot (D-D_average *U) ) / ( (D-D_average *U) dot (D-D_average *U) )
	o = R_average - s*D_average
	"""
	Res = {}

	R_average = R.mean();
	D_average = D.mean();
	s = (np.array(R-R_average)*np.array(D-D_average)).sum() / (np.array(D-D_average)*np.array(D-D_average)).sum()
	o = R_average - s* D_average;
	E = LA.norm(R*(s*D+o))

	Res['E'] = E
	Res['s'] = s
	Res['o'] = o
	Res['x'] = -1
	Res['y'] = -1
	Res['t'] = -1

	return Res

def transform(D,type):
	"""
	  possible rotations (in degrees): 0 , 90 , 180 , 270
	  possible flips: left-to-right
	"""
	#if type >= 8:
	#  print 'Error, transformation not handled'
	#  return -1

	if type >= 4:
		return np.rot90(np.fliplr(D),type%4)
	else:
		return np.rot90(D,type%4)

def average(D):
	"""
		Averages four neighbouring pixels
	"""
	newShape = len(D)/2
	D_av = np.empty([newShape,newShape])
	for i in range(0,newShape):
		for j in range(0,newShape):
			D_av[i,j] =  D[2*i:2*(i+1),2*j:2*(j+1)].mean()
	return D_av

def compression(R_size,image):
	"""
		function finds best match Domain Block (D) for every Range Block (R)
		saves data (x,y,s,o,E,t) into transform_list(not yet)
	"""
	MAX_ERROR = float('inf')

	R_number = [image.block_number_x(R_size) , image.block_number_y(R_size)]
	D_number = [image.block_number_x(2*R_size) , image.block_number_y(2*R_size)]

	D_list = get_D_blocks(image,D_number,R_size)

	transform_list = []
	for R_x in range(0,R_number[0]):
		transform_list.append([])
		for R_y in range (0,R_number[1]):
			R = image.blockR(R_y,R_x,R_size)
			transform_list[R_x].append({'E': MAX_ERROR})
			for D_x in range(0,D_number[0]):
				for D_y in range (0,D_number[1]):
					for T_type in range(7):
						Res = compare(R,transform(D_list[D_x][D_y],T_type))
						if Res['E'] < transform_list[R_x][R_y]['E']:
							transform_list[R_x][R_y] = Res 
							transform_list[R_x][R_y]['x'] = D_x
							transform_list[R_x][R_y]['y'] = D_y
							transform_list[R_x][R_y]['t'] = T_type
					
	return transform_list

def get_D_blocks(image,D_number,R_size):
	D_list = []
	for D_x in range(0,D_number[0]):
		D_list.append([])
		for D_y in range (0,D_number[1]):
			D = image.blockD(D_y,D_x,R_size)
			D = average(D)
			D_list[D_x].append(D)

	return D_list

def open_img_PGM(filename):
	"""
	Opens .PGM image using pillow library

	should return 2D list / numpy.array of pixels in gray scale
	"""

	fp = open(filename,'rb')

	p = ImageFile.Parser()

	while True :
		s = fp.read(1024)
		if not s:
			break
		p.feed(s)

	im = p.close()

	pixels = np.asarray(im)
	return pixels.view(img)

def decompression(transform_list,img_size,blockSize):
	Base = np.zeros(img_size)+127

	for iteration in range(0,2):
		for i in range(Base.shape[0]/blockSize):
			for j in range(Base.shape[0]/blockSize):

				Base[blockSize*i:blockSize*(i+1),blockSize*j:blockSize*(j+1)] = (transform(average(Base[transform_list[i][j]['x']:transform_list[i][j]['x']+2*blockSize,transform_list[i][j]['y']:transform_list[i][j]['y'] + 2*blockSize]),transform_list[i][j]['t']))*transform_list[i][j]['s'] + transform_list[i][j]['o']

	img = Image.fromarray(numpy.uint8(numpy.matrix(Base)))
	img.save('lena_frac.pgm')

