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

        newBlock[0,0] = from_normalized(coefficients[0],256)
        newBlock[0,1] = from_normalized(coefficients[1],128)
        newBlock[1,0] = from_normalized(coefficients[2],128)
        newBlock[2,0] = from_normalized(coefficients[3],32)
        newBlock[1,1] = from_normalized(coefficients[4],64)
        newBlock[0,2] = from_normalized(coefficients[5],128)

        recovered = np.multiply(newBlock,quantization_table)
        return recovered
