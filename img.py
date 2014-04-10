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

    # sets R block of size=blocksize and number [h,v] 
    # e.g. when you have 512x512 image and blocksize=4, you have 128x128 R blocks
    # img.blockR(0,0) returns first ([0,0]), img.blockR(0,1) returns second ([0,1])...
    # that goes to img.blockR(127,127) which returns lower right corner (last block)
    # warning: to be consistent, D blocks are 0-indexed!

    def cutsquare(self, x, y, size): # x i y sa w pikselach
        crop1 = self[y:y+size] # przyciecie pozadanej ilosci wierszy tabeli, czyli przyciecie wertykalne (y)
        crop2 = numpy.zeros(shape=(size,size))
        for index in range(size):
            crop2[index] = (crop1[index])[x:x+size]  #przyciecie pozadanej ilosci elementow w wierszu, czyli przyciecie horyzontalne (x)
        return crop2.view(img)

    def blockR(self, x, y, blocksize):
        sth = self.cutsquare(x*blocksize,y*blocksize,blocksize)
        return sth.view(R_block)

    # sets D block of size=2*blocksize and number [h,v] as defined above 
    def blockD(self, x, y, blocksize):
		if (x <= (self.width()/blocksize - 2) and y <= (self.height()/blocksize)-2):
			sth = self.cutsquare(x*blocksize,y*blocksize,2*blocksize)
			return sth.view(D_block)
		else:
			print "Blad indeksowania D_block"		
			return -1

# class for R_block for special operations
class R_block(img):

	def plot(self): # overriding inherited plot by one with no interpolation
		plt.imshow(self, cmap=plt.cm.gray, interpolation='none', norm=plt.Normalize(0,255)) # bez normalizacji normalizuje do max i min z self
		plt.show()

# class for D_block for special operations
class D_block(img):

	def plot(self): # overriding inherited plot by one with no interpolation
		plt.imshow(self, cmap=plt.cm.gray, interpolation='none', norm=plt.Normalize(0,255)) # bez normalizacji normalizuje do max i min z self
		plt.show()
