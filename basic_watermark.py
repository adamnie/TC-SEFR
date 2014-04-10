import numpy as np
import random
from PIL import ImageFile
from PIL import Image
from img import *
from metrics import *

# algorithm:
# 1. select randomly area of image to obtain initial pixel values
# 2. convert them to binary
# 3. form a watermarking key (max 2 or 3 bit length)
# 4. area = area | key (binary or)

# obraz = open_img_PGM("mona_lisa.pgm")  nie dziala :(

obraz = misc.lena()                        # importing image
image = obraz.view(img)                    # numpy way of subclassing...

image.plot()

rand_width = random.randint(0,image.width()-1)
rand_height = random.randint(0,image.height()-1)

losowosc = image.cutsquare(rand_width, rand_height, 3)
key = np.array([[8.,7.,6.],[5.,4.,3.],[2.,1.,0.]])
key = key.view(img)

for y in range(losowosc.height()):
	for x in range(losowosc.width()):
		losowosc[x][y]=key[x][y]
		image[rand_width+x][rand_height+y] += key[x][y]  # adding, not ORing... obvious problems with values near 255

image.plot()