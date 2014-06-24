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
        dct = lambda x: fftpack.dct(x, type=2,norm='ortho')
        idct = lambda x: fftpack.dct(x, type=3,norm='ortho')
        return self

    def perform(self,block):
        return dct(block)

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
        R_DCT = self.perform_rosiek(R)
        D_DCT = self.perform_rosiek(D)

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

    def perform_rosiek(self,block):
      T = np.matrix([[.3536, .3536, .3536, .3536, .3536, .3536, .3536, .3536],
                    [.4904, .4157, .2778, .0975, -.0975, -.2778, -.4157, -.4904],
                    [.4619, .1913, -.1913, -.4619, -.4619, -.1913, .1913, .4619],
                    [.4157, -.0975, -.4904, -.2778, .2778, .4904, .0975, -.4157],
                    [.3536, -.3536, -.3536, .3536, .3536, -.3536, -.3536, .3536],
                    [.2778, -.4904, .0975, .4157, -.4157, -.0975, .4904, -.2778],
                    [.1913, -.4619, .4619, -.1913, -.1913, .4619, -.4619, .1913],
                    [.0975, -.2778, .4157, -.4904, .4904, -.4157, .2778, -.0975]]);

      Q = np.matrix([[16, 11, 10, 16, 24, 40, 51, 61],
                        [12, 13, 14, 19, 26, 58, 60, 55],
                        [14, 13, 16, 24, 40, 57, 69, 56],
                        [16, 17, 22, 29, 51, 87, 80, 62],
                        [18, 22, 37, 56, 68, 109, 103, 77],
                        [24, 35, 55, 64, 81, 104, 113, 92],
                        [49, 64, 78, 87, 103, 121, 120, 101],
                        [72, 92, 95, 98, 112, 100, 103, 99]]);

      Q_10 = np.matrix([[80, 60, 50, 80, 120, 200, 255, 255],
                          [55, 60, 70, 95, 130, 255, 255, 255],
                          [70, 65, 80, 120, 200, 255, 255, 255],
                          [70, 85, 110, 145, 255, 255, 255, 255],
                          [90, 110, 185, 255, 255, 255, 255, 255],
                          [120, 175, 255, 255, 255, 255, 255, 255],
                          [245, 255, 255, 255, 255, 255, 255, 255],
                          [255, 255, 255, 255, 255, 255, 255, 255]]);

      D = T*(block-128)*T.H;
      
      C = (np.matrix(D)/Q).round()
      quant = 1;


      return C
    def reverse_rosiek(self,coef):

      T = np.matrix([[.3536, .3536, .3536, .3536, .3536, .3536, .3536, .3536],
                    [.4904, .4157, .2778, .0975, -.0975, -.2778, -.4157, -.4904],
                    [.4619, .1913, -.1913, -.4619, -.4619, -.1913, .1913, .4619],
                    [.4157, -.0975, -.4904, -.2778, .2778, .4904, .0975, -.4157],
                    [.3536, -.3536, -.3536, .3536, .3536, -.3536, -.3536, .3536],
                    [.2778, -.4904, .0975, .4157, -.4157, -.0975, .4904, -.2778],
                    [.1913, -.4619, .4619, -.1913, -.1913, .4619, -.4619, .1913],
                    [.0975, -.2778, .4157, -.4904, .4904, -.4157, .2778, -.0975]]);

      Q = np.matrix([[16, 11, 10, 16, 24, 40, 51, 61],
                    [12, 13, 14, 19, 26, 58, 60, 55],
                    [14, 13, 16, 24, 40, 57, 69, 56],
                    [16, 17, 22, 29, 51, 87, 80, 62],
                    [18, 22, 37, 56, 68, 109, 103, 77],
                    [24, 35, 55, 64, 81, 104, 113, 92],
                    [49, 64, 78, 87, 103, 121, 120, 101],
                    [72, 92, 95, 98, 112, 100, 103, 99]]);
      quant = 1
      R = np.matrix(Q)*0;
      R[0,0] = coef[0]*quant
      R[0,1] = coef[1]*quant
      R[1,0] = coef[2]*quant
      R[2,0] = coef[3]*quant
      R[1,1] = coef[4]*quant
      R[0,2] = coef[5]*quant
      R = (np.multiply(R, Q)).round()
      N = (T.H*R*T).round()+128
      return N



