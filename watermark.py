import numpy as np
from img import *
from metrics import *
from helpers import *

n = 8


image = open_img_PGM("reese.pgm")          # importing image
image.setflags(write=True)

for y in range(image.height()):
	for x in range(image.width()):
		image[y][x]=replacetwoLSB(image[y][x],0,0)

#if I understand correctly, its not about rearrannging the image but changing pixels in blocks!
imageA = image
imageB = image.shiftup()
imageC = image.shiftleft()

# in A we are using fractal compression, in B and C - DCT mechanism 

