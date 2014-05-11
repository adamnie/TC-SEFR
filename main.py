"""
Main file:

Preparing the watermarked image:
1) open and convert image
2) calculate fractal data
3) embed fractal data into the image
4) save image

Authentication:
1) open image
2) retrive data
3) create correctness table and populate it with data (checksum)
4)

"""

import numpy as np
import json
import time

#my modules
from img_refurbished import *
from helpers_refurbished import *
from wm_img import *
from fractal_refurbished import *
from embed import *

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
DCT = DCT()

image = img('pepper.pgm')
image.setflags(write=True)

imageA = wm_img(image)
imageA.type = 'A'
listA = imageA.divide(R_block_size)

for i in range(4):
    nazwa = "wspolczynniki" + str(i) + "_new.json"
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

blocks_in_quad = len(listA)/2

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

      B_coefficients = get_quantization_coefficients(imageB.get_block(listB[i_quad][j_quad]))
      C_coefficients = get_quantization_coefficients(imageC.get_block(listC[i_quad][j_quad]))

      compression_data = fractal.coefficients[quadrant][i][j]

      block = imageA.get_block(compression_data)

      watermarked_block = embed_watermark(block,compression_data,B_coefficients,C_coefficients) 
      watermarked_block = embed_checksum(watermarked_block)

      imageA.save_block(watermarked_block,{'x':i_quad,'y':j_quad})

# imageA.plot() 
ret_comp_data = []

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

      block = imageA.get_block({'x':i_quad,'y':j_quad})
      ret_comp_data[quadrant][i][j].append(retrieve_watermark_and_checksum(block))
      print ret_comp_data[quadrant][i][j]
      if errors_occured(block,ret_comp_data[quadrant][i][j][0][3]):
        checksum_is_correct[i_quad][j_quad] = 1
      else:
        checksum_is_correct[i_quad][j_quad] = -1 

print checksum_is_correct      

# checking a blocks info
for quadrant in range(4):
  mapper_q = imageA.quadrant_attr[quadrant]['mapper']
  mapper_offset = {'x': imageA.quadrant_attr[mapper_q]['x'], 'y': imageA.quadrant_attr[mapper_q]['y'] } 
  quadrant_offset = {'x': imageA.quadrant_attr[quadrant]['x'], 'y': imageA.quadrant_attr[quadrant]['y'] }

  for i in range(blocks_in_quad):
    for j in range(blocks_in_quad):

      i_quad = i + quadrant_offset['x'] / R_block_size
      j_quad = j + quadrant_offset['y'] / R_block_size

      block = imageA.get_block({'x':i_quad,'y':j_quad})

      comp_data = retrieve_watermark_and_checksum(block)

      comp_data[0]['x'] += mapper_offset['x']
      comp_data[0]['y'] += mapper_offset['y']

      comp_data[0]['x'] /= R_block_size
      comp_data[0]['y'] /= R_block_size

      if checksum_is_correct[i_quad][j_quad] and checksum_is_correct[comp_data[0]['x']][comp_data[0]['y']]:
        mapping_block = imageA.get_block(comp_data[0])
        recalculated_data = compare(block,mapping_block)

        if recalculated_data['o'] == comp_data[0]['o'] and recalculated_data['s'] == comp_data[0]['s']:
          A_type_is_ok[i_quad][j_quad] = 1
        else:
          A_type_is_ok[i_quad][j_quad] = -1

      else:
          A_type_is_ok[i_quad][j_quad] = 0
# checking B and C blocks info
for quadrant in range(4):
  mapper_q = imageA.quadrant_attr[quadrant]['mapper']
  mapper_offset = {'x': imageA.quadrant_attr[mapper_q]['x'], 'y': imageA.quadrant_attr[mapper_q]['y'] } 
  quadrant_offset = {'x': imageA.quadrant_attr[quadrant]['x'], 'y': imageA.quadrant_attr[quadrant]['y'] }

  for i in range(blocks_in_quad):
    for j in range(blocks_in_quad):
      B_correct = True
      C_correct = True

      i_quad = i + quadrant_offset['x'] / R_block_size
      j_quad = j + quadrant_offset['y'] / R_block_size

      blockA = imageA.get_block({'x':i_quad,'y':j_quad})
      blockB = imageB.get_block({'x':i_quad,'y':j_quad})
      blockC = imageC.get_block({'x':i_quad,'y':j_quad})

      data = retrieve_watermark_and_checksum(blockA)

      B_dct_coef = get_quantization_coefficients(DCT.perform(blockB-128))
      C_dct_coef = get_quantization_coefficients(DCT.perform(blockC-128))

      for i in range(6):
        if B_dct_coef[i] != data[1][i]:
          B_correct = False
        if C_dct_coef[i] != data[2][i]:
          C_correct = False

      if B_correct:
        B_type_is_ok[i_quad][j_quad] = 1
      else: 
        B_type_is_ok[i_quad][j_quad] = -1

      if C_correct:
        C_type_is_ok[i_quad][j_quad] = 1
      else: 
        C_type_is_ok[i_quad][j_quad] = -1


## Adding all detections data to decide whether block is damaged or not
# weights
w_check = 1
# weights in deciding whethere img was damaged
w_A = 1
w_B = 1
w_C = 1
#weights for reconstruction
weight_A = np.zeros([len(listA),len(listA)])
weight_B = np.zeros([len(listB),len(listB)])
weight_C = np.zeros([len(listC),len(listC)])

detection = w_check*checksum_is_correct + w_A*A_type_is_ok + w_B*B_type_is_ok + w_C*C_type_is_ok

# reconstruction prep

for quadrant in range(4):
  mapper_q = imageA.quadrant_attr[quadrant]['mapper']
  mapper_offset = {'x': imageA.quadrant_attr[mapper_q]['x'], 'y': imageA.quadrant_attr[mapper_q]['y'] } 
  quadrant_offset = {'x': imageA.quadrant_attr[quadrant]['x'], 'y': imageA.quadrant_attr[quadrant]['y'] }

  for i in range(blocks_in_quad):
    for j in range(blocks_in_quad):
      coords = {}
      i_quad = i + quadrant_offset['x'] / R_block_size
      j_quad = j + quadrant_offset['y'] / R_block_size 
      coords['x'] = i_quad
      coords['y'] = j_quad     

      if detection[i_quad][j_quad] > 0:
        print "block is ok proceeding..."
      else:
        print "block may be damaged, reconstruction started ..."

        if A_type_is_ok[i_quad][j_quad]:
          weight_A[i_quad][j_quad] = 1
          block_A_rec = reconstruct.fromA()
          imageA.save_block(block_A_rec,coords)
        elif B_type_is_ok[i_quad][j_quad]:
          weight_B[i_quad][j_quad] = 1
          block_B_rec = reconstruct.fromB()
          imageB.save_block(block_B_rec,coords)
        elif C_type_is_ok[i_quad][j_quad]:
          weight_C[i_quad][j_quad] = 1
          block_C_rec = reconstruct.fromC()
          imageC.save_block(block_C_rec,coords)

