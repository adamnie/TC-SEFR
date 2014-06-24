
import numpy as np
import json
import time
import sys

#my modules
from lib.img import *
from lib.helpers import *
from lib.wm_img import *
from lib.fractal import *
from lib.embed import *
from lib.reconstruct import *
from lib.dct import *

quantization_table = np.matrix([[16, 11, 10, 16, 24, 40, 51, 61],
                                   [12, 13, 14, 19, 26, 58, 60, 55],
                                   [14, 13, 16, 24, 40, 57, 69, 56],
                                   [16, 17, 22, 29, 51, 87, 80, 62],
                                   [18, 22, 37, 56, 68, 109, 103, 77],
                                   [24, 35, 55, 64, 81, 104, 113, 92],
                                   [49, 64, 78, 87, 103, 121, 120, 101],
                                   [72, 92, 95, 98, 112, 100, 103, 99]]);

def perform_compression(image, R_block_size, calculate_flg, delta, E_threshold, dct_threshold,filename):

  ## default calculate
  calculate_flg = True
  B_coefs = []
  myfractal = fractal()
  myDCT = DCT()
  imageA = wm_img(image)
  imageA.type = 'A'
  listA = imageA.divide(R_block_size)

  for i in range(4):
      nazwa = "precalculated_files/wspolczynniki_"+ filename + "_" + str(i) + "_new.json"
      if (not calculate_flg):  # ladowanie z pliku
          if i==0: 
            print "Loading previously calculated watermark data..."
          with open(nazwa, 'rb') as handle:
              myfractal.coefficients[i] = json.load(handle)
      else:
          json_file = open(nazwa, 'wb')               # kompresja
          mapper_nr=imageA.quadrant_attr[i]["mapper"]
          myfractal.coefficients[i] = myfractal.compression(
             R_block_size, 
             imageA.quadrant(i), 
             imageA.quadrant(mapper_nr)
             )
          json.dump(myfractal.coefficients[i],json_file)
          json_file.close()

  imageB = wm_img(image.shift_up())                # nowy obraz przesuniety w gore
  imageB.type = "B"
  listB = imageB.divide(R_block_size)
  # performing dct on B type blocks
  for y in range(len(listB)):
      for x in range(len(listB[0])):
          output = myDCT.perform_rosiek(imageB.get_block(listB[x][y],R_block_size))
          imageB.save_block(output,listB[x][y]) 

  imageC = wm_img(image.shift_left())
  imageC.type = "C"
  listC = imageC.divide(R_block_size)
  # performing dct on C type blocks
  for x in range(len(listC)):
      for y in range(len(listC[0])):
          output = myDCT.perform_rosiek(imageC.get_block(listC[x][y])) # 128 is offset required for DCT to work faster
          # output = np.divide(output,quantization_table).view(wm_img)
          imageC.save_block(output,listC[x][y])

  blocks_in_quad = len(listA)/2

  #saving compression data in the image
  print "Start embedding..."
  for quadrant in range(4):
    mapper_q_A = imageA.quadrant_attr[quadrant]['mapper']
    mapper_offset_A = {'x': imageA.quadrant_attr[mapper_q_A]['x'],
                       'y': imageA.quadrant_attr[mapper_q_A]['y'] } 
    quadrant_offset_A = {'x': imageA.quadrant_attr[quadrant]['x'],
                         'y': imageA.quadrant_attr[quadrant]['y'] }
    
    mapper_q_B = imageB.quadrant_attr[quadrant]['mapper']
    mapper_offset_B = {'x': imageB.quadrant_attr[mapper_q_B]['x'],
                       'y': imageB.quadrant_attr[mapper_q_B]['y'] } 
    quadrant_offset_B = {'x': imageB.quadrant_attr[quadrant]['x'],
                         'y': imageB.quadrant_attr[quadrant]['y'] }

    mapper_q_C = imageC.quadrant_attr[quadrant]['mapper']
    mapper_offset_C = {'x': imageC.quadrant_attr[mapper_q_C]['x'],
                       'y': imageC.quadrant_attr[mapper_q_C]['y'] } 
    quadrant_offset_C = {'x': imageC.quadrant_attr[quadrant]['x'],
                         'y': imageC.quadrant_attr[quadrant]['y'] }

    for i in range(blocks_in_quad):
      for j in range(blocks_in_quad):

        x = i * R_block_size + quadrant_offset_A['x']
        y = j * R_block_size + quadrant_offset_A['y']

        x_type_A = i * R_block_size + mapper_offset_A['x']
        y_type_A = j * R_block_size + mapper_offset_A['y']

        x_type_B = i * R_block_size + mapper_offset_B['x']
        y_type_B = j * R_block_size + mapper_offset_B['y']

        x_type_C = i * R_block_size + mapper_offset_C['x']
        y_type_C = j * R_block_size + mapper_offset_C['y']

        B_coefficients = get_quantization_coefficients(imageB.get_block(coords={'x':x_type_B,'y':y_type_B}))
        C_coefficients = get_quantization_coefficients(imageC.get_block(coords={'x':x_type_C,'y':y_type_C}))
        # converting to int
        B_coefficients = [int(coef) for coef in B_coefficients]
        C_coefficients = [int(coef) for coef in C_coefficients]

        compression_data = myfractal.coefficients[mapper_q_A][i][j]

        block_data_holder = imageA.get_block(coords={'x':x,'y':y})

        watermarked_block = embed_watermark(block_data_holder,compression_data,B_coefficients,C_coefficients) 
        watermarked_block = embed_checksum(watermarked_block)

        imageA.save_block(watermarked_block,coords={'x':x,'y':y})

  print "Embedding finished. "
  comp_pic = "./pictures/" + filename + "_watermarked.pgm"
  imageA.export(comp_pic)

