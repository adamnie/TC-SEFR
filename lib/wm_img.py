# wm_img.py
# class designed specially for algorithm provided in the article

from lib.img import *
from lib.fractal import *
import math

size = 8  #as for 8x8 blocks

class wm_img(img):
    # definiuje klase dziedziczaca po img, ale posiadajaca dodatkowe atrybuty
    # cala ta kombinacja po to, zeby operowac bezposrednio na obrazie, a nie na jakichs jego kopiach

    def __new__(cls, img):     
        obj = img.view(cls)
        obj.quadrant_attr = [
        {"nr" : 0, "x" : img.width()/2, "y" : 0},
        {"nr" : 1, "x" : img.width()/2, "y" : img.height()/2}, 
        {"nr" : 2, "x" : 0, "y" : img.height()/2},
        {"nr" : 3, "x" : 0, "y" : 0}]
        return obj

    def __init__(self, img):
        pass        

    # w momencie inicjalizacji typu obiektu wm_img obliczany jest odpowiadajacy mapper
    def __setattr__(self, what, type): # kurwa ale tu dojebalem magie
        self.__dict__[what] = type
        if what=="type":
            self.quadrant_attr[0]["mapper"]=self.mapper(0,type) 
            self.quadrant_attr[1]["mapper"]=self.mapper(1,type)
            self.quadrant_attr[2]["mapper"]=self.mapper(2,type)
            self.quadrant_attr[3]["mapper"]=self.mapper(3,type)

    def block(self, x, y,size=8):   # NON-OVERLAPPING blocks
        sth = self.cutsquare(x*size,y*size,size).view(wm_img)
        return sth

    def mapper(self, nr, typ):
        if typ == "A":
            return (nr + 2) % 4
        elif typ == "B":
            return (nr + 1) % 4
        elif typ == "C":
            return (nr + 3) % 4
        else:
            return "Mapping error"

    # returns current state of wanted quadrant
    def quadrant(self, nr):
        return self.cut_block(self.quadrant_attr[nr]["x"], self.quadrant_attr[nr]["y"], self.width()/2)

    # divides to non-overlapping blocks
    def divide(self, block_size=8):
        max_row = self.how_many_D_in_a_row(block_size,block_size)+1
        max_column = self.how_many_D_in_a_column(block_size,block_size)+1
        indexes_list = [0]*max_row
        for y in range(0,max_row):
            indexes_list[y] = [0]*max_column
            for x in range(0,max_column):
                indexes_list[y][x] = {"y": y*block_size, "x" : x*block_size}
        return indexes_list # zwraca wspolrzedne pierwszego i "ostatniego" piksela (tak naprawde to jest to pierwszy piksel nastepnego bloku, ale Python tak specyficznie przetwarza indeksy, ze tak jest logiczniej)
