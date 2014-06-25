from lib.fractal import *
import numpy as np

quantization_table = np.matrix([[16, 11, 10, 16, 24, 40, 51, 61],
                                   [12, 13, 14, 19, 26, 58, 60, 55],
                                   [14, 13, 16, 24, 40, 57, 69, 56],
                                   [16, 17, 22, 29, 51, 87, 80, 62],
                                   [18, 22, 37, 56, 68, 109, 103, 77],
                                   [24, 35, 55, 64, 81, 104, 113, 92],
                                   [49, 64, 78, 87, 103, 121, 120, 101],
                                   [72, 92, 95, 98, 112, 100, 103, 99]]);

class reconstruct :

    def __init__(self):
        self.fractal = fractal()

    def block_A(self,base,compression_data,R_block_size=8):
        return self.fractal.decompression(compression_data,base,R_block_size)

    def block_B_or_C(self,coefficients,block_size=8):
        newBlock = np.zeros((block_size,block_size))
        # inserting coefficient in zigzag order

        newBlock[0,0] = coefficients[0]
        newBlock[0,1] = coefficients[1]
        newBlock[1,0] = coefficients[2]
        newBlock[2,0] = coefficients[3]
        newBlock[1,1] = coefficients[4]
        newBlock[0,2] = coefficients[5]

        recovered = np.multiply(newBlock,quantization_table) / 2
        return recovered

    def whole_img(self,original, imageA, imageB, imageC, correctness ,R_block_size , blocks_in_quad):
        # creating a image of the same size as the one loaded
        reconstructed = imageA.copy()
        correctness_table = correctness[0] + correctness[1] + correctness[2]

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

              wages = 0

              x = i * R_block_size + quadrant_offset_A['x']
              y = j * R_block_size + quadrant_offset_A['y']

              x_block = x / R_block_size
              y_block = y / R_block_size

              if correctness_table[x_block][y_block] < 0 :
                x_type_A = i * R_block_size + mapper_offset_A['x']
                y_type_A = j * R_block_size + mapper_offset_A['y']

                x_mapp_A = x_type_A / R_block_size
                y_mapp_A = y_type_A / R_block_size

                x_type_B = i * R_block_size + mapper_offset_B['x']
                y_type_B = j * R_block_size + mapper_offset_B['y']

                x_mapp_B = x_type_B / R_block_size
                y_mapp_B = y_type_B / R_block_size

                x_type_C = i * R_block_size + mapper_offset_C['x']
                y_type_C = j * R_block_size + mapper_offset_C['y']

                x_mapp_C = x_type_C / R_block_size
                y_mapp_C = y_type_C / R_block_size


                # block A
                if correctness[0][x_mapp_A][y_mapp_A] == 1:
                  block_A = imageA.get_block({'x':x,'y':y})
                  wages += 1
                else:
                  block_A = 0
                # block B
                if correctness[1][x_mapp_B][y_mapp_B] == 1:
                  block_B = imageB.get_block({'x':x,'y':y})
                  wages += 1
                else:
                  block_B = 0
                # block C
                if correctness[2][x_mapp_C][y_mapp_C] == 1:
                  block_C = imageC.get_block({'x':x,'y':y})
                  wages += 1
                else:
                  block_C = 0
                if wages > 0:
                  reconstructed_block = (block_A + block_B + block_C) / wages
                else:
                  reconstructed_block = original.get_block({'x':x,'y':y})
              else:
               reconstructed_block = original.get_block({'x':x,'y':y})

              
              reconstructed.save_block(reconstructed_block,{'x':x,'y':y} )
              

        return reconstructed

