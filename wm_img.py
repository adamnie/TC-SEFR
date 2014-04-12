# wm_img.py
# class designed specially for algorithm provided in the article

from img import *

size = 8  #as for 8x8 blocks

class wm_img(img):
    q = -1
    def block(self, x, y):   # NON-OVERLAPPING
        sth = self.cutsquare(x*size,y*size,size).view(wm_img)
        return sth
    def quadrant(self, which):
        tp = type(self)
        if (which == 0):
            ret = self.cutsquare(size/2, 0, size/2).view(tp) #zwracam w takim samym typie jakim otrzymalem czyli nie wm_img ale blockA...
            ret.q = 0
            return ret
        elif (which == 1):
            ret = self.cutsquare(size/2, size/2, size/2).view(tp)
            ret.q = 1
            return ret
        elif (which == 2):
            ret = self.cutsquare(0, size/2, size/2).view(tp)
            ret.q = 2
            return ret
        elif (which == 3):
            ret = self.cutsquare(0, 0, size/2).view(tp)
            ret.q = 3
            return ret
        else:
            return "Ogarnij sie"

class blockA(wm_img):
    def set_mapper(self):
        self.mapper = (self.q + 2) % 4
class blockB(wm_img):
    def set_mapper(self):
        self.mapper = (self.q + 1) % 4
class blockC(wm_img):
    def set_mapper(self):
        self.mapper = (self.q + 3) % 4
class blockD(wm_img):
    pass