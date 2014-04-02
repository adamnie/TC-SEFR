"""
grzebanie.py
Trying to figure out whats going on in TC-SEFR
Very far from optimalization, huge mess but something
"""

# necessary imports
from scipy import misc
import matplotlib.pyplot as plt
import numpy

# OF COURSE it's better to write these functions as methods for our class, but i don't know yet how to do it

# helper function for plotting images in grayscale
def plotgray(image,no="yes"):
    if (no == "no"): #no interpolation
        plt.imshow(image, cmap=plt.cm.gray, interpolation='none')
        plt.show()
    else:
        plt.imshow(image, cmap=plt.cm.gray)
        plt.show()

def imsize(image, which):
    if (which == "h" or which == "hor"):
        return len(image[1])
    elif (which == "v" or which == "ver"):
        return len(image)
    else:
        return -1

def printsize(image):
    print "Image size: vertical " + str(imsize(image, "v")) + ", horizontal: " + str(imsize(image,"h"))

def d_block(image, index_v, index_h): #index_v, index_h are from 0 to len/blocksize
    start_h = index_h * blocksize
    start_v = index_v * blocksize
    print start_h, start_v
    crop1 = image[start_h:start_h+blocksize]
    crop2 = numpy.zeros(shape=(blocksize,blocksize))
    for index in range(blocksize):
        crop2[index] = (crop1[index])[start_v:start_v+blocksize]
    return crop2
        

#important - images are stored as arrays, they're zero indexed!
image = misc.lena()

print "Loaded image..."
#misc.imsave('lena.png',image) #exporting to ext file

printsize(image)

# Small blocks are size blocksize x blocksize
# Big blocks are size 2blocksize x 2blocksize
blocksize = 4

if (imsize(image,"v")%(2*blocksize) != 0 or imsize(image,"h")%(2*blocksize) != 0):
    print "Wrong picture, cropping..." # could use better error handling, but dont know what
    image = image[1:len(image)-imsize(image,"v")%(2*blocksize)]
    for line in image:
        line = line[1:len(image)-imsize(image,"h")%(2*blocksize)]
    
    print "Cropped:",
    printsize(image)

print "Assuming size of big block (D) = " + str(blocksize)

print "That gives us " + str(imsize(image,"v")/blocksize) + "x" + str(imsize(image,"h")/blocksize) + "=" + str((imsize(image,"v")/blocksize) * (imsize(image,"h")/blocksize)) + " D blocks."

#to be consistent, we index d-blocks from 0

example = d_block(image, 0, 0)
print example
plotgray(example, "no") # interpolating i guess...
