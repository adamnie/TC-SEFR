"""
    watermark.py
    A tale about understanding Chinese customs and articles.

    Possibly there are problems with indexing... it's hard for me to remember which axis is x and which is y. I'm not that clever, you know.
    So, for now, I take no responsibility for some fancy-shaped images. Square is just fine.

"""

"""
Phase 0: INTRO
First, we have to import all necessary files.
"""

import numpy as np
from img import *
from helpers import *
from wm_img import *
from fractal import *
from time import *
import pickle                              # this one allows us to avoid long computation time while debugging: once computed, you can load it from file by setting boolean flag compress

compress = False                            # zmienna ustalajaca czy obliczamy kompresje czy ladujemy juz obliczona z pliku

"""
Phase 1: WELCOME TO THE JUNGLE
We are kindly importing our guest and inviting him to play. But, we have to set the rules of game, so there will be no cheating.
"""
fractal = fractal()                        # inviting out invisible friends to join us
DCT = DCT()
wspolczynniki = wspolczynniki()          

image = fractal.open_img_PGM("pepper.pgm") # hello
image.setflags(write=True)                 # flag needed to write to file 

n = 8                                      # we are setting our block to 8x8 size. other sizes are not tested... YET

# replacing two LSB with zeros - preparing to saving information
for y in range(image.height()):
    for x in range(image.width()):
        image[y][x]=replacetwoLSB(image[y][x],0,0)

"""
Phase 2: LET'S GET IT STARTED
Suddenly, out of nowhere, we are starting our game.
"""

imageA = wm_img(image)                      # inicjalizacja obiektu klasy wm_img
imageA.type = "A"                           # ustalanie typu obiektu, automatyczne obliczanie blokow mapujacych
listA = imageA.divide(n)                    # dzielenie na bloki n x n, zapisanie w tablicy INDEKSOW tych blokow (patrz wm_img.divide())   

for i in range(4):
    if (not compress):  # ladowanie z pliku
        if i==0: print "Loading previously calculated watermark data..."
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

# teraz, obiekt wspolczynniki.list zawiera wszystkie wspolczynniki kodowania fraktalnego.
# odwolujemy sie do niego wspolczynniki.list[cwiartka bazowa][indeks y][indeks x]

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
    mapper_nr=imageA.quadrant_attr[q]["mapper"] # znajduje jej cwiartke mapujaca
    fix = {"x" : imageA.quadrant_attr[mapper_nr]["x"], "y" : imageA.quadrant_attr[mapper_nr]["y"]}  # zapisuje piksele naprawiajace wspolrzedne 
    for i in range(len(listA)/2): 
        for j in range (len(listA)/2): #dla kazdego bloku

            # TUTAJ TRZEBA ZAMIENIC INFORMACJE NA BINARY, SKOMPRESOWAC

            block = wspolczynniki.list[q][i][j] # definiuje blok w macierzy wspolczynnikow
            mapping_block = [ fix["y"] + block["y"] * n , fix["x"] + block["x"] * n] # otrzymuje indeksy pierwszego piksela z bloku w ktorym musze zapisac informacje
            
            # TUTAJ ZA POMOCA FUNKCJI SAVE NALEZY ZAPISAC PO DWA BITY W KAZDYM PIKSELU            

