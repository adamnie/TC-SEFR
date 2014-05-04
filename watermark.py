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
from embed import *
import json                              # this one allows us to avoid long computation time while debugging: once computed, you can load it from file by setting boolean flag compress

compress = False                          # zmienna ustalajaca czy obliczamy kompresje czy ladujemy juz obliczona z pliku

quantization_table = numpy.matrix([[16, 11, 10, 16, 24, 40, 51, 61],
                                   [12, 13, 14, 19, 26, 58, 60, 55],
                                   [14, 13, 16, 24, 40, 57, 69, 56],
                                   [16, 17, 22, 29, 51, 87, 80, 62],
                                   [18, 22, 37, 56, 68, 109, 103, 77],
                                   [24, 35, 55, 64, 81, 104, 113, 92],
                                   [49, 64, 78, 87, 103, 121, 120, 101],
                                   [72, 92, 95, 98, 112, 100, 103, 99]]);

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
    nazwa = "wspolczynniki" + str(i) + "_new.json"
    if (not compress):  # ladowanie z pliku
        if i==0: 
          print "Loading previously calculated watermark data..."
        with open(nazwa, 'rb') as handle:
            wspolczynniki.list[i] = json.load(handle)
    else:
        json_file = open(nazwa, 'wb')               # kompresja
        start=time()
        mapper_nr=imageA.quadrant_attr[i]["mapper"]
        wspolczynniki.list[i] = fractal.compression(
           n, 
           imageA.quadrant(i), 
           imageA.quadrant(mapper_nr)
           )
        json.dump(wspolczynniki.list[i],json_file)
        json_file.close()

# teraz, obiekt wspolczynniki.list zawiera wszystkie wspolczynniki kodowania fraktalnego.
# odwolujemy sie do niego wspolczynniki.list[cwiartka bazowa][indeks y][indeks x]

imageB = wm_img(image.shiftup())                # nowy obraz przesuniety w gore
imageB.type = "B"
listB = imageB.divide(n)

reconstruct=[]

for y in range(len(listB)):
    for x in range(len(listB[0])):
        output = DCT.perform(imageB.get(listB[y][x])-128)
        # wykonuje DCT - UWAGA - zmienilem funkcje dct.perform(), tak, zeby nie zapisywala do listy a zwracala bezposrednio!
        output = np.divide(output,quantization_table).view(wm_img)
        imageB.view(wm_img).save(output,listB[y][x])                       # nadpisuje otrzymane wspolczynniki DCT na 

imageC = wm_img(image.shiftleft())
imageC.type = "C"
listC = imageC.divide(n)


for y in range(len(listC)):
    for x in range(len(listC[0])):
        output = DCT.perform(imageC.get(listC[y][x])-128) # 128 is offset required for DCT to work faster
        output = np.divide(output,quantization_table).view(wm_img)
        imageC.view(wm_img).save(output,listC[y][x])

wspolczynniki.list[0] # lista wspolczynnikow dopasowanych do cwiartki 0
# przypisuje je do blokow w diagonalnej cwiartce:
error_count = 0
good_count = 0

for q in range(4): #dla kazdej cwiartki
    mapper_nr=imageA.quadrant_attr[q]["mapper"] # znajduje jej cwiartke mapujaca
    fix = {"x" : imageA.quadrant_attr[mapper_nr]["x"], "y" : imageA.quadrant_attr[mapper_nr]["y"]}  # zapisuje piksele naprawiajace wspolrzedne 
    for i in range(len(listA)/2): 
        for j in range (len(listA)/2): #dla kazdego bloku
            B_coefficients = get_quantization_coefficients(imageB.get(listB[i][j]))
            C_coefficients = get_quantization_coefficients(imageC.get(listC[i][j]))

            block = wspolczynniki.list[q][i][j] # definiuje blok w macierzy wspolczynnikow
            mapping_block = {
              "y1": fix["y"] + block["y"] * n,
              "y2": fix["y"] + block["y"] * n+8,
              "x1":fix["x"] + block["x"] * n,
              "x2":fix["x"] + block["x"] * n+8,
            }

            block_to_be_watermarked = imageA.get(mapping_block)
            watermarked_block = embed_watermark(block_to_be_watermarked,block,B_coefficients,C_coefficients)
            watermarked_block = embed_checksum(watermarked_block)

            imageA.save(watermarked_block,mapping_block)

            #retrieving data

            ret_block = imageA.get(mapping_block)

            data = retrieve_watermark_and_checksum(ret_block)
            if errors_occured(ret_block,data):
              error_count += 1
            else:
              good_count += 1

print error_count
print good_count






