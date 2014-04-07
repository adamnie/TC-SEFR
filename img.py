"""
    img.py
    Defining classes with all needed methods.
"""


from scipy import misc
import matplotlib.pyplot as plt
import numpy

# class for imported image
class img(numpy.ndarray):
    
    # initialize
    def __init__(self, obraz):
        self.obraz = obraz

    # returns width
    def width(self): ##former size_horizontal
        return len(self[1])

    # returns height
    def height(self): ##former size_vertical
        return len(self)

    # prints verbose size
    def printsize(self):
        print "Image size: height " + str(self.height()) + ", width: " + str(self.width())

    # plots normalized image in grayscale
    def plot(self): #in grayscale
        plt.imshow(self, cmap=plt.cm.gray, norm=plt.Normalize(0,255))
        plt.show()

    # exports image to file
    def export(filename):
        misc.imsave(filename,self)

    # sets D block of size and number [h,v] 
    # e.g. when you have 512x512 image and blocksize=4, you have 128x128 D blocks
    # img.blockD(0,0) returns first ([0,0]), img.blockD(0,1) returns second ([0,1])...
    # that goes to img.blockD(127,127) which returns lower right corner (last block)
    # warning: to be consistent, D blocks are 0-indexed!
    def blockD(self, v, h, blocksize):
        start_h = h * blocksize
        start_v = v * blocksize
        crop1 = self[start_h:start_h+blocksize]
        crop2 = numpy.zeros(shape=(blocksize,blocksize))
        for index in range(blocksize):
            crop2[index] = (crop1[index])[start_v:start_v+blocksize]
        return crop2.view(D_block)

# class for D_block for special operations
class D_block(img):

    def plot(self): # overriding inherited plot by one with no interpolation
        plt.imshow(self, cmap=plt.cm.gray, interpolation='none', norm=plt.Normalize(0,255)) # bez normalizacji normalizuje do max i min z self
        plt.show()
    
    

