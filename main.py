
import numpy as np
import json
import time

#my modules
from lib.img import *
from lib.helpers import *
from lib.wm_img import *
from lib.fractal import *
from lib.embed import *
from lib.reconstruct import *

calculate = False # decide whether to calculate or load data
R_block_size = 8

quantization_table = np.matrix([[16, 11, 10, 16, 24, 40, 51, 61],
                                   [12, 13, 14, 19, 26, 58, 60, 55],
                                   [14, 13, 16, 24, 40, 57, 69, 56],
                                   [16, 17, 22, 29, 51, 87, 80, 62],
                                   [18, 22, 37, 56, 68, 109, 103, 77],
                                   [24, 35, 55, 64, 81, 104, 113, 92],
                                   [49, 64, 78, 87, 103, 121, 120, 101],
                                   [72, 92, 95, 98, 112, 100, 103, 99]]);

# initializing objects
fractal = fractal()
reconstruct = reconstruct()
DCT = DCT()

image = img('./pictures/scarlett.pgm')
image.setflags(write=True)

imageA = wm_img(image)
imageA.type = 'A'
listA = imageA.divide(R_block_size)

for i in range(4):
    nazwa = "./precalculated_files/wspolczynniki_"+ image.name + "_" + str(i) + "_new.json"
    if (not calculate):  # ladowanie z pliku
        if i==0: 
          print "Loading previously calculated watermark data..."
        with open(nazwa, 'rb') as handle:
            fractal.coefficients[i] = json.load(handle)
    else:
        json_file = open(nazwa, 'wb')               # kompresja
        mapper_nr=imageA.quadrant_attr[i]["mapper"]
        fractal.coefficients[i] = fractal.compression(
           R_block_size, 
           imageA.quadrant(i), 
           imageA.quadrant(mapper_nr)
           )
        json.dump(fractal.coefficients[i],json_file)
        json_file.close()

imageB = wm_img(image.shift_up())                # nowy obraz przesuniety w gore
imageB.type = "B"
listB = imageB.divide(R_block_size)
# performing dct on B type blocks
for y in range(len(listB)):
    for x in range(len(listB[0])):
        output = DCT.perform(imageB.get_block(listB[x][y])-128)
        # wykonuje DCT - UWAGA - zmienilem funkcje dct.perform(), tak, zeby nie zapisywala do listy a zwracala bezposrednio!
        output = np.divide(output,quantization_table).view(wm_img)
        imageB.view(wm_img).save_block(output,listB[x][y])                       # nadpisuje otrzymane fractal.coefficients DCT na 

imageC = wm_img(image.shift_left())
imageC.type = "C"
listC = imageC.divide(R_block_size)
# performing dct on C type blocks
for x in range(len(listC)):
    for y in range(len(listC[0])):
        output = DCT.perform(imageC.get_block(listC[x][y])-128) # 128 is offset required for DCT to work faster
        output = np.divide(output,quantization_table).view(wm_img)
        imageC.view(wm_img).save_block(output,listC[x][y])

# imageA.plot() 
# imageB.plot()
# imageC.plot()     

checksum_is_correct = np.zeros([len(listA),len(listA)])

A_type_is_ok = np.zeros([len(listA),len(listA)])
B_type_is_ok = np.zeros([len(listB),len(listB)])
C_type_is_ok = np.zeros([len(listC),len(listC)])

correctnes_table = np.zeros([len(listA),len(listA)])

blocks_in_quad = len(listA)/2

B_first = []
#saving compression data in the image
print "Start embedding..."
for quadrant in range(4):
  mapper_q = imageA.quadrant_attr[quadrant]['mapper']
  mapper_offset = {'x': imageA.quadrant_attr[mapper_q]['x'], 'y': imageA.quadrant_attr[mapper_q]['y'] } 
  quadrant_offset = {'x': imageA.quadrant_attr[quadrant]['x'], 'y': imageA.quadrant_attr[quadrant]['y'] }
  
  for i in range(blocks_in_quad):
    for j in range(blocks_in_quad):

      i_quad = i + quadrant_offset['x'] / R_block_size
      j_quad = j + quadrant_offset['y'] / R_block_size

      x = i * R_block_size + quadrant_offset['x']
      y = j * R_block_size + quadrant_offset['y']

      B_coefficients = get_quantization_coefficients(imageB.get_block(coords={'x':x,'y':y}))
      C_coefficients = get_quantization_coefficients(imageC.get_block(coords={'x':x,'y':y}))

      # converting to int
      B_coefficients = [int(coef) for coef in B_coefficients]
      C_coefficients = [int(coef) for coef in C_coefficients]
      B_first.append(B_coefficients)
      compression_data = fractal.coefficients[quadrant][i][j]

      block = imageA.get_block(coords={'x':x,'y':y})

      watermarked_block = embed_watermark(block,compression_data,B_coefficients,C_coefficients) 
      watermarked_block = embed_checksum(watermarked_block)

      imageA.save_block(watermarked_block,{'x':x,'y':y})

print "Embedding finished. "

# damaging blocks
imageA.save_block(np.zeros((50,50)),{'x':0,'y':0})
imageA.plot()
# data, that may be used to reconstruct image
ret_comp_data = []

