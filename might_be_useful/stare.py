"""
    stare.py
    Examples of using img.py.
"""

from img import *               

obraz = misc.lena()                        # importing image

image = obraz.view(img)                    # numpy way of subclassing...

print "Loaded image..."

image.printsize()

Rsize = 4

   
# Small blocks are RANGE: size Rsize x Rsize
# Big blocks are DOMAIN: size 2Rsize x 2Rsize


image.plot()

image.checksize(Rsize)

print "Assuming size of small block (R) = " + str(Rsize)

print "We can have " + str(image.height()/Rsize) + "x" + str(image.width()/Rsize) + "=" + str( (image.height()/Rsize)*(image.width()/Rsize)) + " non-overlapping R blocks."

print "An example of R block: "
a = image.blockR(0,0,Rsize)
print a
a.plot()

print "We also can have " + str((image.height()/Rsize)-1) + "x" + str((image.width()/Rsize)-1) + "=" + str(((image.height()/Rsize)-1)*((image.width()/Rsize)-1)) + " overlapping D blocks."

print "An example of D block: "
b = image.blockD(0,0,Rsize)
print b
b.plot()

busr = b.meanbyfour(Rsize)
print busr
busr.plot()
