# quadranttest.py

from wm_img import *
import numpy as np

test = np.arange(64)
test = np.reshape(test, (8,8))
test = test.view(blockA)

#print test

"""
first = test.quadrant(0)
second = test.quadrant(1)
third = test.quadrant(2)
fourth = test.quadrant(3)

print "Quadrant", first.q
print first

print "Quadrant", second.q
print second

print "Quadrant", third.q
print third

print "Quadrant", fourth.q
print fourth
"""

no=3

testA = test.view(blockA)
testA = testA.quadrant(no)
print "Quadrant", testA.q, type(testA)
print testA
testA.set_mapper()
print "Mapper is", testA.mapper 
print


testB = test.view(blockB)
testB = testB.quadrant(no)
print "Quadrant", testB.q, type(testB)
print testB
testB.set_mapper()
print "Mapper is", testB.mapper 
print

testC = test.view(blockC)
testC = testC.quadrant(no)
print "Quadrant", testC.q, type(testC)
print testC
testC.set_mapper()
print "Mapper is", testC.mapper 
print