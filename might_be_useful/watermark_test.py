"""
watermark_new.py
    reinventing the wheel
"""

import numpy as np
from img import *
from helpers import *
from wm_img import *
from fractal import *

n = 8

# PHASE 0 - importing image
fractal = fractal()
image = fractal.open_img_PGM("pepper.pgm")         # importing image
#image.setflags(write=True)                 # bez tego nie chcialo sie zapisywac

# replacing two LSB with zeros - preparing to saving information
# for y in range(image.height()):
#     for x in range(image.width()):
#         image[y][x]=replacetwoLSB(image[y][x],0,0)   # zastepuje w kazdym pikselu dwa ostatnie bity zerami

imageA = image.view(wm_img)

howmanyblocks=[image.height()/n - 1,image.width()/n - 1]

# a = np.ndarray(shape=(n,n))
# b = dividedA[0][0]
# c = np.hstack((a,b))
# print f

# skladanie z czesci...
# outv = np.ndarray(shape=(len(imageA),len(imageA)))
# for y in range(len(dividedA)):
#     outh = np.ndarray(shape=(n,n))
#     for x in range(len(dividedA)):
#         outh = np.hstack((outh,dividedA[y][x]))
#     outv = np.vstack((outv, outh))
#     print y,
#     del outh
#     print "Nailed"
# outv = np.delete(outv,range(256),0)
# outv = np.delete(outv,range(8),1)
# outv.view(img).plot()
# imageA.plot()
# TODO - troche obcina - z 256x256 robi 248x248

# in A we are using fractal compression, in B and C - DCT mechanism 
imageA.blocks.append(imageA.quadrant(0))
imageA.blocks.append(imageA.quadrant(1))
imageA.blocks.append(imageA.quadrant(2))
imageA.blocks.append(imageA.quadrant(3))
A.append(fractal.get_D_blocks(a[0], howmanyblocks, n/2, delta=n, avg=False))
A.append(fractal.get_D_blocks(a[1], howmanyblocks, n/2, delta=n, avg=False))
A.append(fractal.get_D_blocks(a[2], howmanyblocks, n/2, delta=n, avg=False))
A.append(fractal.get_D_blocks(a[3], howmanyblocks, n/2, delta=n, avg=False))

fractal.get_D_blocks(a[0], howmanyblocks, n/2, delta=n, avg=False)


"""


# te "mappery" prawdopodobnie niepotrzebne


# tutaj kompresuje i staram sie naprawic wspolrzedne punktow


mapowanie :

3 0 
2 1

compA0 = fractal.compression(n/2,a[0],a[2])  # mapowanie quadrantu 0 na 2 
for y in range(len(compA0)):
    for x in range(len(compA0[1])):
        -compA0[y][x]['x']+=image.width()/(2*n)

compA1 = fractal.compression(n/2,a[1],a[3]) 
for y in range(len(compA0)):
    for x in range(len(compA0[1])):
        compA0[y][x]['y']+=image.height()/(2*n)
        compA0[y][x]['x']+=image.width()/(2*n)

compA2 = fractal.compression(n/2,a[2],a[0])
for y in range(len(compA0)):
    for x in range(len(compA0[1])):
        compA0[y][x]['y']+=image.height()/(2*n)

compA3 = fractal.compression(n/2,a[3],a[1])

up = np.hstack((compA3,compA0))
down = np.hstack((compA2,compA1))
raw_data_for_Adam = np.vstack((up,down)) #here you are, I guess


dct = DCT()

ojej = fractal.get_D_blocks(imageB.view(img), howmanyblocks, n)
ojej = [y for x in ojej for y in x]
DCTlistB = dct.perform(ojej)
rev = dct.reverse(DCTlistB)

print rev

"""

            # naprawa wspolczynnikow ponizej - ale nie dziala. moze zaimplementowac to 
            # for x in range(len(wspolczynniki.list[i])):
            #     for y in range(len(wspolczynniki.list[i][x])):
            #         for z in range(len(wspolczynniki.list[i][x][y])):
            #             wspolczynniki.list[x][y][z]["x"]+=imageA.quadrant_attr[imageA.quadrant_attr[i]["mapper"]]["x"]
            #             wspolczynniki.list[x][y][z]["y"]+=imageA.quadrant_attr[imageA.quadrant_attr[i]["mapper"]]["y"]
            # nazwa = "wspolczynniki" + str(i) + "_new.pickle" 
            # with open(nazwa, 'wb') as handle:
            #      pickle.dump(wspolczynniki.list[i], handle)
            # wspolczynniki.czas[i]=time() - start
            # del start
