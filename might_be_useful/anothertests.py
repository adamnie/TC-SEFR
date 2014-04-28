import numpy as np
from img import *
from helpers import *
from wm_img import *
from fractal import *
from time import *
import pickle

fractal = fractal()
DCT = DCT()
image = fractal.open_img_PGM("pepper.pgm")
image.setflags(write=True)                 # bez tego nie chcialo sie zapisywac

n = 8

# replacing two LSB with zeros - preparing to saving information
for y in range(image.height()):
    for x in range(image.width()):
        image[y][x]=replacetwoLSB(image[y][x],0,0)   # zastepuje w kazdym pikselu dwa ostatnie bity zerami

imageA = wm_img(image)                      # inicjalizacja obiektu klasy wm_img
imageA.type = "A"                           # ustalanie typu obiektu, automatyczne obliczanie blokow mapujacych
listA = imageA.divide(n)                    # dzielenie na bloki n x n, zapisanie w tablicy INDEKSOW tych blokow (patrz wm_img.divide())

wspolczynniki = wspolczynniki()

compress = False                            # zmienna ustalajaca czy obliczamy kompresje czy ladujemy juz obliczona z pliku 

for i in range(4):
    if (not compress):  # ladowanie z pliku
        nazwa = "wspolczynniki" + str(i) + "_new.pickle"
        with open(nazwa, 'rb') as handle:
            wspolczynniki.list[i] = pickle.load(handle)
    else:               # kompresja
        start=time()
        mapper_nr=imageA.quadrant_attr[i]["mapper"]
        wspolczynniki.list[i] = fractal.compression(
           n, 
           imageA.quadrant(i), 
           imageA.quadrant(mapper_nr)
           )

    """
    Problem: fractal.compression() zwraca zle wspolczynniki blokow x i y. Nalezy to naprawic.
    """

        # naprawa wspolczynnikow ponizej - ale nie dziala. moze zaimplementowac to 
        # for x in range(len(wspolczynniki.list[i])):
        #     for y in range(len(wspolczynniki.list[i][x])):
        #         for z in range(len(wspolczynniki.list[i][x][y])):
        #             wspolczynniki.list[x][y][z]["x"]+=imageA.quadrant_attr[imageA.quadrant_attr[i]["mapper"]]["x"]
        #             wspolczynniki.list[x][y][z]["y"]+=imageA.quadrant_attr[imageA.quadrant_attr[i]["mapper"]]["y"]
        # nazwa = "wspolczynniki" + str(i) + "_new.pickle" 
        # with open(nazwa, 'wb') as handle:
        #      pickle.dump(wspolczynniki.list[i], handle)
        # wspolczynniki.czas[i]=time() - start
        # del start

imageB = wm_img(image.shiftup())                # nowy obraz przesuniety w gore
imageB.type = "B"
listB = imageB.divide(n)

for y in range(len(listB)):
    for x in range(len(listB[0])):
        output = DCT.perform(imageB.get(listB[y][x]))   # wykonuje DCT - UWAGA - zmienilem funkcje dct.perform(), tak, zeby nie zapisywala do listy a zwracala bezposrednio!
        imageB.save(output,listB[y][x])                 # nadpisuje otrzymane wspolczynniki DCT na 

imageC = wm_img(image.shiftleft())
imageC.type = "C"
listC = imageC.divide(n)


for y in range(len(listC)):
    for x in range(len(listC[0])):
        output = DCT.perform(imageC.get(listC[y][x]))
        imageC.save(output,listC[y][x])

wspolczynniki.list[0] # lista wspolczynnikow dopasowanych do cwiartki 0
# przypisuje je do blokow w diagonalnej cwiartce:

for q in range(4): #dla kazdej cwiartki
    fix = {"x" : imageA.quadrant_attr[q]["x"], "y" : imageA.quadrant_attr[q]["y"]}  # tutaj zapisuje piksele naprawiajace wspolrzedne 
    for i in range(len(listA)/2): 
        for j in range (len(listA)/2): #dla kazdego bloku

            # TUTAJ TRZEBA ZAMIENIC INFORMACJE NA BINARY, SKOMPRESOWAC

            block = wspolczynniki.list[q][i][j] # definiuje blok w macierzy wspolczynnikow
            mapping_block = [ fix["y"] + block["y"] * n , fix["x"] + block["x"] * n] # otrzymuje indeksy pierwszego piksela z bloku w ktorym musze zapisac informacje
            
            # TUTAJ ZA POMOCA FUNKCJI SAVE NALEZY ZAPISAC PO DWA BITY W KAZDYM PIKSELU            