def authenticate(image, R_block_size, calculate_flg, delta, E_threshold, dct_threshold):
  myfractal = fractal()
  myDCT = DCT()
  
  imageA = wm_img(image)
  imageA.type = 'A'
  listA = imageA.divide(R_block_size)
  blocks_in_quad = len(listA)/2

  imageB = wm_img(image.shift_up())                # nowy obraz przesuniety w gore
  imageB.type = "B"
  listB = imageB.divide(R_block_size)

  imageC = wm_img(image.shift_left())
  imageC.type = "C"
  listC = imageC.divide(R_block_size)

  checksum_is_correct = np.zeros([len(listA),len(listA)])

  A_type_is_ok = np.zeros([len(listA),len(listA)])
  B_type_is_ok = np.zeros([len(listB),len(listB)])
  C_type_is_ok = np.zeros([len(listC),len(listC)])

  correctnes_table = np.zeros([len(listA),len(listA)])

  for x in range(len(listB)):
      for y in range(len(listB[0])):
          output = myDCT.perform_rosiek(imageB.get_block(listB[x][y])) # 128 is offset required for DCT to work faster
          # output = np.divide(output,quantization_table).view(wm_img)
          imageB.view(wm_img).save_block(output,listB[x][y])  

  for x in range(len(listC)):
      for y in range(len(listC[0])):
          output = myDCT.perform_rosiek(imageC.get_block(listC[x][y])) # 128 is offset required for DCT to work faster
          # output = np.divide(output,quantization_table).view(wm_img)
          imageC.view(wm_img).save_block(output,listC[x][y])


  # checking correctnes of checksum
  print "Start checking data ..."
  for quadrant in range(4):
    mapper_q = imageA.quadrant_attr[quadrant]['mapper']
    mapper_offset = {'x': imageA.quadrant_attr[mapper_q]['x'], 'y': imageA.quadrant_attr[mapper_q]['y'] } 
    quadrant_offset = {'x': imageA.quadrant_attr[quadrant]['x'], 'y': imageA.quadrant_attr[quadrant]['y'] }
    for i in range(blocks_in_quad):
      for j in range(blocks_in_quad):
        # wchodzimy do kazdego kwadwarntu
        # nastepnie ustawiamy odpowiedniego offseta, odpowiedniego
        # dla kwarantu, zeby mozna bylo operowac na calym obrazie
        # wyciagamy z kazdego bloku checksum i go przeliczamy czy sie nie zmienil
        i_quad = i + quadrant_offset['x'] / R_block_size
        j_quad = j + quadrant_offset['y'] / R_block_size

        x = i * R_block_size + quadrant_offset['x']
        y = j * R_block_size + quadrant_offset['y']

        x_type_A = i * R_block_size + mapper_offset['x']
        y_type_A = j * R_block_size + mapper_offset['y']

        block = imageA.get_block({'x':x,'y':y})
        block_mapped = imageA.get_block({'x':x_type_A,'y':y_type_A})
         
        data = retrieve_watermark_and_checksum(block)

        if errors_occured(block,data[3]):
          checksum_is_correct[i_quad][j_quad] = -1
        else:
          checksum_is_correct[i_quad][j_quad] = 1

        # checking correctness of E data        

  # checking correctness of B blocks info 
  for quadrant in range(4):
    
    mapper_q_A = imageA.quadrant_attr[quadrant]['mapper']
    mapper_offset_A = {'x': imageA.quadrant_attr[mapper_q_A]['x'],
                       'y': imageA.quadrant_attr[mapper_q_A]['y'] } 
    quadrant_offset_A = {'x': imageA.quadrant_attr[quadrant]['x'],
                         'y': imageA.quadrant_attr[quadrant]['y'] }
    
    mapper_q_B = imageB.quadrant_attr[quadrant]['mapper']
    mapper_offset_B = {'x': imageB.quadrant_attr[mapper_q_B]['x'],
                       'y': imageB.quadrant_attr[mapper_q_B]['y'] } 
    quadrant_offset_B = {'x': imageB.quadrant_attr[quadrant]['x'],
                         'y': imageB.quadrant_attr[quadrant]['y'] }

    mapper_q_C = imageC.quadrant_attr[quadrant]['mapper']
    mapper_offset_C = {'x': imageC.quadrant_attr[mapper_q_C]['x'],
                       'y': imageC.quadrant_attr[mapper_q_C]['y'] } 
    quadrant_offset_C = {'x': imageC.quadrant_attr[quadrant]['x'],
                         'y': imageC.quadrant_attr[quadrant]['y'] }
    
    for i in range(blocks_in_quad):
      for j in range(blocks_in_quad):    
        B_correct = True

        i_quad = i + quadrant_offset_A['x'] / R_block_size
        j_quad = j + quadrant_offset_A['y'] / R_block_size

        x = i * R_block_size + quadrant_offset_B['x']
        y = j * R_block_size + quadrant_offset_B['y']

        x_type_B = i * R_block_size + mapper_offset_B['x']
        y_type_B = j * R_block_size + mapper_offset_B['y']

        blockA = imageA.get_block({'x':x,'y':y})
        blockB = imageB.get_block({'x':x_type_B,'y':y_type_B})

        data = retrieve_watermark_and_checksum(blockA)

        B_recalculated = get_quantization_coefficients(blockB)

        for k in range(6):
          # adding threshold, because somehow there's problem with saving and retriving image
          if abs(B_recalculated[k] - data[1][k]) >= dct_threshold:
            B_correct = False

        if B_correct:
          B_type_is_ok[i_quad][j_quad] = 1
        else: 
          B_type_is_ok[i_quad][j_quad] = -1   
    # checking correctness of C blocks info 
    for quadrant in range(4):
      
      mapper_q_A = imageA.quadrant_attr[quadrant]['mapper']
      mapper_offset_A = {'x': imageA.quadrant_attr[mapper_q_A]['x'],
                         'y': imageA.quadrant_attr[mapper_q_A]['y'] } 
      quadrant_offset_A = {'x': imageA.quadrant_attr[quadrant]['x'],
                           'y': imageA.quadrant_attr[quadrant]['y'] }
      
      mapper_q_C = imageC.quadrant_attr[quadrant]['mapper']
      mapper_offset_C = {'x': imageC.quadrant_attr[mapper_q_C]['x'],
                         'y': imageC.quadrant_attr[mapper_q_C]['y'] } 
      quadrant_offset_C = {'x': imageC.quadrant_attr[quadrant]['x'],
                           'y': imageC.quadrant_attr[quadrant]['y'] }
      
      for i in range(blocks_in_quad):
        for j in range(blocks_in_quad):    
          C_correct = True

          i_quad = i + quadrant_offset_A['x'] / R_block_size
          j_quad = j + quadrant_offset_A['y'] / R_block_size

          x = i * R_block_size + quadrant_offset_A['x'] 
          y = j * R_block_size + quadrant_offset_A['y']

          x_type_C = i * R_block_size + mapper_offset_C['x']
          y_type_C = j * R_block_size + mapper_offset_C['y']

          blockA = imageA.get_block({'x':x,'y':y})
          blockC = imageC.get_block({'x':x_type_C,'y':y_type_C})

          data = retrieve_watermark_and_checksum(blockA)

          C_recalculated = get_quantization_coefficients(blockC)

          for k in range(6):
            # adding threshold, because somehow there's problem with saving and retriving image
            if abs(C_recalculated[k] - data[2][k]) >= dct_threshold:
              C_correct = False

          if C_correct:
            C_type_is_ok[i_quad][j_quad] = 1
          else: 
            C_type_is_ok[i_quad][j_quad] = -1   

  correctness_table = checksum_is_correct + B_type_is_ok + C_type_is_ok
  return [checksum_is_correct,B_type_is_ok,C_type_is_ok]

