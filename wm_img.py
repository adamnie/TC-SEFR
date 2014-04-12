# wm_img.py
# class designed specially for algorithm provided in the article

from img import *

size = 8  #as for 8x8 blocks

class wm_img(img):
    # zmienna q przechowuje wartosc informujaca o quadrancie: 0-3 odpowiada odpowiedniej cwiartce, -1 znaczy, ze nie jest zadna cwiartka
    q = -1  
    def block(self, x, y,size=8):   # NON-OVERLAPPING blocks
        sth = self.cutsquare(x*size,y*size,size).view(wm_img)
        return sth
    def quadrant(self, which): # wycinam cwiartki z bloku 8x8
        tp = type(self)
        if (which == 0):
            ret = self.cutsquare(self.width()/2, 0, self.width()/2).view(tp) # WAZNE: zwracam w takim samym typie jakim otrzymalem czyli nie wm_img ale np. blockA...
            ret.q = 0
            return ret
        elif (which == 1):
            ret = self.cutsquare(self.width()/2, self.height()/2, self.width()/2).view(tp) 
            ret.q = 1
            return ret
        elif (which == 2):
            ret = self.cutsquare(0, self.height()/2, self.height()/2).view(tp)
            ret.q = 2
            return ret
        elif (which == 3):
            ret = self.cutsquare(0, 0, self.height()/2).view(tp)
            ret.q = 3
            return ret
        else:
            return "Ogarnij sie" # TO DO: error handling...

# funkcja set_mapper() potrzebna jest do wyliczenia numery mapujacego quadranta w tym blocku
# poki co trzeba ja wywolywac zaraz po subklasowaniu lub zaraz przed checia skorzystania ze zmiennej mapper
# mapper mozna wywolywac tylko na istniejacym obiekcie!!! nie mozna "w locie"!
# tzn: 
#    a0 = imageA.quadrant(0)
#    a0.set_mapper()
#    print a0.mapper
# OK!
# ale to juz zle:
#    imageA.quadrant(0).set_mapper() - obiekt ginie w pamieci
#    print imageA.quadrant(0).mapper - error, nie ma zdefiniowanego mappera
#
# TODO: prawdopodobie mozna to wlozyc w jakis __init__ czy inny __new__

# klasy dla kazdego rodzaju blokow
# daleko do optymalizacji...

class blockA(wm_img):
    def set_mapper(self):
        self.mapper = (self.q + 2) % 4
class blockB(wm_img):
    def set_mapper(self):
        self.mapper = (self.q + 1) % 4
class blockC(wm_img):
    def set_mapper(self):
        self.mapper = (self.q + 3) % 4
