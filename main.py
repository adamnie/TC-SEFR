"""
    main.py
    Examples of using img.py.
"""

from img import *                          # TO DO - fix importing class, returns type <img.img> instead of <img>


obraz = misc.lena()                        # importing image

image = obraz.view(img)                    # numpy way of subclassing...

print "Loaded image..."

image.printsize()

    
# Small blocks are RANGE: size blocksize x blocksize
# Big blocks are DOMAIN: size 2blocksize x 2blocksize

blocksize = 2
image.plot()

if (image.height()%(2*blocksize) != 0 or image.width()%(2*blocksize) != 0):   # Checking if our image can be divided into block without rest
    print "Wrong picture, cropping..."                                        # If not, cropping from down right corner
    image = image[1:len(image)-image.height()%(2*blocksize)]
    for line in image:
        line = line[1:len(image)-image.width()%(2*blocksize)]
    print "Cropped:",
    image.printsize()

print "Assuming size of small block (R) = " + str(blocksize)

print "We can have " + str(image.height()/blocksize) + "x" + str(image.width()/blocksize) + "=" + str( (image.height()/blocksize)*(image.width()/blocksize)) + " non-overlapping R blocks."

print "An example of R block: "
a = image.blockR(0,0, blocksize)
print a
a.plot()

print "We also can have " + str((image.height()/blocksize)-1) + "x" + str((image.width()/blocksize)-1) + "=" + str(((image.height()/blocksize)-1)*((image.width()/blocksize)-1)) + " overlapping D blocks."

print "An example of D block: "
b = image.blockD(0,0, blocksize)
print b
b.plot() 