def reconstruction(image, R_block_size,correctness,filename):
  myfractal = fractal()
  myreconstruct = reconstruct()
  myDCT = DCT()

  imageA = wm_img(image)
  imageA.type = 'A'
  listA = imageA.divide(R_block_size)
  blocks_in_quad = len(listA) / 2

  imageB = wm_img(image.shift_up())                # nowy obraz przesuniety w gore
  imageB.type = "B"
  listB = imageB.divide(R_block_size)

  imageC = wm_img(image.shift_left())
  imageC.type = "C"
  listC = imageC.divide(R_block_size)

  correctness_table = correctness[0] + correctness[1] + correctness[2]
  checksum_is_correct = correctness[0]
  B_type_is_ok = correctness[1]
  C_type_is_ok = correctness[2]

  # A reconstruction
  imageA_new = wm_img(copy.deepcopy(image))
  imageA_new.type = 'A'

  for quadrant in range(4):
    mapper_q = imageA.quadrant_attr[quadrant]['mapper']
    mapper_offset = {'x': imageA.quadrant_attr[mapper_q]['x'], 'y': imageA.quadrant_attr[mapper_q]['y'] } 
    quadrant_offset = {'x': imageA.quadrant_attr[quadrant]['x'], 'y': imageA.quadrant_attr[quadrant]['y'] }
    for i in range(blocks_in_quad):
      for j in range(blocks_in_quad): 

        x = i * R_block_size + quadrant_offset['x']
        y = j * R_block_size + quadrant_offset['y']

        x_mapp = i * R_block_size + mapper_offset['x']
        y_mapp = j * R_block_size + mapper_offset['y']

        blockA = imageA.get_block({'x':x_mapp,'y':y_mapp})
        data = retrieve_watermark_and_checksum(blockA)
        x_base = data[0]['x'] + mapper_offset['x']
        y_base = data[0]['y'] + mapper_offset['y']

        base_block = imageA.get_block({'x': x_base,'y':y_base})
        reconstructed_block = myreconstruct.block_A(base_block,data[0],R_block_size)
        imageA_new.save_block(reconstructed_block,{'x':x,'y': y})

  # Reconstruction B

  reconstruct_B = wm_img(copy.deepcopy(image))
  reconstruct_B.type = 'B'

  for quadrant in range(4):
    mapper_q_A = imageA.quadrant_attr[quadrant]['mapper']
    mapper_offset_A = {'x': imageA.quadrant_attr[mapper_q_A]['x'],
                       'y': imageA.quadrant_attr[mapper_q_A]['y'] } 
    quadrant_offset_A = {'x': imageA.quadrant_attr[quadrant]['x'],
                         'y': imageA.quadrant_attr[quadrant]['y'] }
    
    mapper_q_B = imageB.quadrant_attr[quadrant]['mapper']
    mapper_offset_B = {'x': imageB.quadrant_attr[mapper_q_B]['x'],
                       'y': imageB.quadrant_attr[mapper_q_B]['y'] } 
    quadrant_offset_B = {'x': imageB.quadrant_attr[quadrant]['x'],
                         'y': imageB.quadrant_attr[quadrant]['y'] }

    mapper_q_C = imageC.quadrant_attr[quadrant]['mapper']
    mapper_offset_C = {'x': imageC.quadrant_attr[mapper_q_C]['x'],
                       'y': imageC.quadrant_attr[mapper_q_C]['y'] } 
    quadrant_offset_C = {'x': imageC.quadrant_attr[quadrant]['x'],
                         'y': imageC.quadrant_attr[quadrant]['y'] }

    for i in range(blocks_in_quad):
      for j in range(blocks_in_quad):

          x = i * R_block_size + quadrant_offset_B['x']
          y = j * R_block_size + quadrant_offset_B['y']

          i_mapp = i + mapper_offset_B['x'] / R_block_size
          j_mapp = j + mapper_offset_B['y'] / R_block_size

          i_quad = i + quadrant_offset_B['x'] / R_block_size
          j_quad = j + quadrant_offset_B['y'] / R_block_size

          x_type_B = i * R_block_size + mapper_offset_B['x']
          y_type_B = j * R_block_size + mapper_offset_B['y']

          x_type_A = i * R_block_size + mapper_offset_A['x']
          y_type_A = j * R_block_size + mapper_offset_A['y']


          blockA = imageA.get_block({'x':x_type_B,'y':y_type_B})
          data = retrieve_watermark_and_checksum(blockA)
          data[1] = get_coefficients_from_normalized(data[1]) 
          reconstruct_B.save_block(myDCT.reverse_rosiek(data[1]),{'x':x_type_A,'y':y_type_A})

  imageB_new = reconstruct_B

  # Reconstruction C

  reconstruct_C = wm_img(copy.deepcopy(image))
  reconstruct_C.type = 'A'

  for quadrant in range(4):
    mapper_q_A = imageA.quadrant_attr[quadrant]['mapper']
    mapper_offset_A = {'x': imageA.quadrant_attr[mapper_q_A]['x'],
                       'y': imageA.quadrant_attr[mapper_q_A]['y'] } 
    quadrant_offset_A = {'x': imageA.quadrant_attr[quadrant]['x'],
                         'y': imageA.quadrant_attr[quadrant]['y'] }
    
    mapper_q_B = imageB.quadrant_attr[quadrant]['mapper']
    mapper_offset_B = {'x': imageB.quadrant_attr[mapper_q_B]['x'],
                       'y': imageB.quadrant_attr[mapper_q_B]['y'] } 
    quadrant_offset_B = {'x': imageB.quadrant_attr[quadrant]['x'],
                         'y': imageB.quadrant_attr[quadrant]['y'] }

    mapper_q_C = imageC.quadrant_attr[quadrant]['mapper']
    mapper_offset_C = {'x': imageC.quadrant_attr[mapper_q_C]['x'],
                       'y': imageC.quadrant_attr[mapper_q_C]['y'] } 
    quadrant_offset_C = {'x': imageC.quadrant_attr[quadrant]['x'],
                         'y': imageC.quadrant_attr[quadrant]['y'] }

    for i in range(blocks_in_quad):
      for j in range(blocks_in_quad):

          x = i * R_block_size + quadrant_offset_A['x']
          y = j * R_block_size + quadrant_offset_A['y']

          i_mapp = i + mapper_offset_B['x'] / R_block_size
          j_mapp = j + mapper_offset_B['y'] / R_block_size

          i_quad = i + quadrant_offset_A['x'] / R_block_size
          j_quad = j + quadrant_offset_A['y'] / R_block_size

          x_type_C = i * R_block_size + mapper_offset_C['x']
          y_type_C = j * R_block_size + mapper_offset_C['y']

          x_type_A = i * R_block_size + mapper_offset_A['x']
          y_type_A = j * R_block_size + mapper_offset_A['y']


          blockA = imageA.get_block({'x':x_type_C,'y':y_type_C})
          data = retrieve_watermark_and_checksum(blockA)
          data[2] = get_coefficients_from_normalized(data[2]) 
          reconstruct_C.save_block(myDCT.reverse_rosiek(data[2]),{'x':x_type_A,'y':y_type_A})


  imageC_new = reconstruct_C

  reconstructed_Image = myreconstruct.whole_img(imageA,imageA_new,imageB_new,imageC_new,correctness,R_block_size,blocks_in_quad) 

  reconstructed_Image.export(filename+'_reconstructed_'+'.pgm')

