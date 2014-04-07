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
    def blockR(self, x, y, blocksize):
        x *= blocksize                                             # NOT SURE ABOUT RIGHT INDEXING!!! WHICH ONE IS HOR & WHICH ONE IS VER!!!
        y *= blocksize
        crop1 = self[y:y+blocksize] # przyciecie pozadanej ilosci wierszy tabeli, czyli przyciecie wertykalne (y)
        crop2 = numpy.zeros(shape=(blocksize,blocksize))
        for index in range(blocksize):
            crop2[index] = (crop1[index])[x:x+blocksize]  #przyciecie pozadanej ilosci elementow w wierszu, czyli przyciecie horyzontalne (x)
        return crop2.view(R_block)

    """
    Assuming we have array of R blocks as shown below:
    +------+------+------+------+------+
    | R 00 | R 01 | R 02 | R 03 | R 04 |
    +------+------+------+------+------+
    | R 10 | R 11 | R 12 | R 13 | R 14 |
    +------+------+------+------+------+
    | R 20 | R 21 | R 22 | R 23 | R 24 |
    +------+------+------+------+------+
    | R 30 | R 31 | R 32 | R 33 | R 34 |
    +------+------+------+------+------+
    | R 40 | R 41 | R 42 | R 43 | R 44 |
    +------+------+------+------+------+
    Since D blocks are overlapping, it's desired to identify them ambiguously with the least necessary information given.
    Our function blockD() takes as an argument index of top-left R block and creates D block consisting of four R blocks. Meaning, for example:
    +------+------+------+------+------+   +------+------+------+------+------+   +------+------+------+------+------+
    |             | R 02 | R 03 | R 04 |   | R 00 | R 01 | R 02 | R 03 | R 04 |   | R 00 | R 01 | R 02 | R 03 | R 04 |
    +    D 00     +------+------+------+   +------+------+------+------+------+   +------+------+------+------+------+
    |             | R 12 | R 13 | R 14 |   | R 10 |             | R 13 | R 14 |   | R 10 | R 11 | R 12 | R 13 | R 14 |
    +------+------+------+------+------+   +------+    D 11     +------+------+   +------+------+------+------+------+
    | R 20 | R 21 | R 22 | R 23 | R 24 |   | R 20 |             | R 23 | R 24 |   | R 20 | R 21 | R 22 | R 23 | R 24 |
    +------+------+------+------+------+   +------+------+------+------+------+   +------+------+------+------+------+
    | R 30 | R 31 | R 32 | R 33 | R 34 |   | R 30 | R 31 | R 32 | R 33 | R 34 |   | R 30 | R 31 |             | R 34 
    +------+------+------+------+------+   +------+------+------+------+------+   +------+------+    D 32     +------+
    | R 40 | R 41 | R 42 | R 43 | R 44 |   | R 40 | R 41 | R 42 | R 43 | R 44 |   | R 40 | R 41 |             | R 44 |
    +------+------+------+------+------+   +------+------+------+------+------+   +------+------+------+------+------+
    and so on.
    That means that highest index can be (width-2,height-2)
    """

    # sets D block of size=2*blocksize and number [h,v] as defined above 
    def blockD(self, x, y, blocksize):
        x *= blocksize
        y *= blocksize
        crop1 = self[y:y+2*blocksize]
        crop2 = numpy.zeros(shape=(2*blocksize,2*blocksize))
        for index in range(2*blocksize):
            crop2[index] = (crop1[index])[x:x+2*blocksize]
        return crop2.view(R_block)

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
    
    

