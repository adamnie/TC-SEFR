"""
watermark.py
implementing the algorithm of watermarking from the article
"""

import numpy as np
from img import *
from metrics import *
from helpers import *
from wm_img import *

n = 8

image = open_img_PGM("pepper.pgm")          # importing image
image.setflags(write=True)                 # bez tego nie chcialo sie zapisywac

for y in range(image.height()):
    for x in range(image.width()):
        image[y][x]=replacetwoLSB(image[y][x],0,0)   # zastepuje w kazdym pikselu dwa ostatnie bity zerami

#if I understand correctly, its not about rearrannging the image but changing positions of blocks!
imageA = image.view(blockA)
imageB = image.shiftup().view(blockB)
imageC = image.shiftleft().view(blockC)

# in A we are using fractal compression, in B and C - DCT mechanism 

a=[]

# te "mappery" prawdopodobnie niepotrzebne
a.append(imageA.quadrant(0))
a[0].set_mapper()
a.append(imageA.quadrant(1))
a[1].set_mapper()
a.append(imageA.quadrant(2))
a[2].set_mapper()
a.append(imageA.quadrant(3))
a[3].set_mapper()

compA0 = compression_A(n/2,a[0],a[2])   #tutaj wypadaloby wykorzystac te mappery, ale recznie jest latwiej
compA1 = compression_A(n/2,a[1],a[3])   #mialy byc po to, zeby bylo skalowalnie, ale przeciez nie bedziemy tego skalowac
compA2 = compression_A(n/2,a[2],a[0])
compA3 = compression_A(n/2,a[3],a[1])

# Nie mam pojecia jak przetworzyc te dane. Bede potrzebowal z tym jutro pomocy.