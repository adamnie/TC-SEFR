# wm_img.py
# class designed specially for algorithm provided in the article

from img import *
from fractal import *

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
    def __setattr__(self, what, value): # kurwa ale tu dojebalem magie
        self.__dict__[what] = value
        if what=="type":
            self.quadrant_attr[0]["mapper"]=self.mapper(0,value) 
            self.quadrant_attr[1]["mapper"]=self.mapper(1,value)
            self.quadrant_attr[2]["mapper"]=self.mapper(2,value)
            self.quadrant_attr[3]["mapper"]=self.mapper(3,value)

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
        return self.cutsquare(self.quadrant_attr[nr]["x"], self.quadrant_attr[nr]["y"], self.width()/2)

    # divides to non-overlapping blocks
    def divide(self, blocksize):
        max_row = self.how_many_D_in_a_row(blocksize,blocksize)+1
        max_column = self.how_many_D_in_a_column(blocksize,blocksize)+1
        indexes_list = [0]*max_row
        for y in range(0,max_row):
            indexes_list[y] = [0]*max_column
            for x in range(0,max_column):
                indexes_list[y][x] = {"y1": y*blocksize, "x1" : x*blocksize, "x2" : x*blocksize + blocksize, "y2" : y*blocksize + blocksize}
        return indexes_list # zwraca wspolrzedne pierwszego i "ostatniego" piksela (tak naprawde to jest to pierwszy piksel nastepnego bloku, ale Python tak specyficznie przetwarza indeksy, ze tak jest logiczniej)

    def get(self, list):
        crop1 = self[list["y1"]:list["y2"]] # przyciecie pozadanej ilosci wierszy tabeli, czyli przyciecie wertykalne (y)
        crop2 = np.zeros(shape=(list["y2"]-list["y1"],list["x2"]-list["x1"]))
        for index in range(size):
            crop2[index] = (crop1[index])[list["x1"]:list["x2"]]  #przyciecie pozadanej ilosci elementow w wierszu, czyli przyciecie horyzontalne (x)
        return crop2.view(wm_img)

    def save(self, what, lista):   # lista jest zbudowana ta samo jak slownik zwracany przez self.divide()
        for y in range(len(what)):
            for x in range(len(what[0])):
                self[lista['y1']+y][lista['x1']+x] = what[y][x] # zapisuje w samym sobie argument what w miejscu okreslonym przez 

class wspolczynniki:    # inicjalizacja kontenera na wspolczynniki
    list = [None] * 4
    czas = [None] * 4
