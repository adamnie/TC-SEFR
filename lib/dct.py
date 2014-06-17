from scipy.fftpack import dct , idct
import numpy as np
from wm_img import *

quantization_table = np.matrix([[16, 11, 10, 16, 24, 40, 51, 61],
                                   [12, 13, 14, 19, 26, 58, 60, 55],
                                   [14, 13, 16, 24, 40, 57, 69, 56],
                                   [16, 17, 22, 29, 51, 87, 80, 62],
                                   [18, 22, 37, 56, 68, 109, 103, 77],
                                   [24, 35, 55, 64, 81, 104, 113, 92],
                                   [49, 64, 78, 87, 103, 121, 120, 101],
                                   [72, 92, 95, 98, 112, 100, 103, 99]]);



class DCT:
    """
        Wrapper class for scipy.fftpack.dct/idct
    """
    def __new__(self):
        dct = lambda x: fftpack.dct(x, type=3,norm='ortho')
        idct = lambda x: fftpack.idct(x, type=3,norm='ortho')
        return self

    def perform(self,block):
        return dct(dct(block.T).T)

    def perform_block(self,block_list):
        dct_list = []
        for block in block_list:
            dct_list.append(dct(block,type=3,norm='ortho'))
        return dct_list

    def reverse(self,block):
        return idct(idct(block.T).T)

    def reverse_block(self,block):
        dct_list = []
        for block in block_list:
            dct_list.append(dct(block,type=3,norm='ortho'))
        return dct_list
    def compare(self,R,D):
        diff = 0.0 
        R_DCT = dct(R,type=3,norm='ortho')
        D_DCT = dct(D,type=3,norm='ortho')

        for i in range(len(R_DCT)):
            for j in range(len(R_DCT[0])):
                diff += abs(R_DCT[i,j] - D_DCT[i,j])

        return diff

    def on_image(self,image,list):
      for x in range(len(list)):
        for y in range(len(list[0])):
          output = self.perform(image.get(list[x][y])-128)
          # wykonuje DCT - UWAGA - zmienilem funkcje dct.perform(), tak, zeby nie zapisywala do listy a zwracala bezposrednio!
          output = np.divide(output,quantization_table).view(wm_img)
          image.view(wm_img).save_block(output,list[x][y])         

      return image


