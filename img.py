"""
    img.py
    Defining classes with all needed methods.
"""

import numpy as np
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

    def checksize(self):
        if (image.height()%(2*Rsize) != 0 or image.width()%(2*Rsize) != 0):   # Checking if our image can be divided into block without rest
            image = image[1:len(image)-image.height()%(2*Rsize)] # If not, cropping from down right corner
            for line in image:
                line = line[1:len(image)-image.width()%(2*Rsize)]
    
    # plots normalized image in grayscale
    def plot(self): #in grayscale
        plt.imshow(self, cmap=plt.cm.gray, norm=plt.Normalize(0,255))
        plt.show()

    # exports image to file
    def export(filename):
        misc.imsave(filename,self)

    # can be used to zooming with plot()!
    def cutsquare(self, x, y, size): # x i y sa w pikselach
        crop1 = self[y:y+size] # przyciecie pozadanej ilosci wierszy tabeli, czyli przyciecie wertykalne (y)
        crop2 = numpy.zeros(shape=(size,size))
        for index in range(size):
            crop2[index] = (crop1[index])[x:x+size]  #przyciecie pozadanej ilosci elementow w wierszu, czyli przyciecie horyzontalne (x)
        return crop2.view(img)
   
    # sets R block of size=Rsize and number [h,v] 
    # e.g. when you have 512x512 image and Rsize=4, you have 128x128 R blocks
    # img.blockR(0,0) returns first ([0,0]), img.blockR(0,1) returns second ([0,1])...
    # that goes to img.blockR(127,127) which returns lower right corner (last block)
    # warning: to be consistent, D blocks are 0-indexed!

    def blockR(self, x, y, Rsize):   # NON-OVERLAPPING
        sth = self.cutsquare(x*Rsize,y*Rsize,Rsize)
        return sth.view(R_block)
    
    #poki co bez modulo, ok? 

    def howmanyDinarow(self, Rsize, delta=None):
        if (delta == None):
            delta = Rsize
        return (self.width() - 2*Rsize)/delta + 1

    def howmanyDinacolumn(self, Rsize, delta=None):
        if (delta == None):
            delta = Rsize
        return (self.height() - 2*Rsize)/delta + 1


    # size of block D is 2x size of block R
    # as an argument we pass the same Rsize as to block R! it is multiplied inside the function
    # delta is the step of selecting next image, default it's equal to Rsize 
    # x and y are numbers (indexes) of block D, assuming Dsize=2*Rsize and step=delta

    def blockD(self, x, y, Rsize, delta=None): # OVERLAPPING
        if (x>self.howmanyDinarow(Rsize,delta)-1 or y>self.howmanyDinacolumn(Rsize,delta)-1):
            print "Blad indeksowania D!!!"
            return -1
        if (delta == None):
            delta = Rsize
        sth = self.cutsquare(x*delta,y*delta,2*Rsize)
        return sth.view(D_block)

    def block_number_x(self,blocksize):
        return self.width()/blocksize

    def block_number_y(self,blocksize):
        return self.width()/blocksize

    def shiftup(self,x=4):
        return np.roll(self,-x,axis=0)

    def shiftleft(self,x=4):
        return np.roll(self,-x,axis=1)


# class for R_block for special operations
class R_block(img):

    def plot(self): # overriding inherited plot by one with no interpolation
        plt.imshow(self, cmap=plt.cm.gray, interpolation='none', norm=plt.Normalize(0,255)) # bez normalizacji normalizuje do max i min z self
        plt.show(block=True)

# class for D_block for special operations
class D_block(img):

    def plot(self): # overriding inherited plot by one with no interpolation
        plt.imshow(self, cmap=plt.cm.gray, interpolation='none', norm=plt.Normalize(0,255)) # bez normalizacji normalizuje do max i min z self
        plt.show(block=True)