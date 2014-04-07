"""
    main.py
    Examples of using img.py.
"""

from img import *                          # TO DO - fix importing class, returns type <img.img> instead of <img>


obraz = misc.lena()                        # importing image

image = obraz.view(img)                    # numpy way of subclassing...

print "Loaded image..."

image.printsize()

    
# Small blocks are size blocksize x blocksize
# Big blocks are size 2blocksize x 2blocksize

blocksize = 4
image.plot()

if (image.height()%(2*blocksize) != 0 or image.width()%(2*blocksize) != 0):   # Checking if our image can be divided into block without rest
    print "Wrong picture, cropping..."                                        # If not, cropping from down right corner
    image = image[1:len(image)-image.height()%(2*blocksize)]
    for line in image:
        line = line[1:len(image)-image.width()%(2*blocksize)]
    print "Cropped:",
    image.printsize()

print "Assuming size of big block (D) = " + str(blocksize)

print "We have " + str(image.height()/blocksize) + "x" + str(image.width()/blocksize) + "=" + str( (image.height()/blocksize)*(image.width()/blocksize)) + " D blocks."

print "An example of D block: "
a = image.blockD(64,64, blocksize)
print a
a.plot()


