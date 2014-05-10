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
from img_refurbished import *
from helpers_refurbished import *
from wm_img import *
from fractal_refurbished import *
from time import *
from embed import *
import json                              # this one allows us to avoid long computation time while debugging: once computed, you can load it from file by setting boolean flag compress

compress = True                          # zmienna ustalajaca czy obliczamy kompresje czy ladujemy juz obliczona z pliku

quantization_table = np.matrix([[16, 11, 10, 16, 24, 40, 51, 61],
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

image = img("pepper.pgm") # hello
image.setflags(write=True)                 # flag needed to write to file 

n = 8                                      # we are setting our block to 8x8 size. other sizes are not tested... YET

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
            fractal.coefficients.list[i] = json.load(handle)
    else:
        json_file = open(nazwa, 'wb')               # kompresja
        start=time()
        mapper_nr=imageA.quadrant_attr[i]["mapper"]
        fractal.coefficients.list[i] = fractal.compression(
           n, 
           imageA.quadrant(i), 
           imageA.quadrant(mapper_nr)
           )
        json.dump(fractal.coefficients.list[i],json_file)
        json_file.close()

# teraz, obiekt fractal.coefficients.list zawiera wszystkie fractal.coefficients kodowania fraktalnego.
# odwolujemy sie do niego fractal.coefficients.list[cwiartka bazowa][indeks y][indeks x]

imageB = wm_img(image.shift_up())                # nowy obraz przesuniety w gore
imageB.type = "B"
listB = imageB.divide(n)

reconstruct=[]

for y in range(len(listB)):
    for x in range(len(listB[0])):
        output = DCT.perform(imageB.get(listB[y][x])-128)
        # wykonuje DCT - UWAGA - zmienilem funkcje dct.perform(), tak, zeby nie zapisywala do listy a zwracala bezposrednio!
        output = np.divide(output,quantization_table).view(wm_img)
        imageB.view(wm_img).save_block(output,listB[y][x])                       # nadpisuje otrzymane fractal.coefficients DCT na 

imageC = wm_img(image.shift_left())
imageC.type = "C"
listC = imageC.divide(n)


for y in range(len(listC)):
    for x in range(len(listC[0])):
        output = DCT.perform(imageC.get(listC[y][x])-128) # 128 is offset required for DCT to work faster
        output = np.divide(output,quantization_table).view(wm_img)
        imageC.view(wm_img).save_block(output,listC[y][x])

fractal.coefficients.list[0] # lista wspolczynnikow dopasowanych do cwiartki 0
# przypisuje je do blokow w diagonalnej cwiartce:

A_size = len(listA)
block_is_correct = np.zeros([A_size,A_size])
size = 8
for q in range(4): #dla kazdej cwiartki
    mapper_nr=imageA.quadrant_attr[q]["mapper"] # znajduje jej cwiartke mapujaca
    img_offset = {"x" : imageA.quadrant_attr[mapper_nr]["x"]/size, "y" : imageA.quadrant_attr[mapper_nr]["y"]/size}  # zapisuje piksele naprawiajace wspolrzedne 
    for i in range(len(listA)/2): 
        for j in range (len(listA)/2): #dla kazdego bloku
            B_coefficients = get_quantization_coefficients(imageB.get(listB[i][j]))
            C_coefficients = get_quantization_coefficients(imageC.get(listC[i][j]))

            block_coords = fractal.coefficients.list[q][i][j] # definiuje blok w macierzy wspolczynnikow

            block_to_be_watermarked = imageA.get_block(block_coords)
            watermarked_block = embed_watermark(block_to_be_watermarked,block_coords,B_coefficients,C_coefficients)
            watermarked_block = embed_checksum(watermarked_block)


            offset_block_coords = block_coords
            offset_block_coords['x'] += img_offset['x']
            offset_block_coords['y'] += img_offset['y']

            imageA.save(watermarked_block,offset_block_coords)

"""
There is an issue with reriving cheksum, but probably not with the indexing,
becuase in deciding whether both blocks are ok, everything went well

"""
# populating correctness_list

for q in range(4): #dla kazdej cwiartki
  mapper_nr=imageA.quadrant_attr[q]["mapper"] # znajduje jej cwiartke mapujaca
  img_offset = {"x" : imageA.quadrant_attr[mapper_nr]["x"]/size, "y" : imageA.quadrant_attr[mapper_nr]["y"]/size}  # zapisuje piksele naprawiajace wspolrzedne 
  for i in range(len(listA)/2): 
    for j in range (len(listA)/2): #dla kazdego bloku

      block_coords = fractal.coefficients.list[q][i][j]
      offset_block_coords['x'] += img_offset['x']
      offset_block_coords['y'] += img_offset['y']
      print "====================="
      print offset_block_coords['x']
      print offset_block_coords['y']

      ret_block = imageA.get_block(offset_block_coords)
      data = retrieve_watermark_and_checksum(ret_block)

      offset_i = i+img_offset['y']
      offset_j = j+img_offset['x']

      if errors_occured(ret_block,data[3]):
        block_is_correct[offset_i][offset_j] = -1
      else:
        block_is_correct[offset_i][offset_j] = 1


print block_is_correct
# extracting fractal data  and calculating new and comparing
for q in range(4): #dla kazdej cwiartki
  mapper_nr=imageA.quadrant_attr[q]["mapper"] # znajduje jej cwiartke mapujaca
  img_offset = {"x" : imageA.quadrant_attr[mapper_nr]["x"]/size, "y" : imageA.quadrant_attr[mapper_nr]["y"]/size}  # zapisuje piksele naprawiajace wspolrzedne 
  for i in range(len(listA)/2): 
    for j in range (len(listA)/2): #dla kazdego bloku
      block_coords = fractal.coefficients.list[q][i][j]
      offset_block_coords = block_coords
      offset_block_coords['x'] += img_offset['x']
      offset_block_coords['y'] += img_offset['y']

      offset_i = i+img_offset['y']
      offset_j = j+img_offset['x']

      this_block = {'x' : offset_j, 'y':offset_i}

      if block_is_correct[offset_i][offset_j]: 
      # and block_is_correct[block_coords['y']][block_coords['x']]:
        block1 = imageA.get_block(block_coords)
        block2 = imageA.get_block(this_block)

        # trans_data = fractal.compare(block2, block1)

        # if trans_data['s'] == block_coords['s']:
          # print "wow wow it works"          

      else:

        print "Something went wrong"