# checking correctnes of checksum
print "Start checking data ..."
for quadrant in range(4):
  mapper_q = imageA.quadrant_attr[quadrant]['mapper']
  mapper_offset = {'x': imageA.quadrant_attr[mapper_q]['x'], 'y': imageA.quadrant_attr[mapper_q]['y'] } 
  quadrant_offset = {'x': imageA.quadrant_attr[quadrant]['x'], 'y': imageA.quadrant_attr[quadrant]['y'] }
  ret_comp_data.append([])
  for i in range(blocks_in_quad):
    ret_comp_data[quadrant].append([])
    for j in range(blocks_in_quad):  
      ret_comp_data[quadrant][i].append([])
      i_quad = i + quadrant_offset['x'] / R_block_size
      j_quad = j + quadrant_offset['y'] / R_block_size

      x = i * R_block_size + quadrant_offset['x']
      y = j * R_block_size + quadrant_offset['y']

      block = imageA.get_block({'x':x,'y':y})
      ret_comp_data[quadrant][i][j].append(retrieve_watermark_and_checksum(block))
      if errors_occured(block,ret_comp_data[quadrant][i][j][0][3]):
        checksum_is_correct[i_quad][j_quad] = -1
      else:
        checksum_is_correct[i_quad][j_quad] = 1

# checking correctness of B blocks info 
for quadrant in range(4):
  mapper_q = imageB.quadrant_attr[quadrant]['mapper']
  mapper_offset = {'x': imageB.quadrant_attr[mapper_q]['x'], 'y': imageB.quadrant_attr[mapper_q]['y'] } 
  quadrant_offset = {'x': imageB.quadrant_attr[quadrant]['x'], 'y': imageB.quadrant_attr[quadrant]['y'] }
  for i in range(blocks_in_quad):
    for j in range(blocks_in_quad):    
      B_correct = True

      i_quad = i + quadrant_offset['x'] / R_block_size
      j_quad = j + quadrant_offset['y'] / R_block_size

      x = i * R_block_size + quadrant_offset['x']
      y = j * R_block_size + quadrant_offset['y']

      blockA = imageA.get_block({'x':x,'y':y})
      blockB = imageB.get_block({'x':x,'y':y})

      data = retrieve_watermark_and_checksum(blockA)

      B_recalculated = get_quantization_coefficients(blockB)

      for k in range(6):
        if B_recalculated[k] != data[1][k]:
          B_correct = False

      if B_correct:
        B_type_is_ok[i_quad][j_quad] = 1
      else: 
        B_type_is_ok[i_quad][j_quad] = -1   

for quadrant in range(4):
  mapper_q = imageC.quadrant_attr[quadrant]['mapper']
  mapper_offset = {'x': imageC.quadrant_attr[mapper_q]['x'], 'y': imageC.quadrant_attr[mapper_q]['y'] } 
  quadrant_offset = {'x': imageC.quadrant_attr[quadrant]['x'], 'y': imageC.quadrant_attr[quadrant]['y'] }
  for i in range(blocks_in_quad):
    for j in range(blocks_in_quad):    
      C_correct = True

      i_quad = i + quadrant_offset['x'] / R_block_size
      j_quad = j + quadrant_offset['y'] / R_block_size

      x = i * R_block_size + quadrant_offset['x']
      y = j * R_block_size + quadrant_offset['y']

      blockA = imageA.get_block({'x':x,'y':y})
      blockC = imageC.get_block({'x':x,'y':y})

      data = retrieve_watermark_and_checksum(blockA)

      C_recalculated = get_quantization_coefficients(blockC)

      for k in range(6):
        if C_recalculated[k] != data[2][k]:
          C_correct = False

      if C_correct:
        C_type_is_ok[i_quad][j_quad] = 1
      else: 
        C_type_is_ok[i_quad][j_quad] = -1 

correctness_table = checksum_is_correct + B_type_is_ok + C_type_is_ok
# A reconstruction
for quadrant in range(4):
  mapper_q = imageA.quadrant_attr[quadrant]['mapper']
  mapper_offset = {'x': imageA.quadrant_attr[mapper_q]['x'], 'y': imageA.quadrant_attr[mapper_q]['y'] } 
  quadrant_offset = {'x': imageA.quadrant_attr[quadrant]['x'], 'y': imageA.quadrant_attr[quadrant]['y'] }
  for i in range(blocks_in_quad):
    for j in range(blocks_in_quad): 

      i_quad = i + quadrant_offset['x'] / R_block_size
      j_quad = j + quadrant_offset['y'] / R_block_size

      x = i * R_block_size + quadrant_offset['x']
      y = j * R_block_size + quadrant_offset['y']

      if correctness_table[i_quad][j_quad] < 0:
        blockA = imageA.get_block({'x':x,'y':y})
        data = retrieve_watermark_and_checksum(blockA)
        x_base = data[0]['x'] + mapper_offset['x']
        y_base = data[0]['y'] + mapper_offset['y']

        base_block = imageA.get_block({'x': x_base,'y':y_base})
        reconstructed_block = reconstruct.fromA(base_block,data[0],R_block_size)
        imageA.save_block(reconstructed_block,{'x':x,'y': y})

# B reconstruction


print correctness_table
imageA.plot()

