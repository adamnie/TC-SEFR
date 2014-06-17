import numpy as np 
import datetime
from lib.dct import *
from lib.helpers import *

MAX_ERROR = float('inf')

class fractal:

  how_many = 5
  coefficients = [None] * 4

  def __new__(self,how_many=5):
    self.coefficients = [None] * 4 # list of coefficients 
    self.how_many = how_many    # how many best matches should be considered

  def compression(self, R_size, image_R, image_D):
    """
      Function calulates fractal coeffiecints of transition from R block to D block
      for the whole image, and returns a list of coefficients
    """

    dct = DCT()

    print "Starting compression"
    time = datetime.datetime.now()

    R_count = [image_R.block_number_y(R_size),image_R.block_number_x(R_size)]
    D_count = [image_D.block_number_y(2*R_size),image_D.block_number_x(2*R_size)]       

    D_list = image_D.get_D_blocks(D_count,R_size)

    transformation_data_list = []
    for R_x in range(R_count[0]):
      transformation_data_list.append([])
      for R_y in range(R_count[1]):
        R = image_R.block_R(R_x,R_y,R_size)
        transformation_data_list[R_x].append({'E': MAX_ERROR})
        local = []
        for D_x in range(0,D_count[0]):
          for D_y in range (0,D_count[1]):
            for T_type in range(7):
              local_dict = {}
              D = transform(D_list[D_x][D_y],T_type)
              local_dict['Distance'] = dct.compare(R,D)
              local_dict['x'] = D_x
              local_dict['y'] = D_y
              local_dict['t'] = T_type
              local.append(local_dict)

        list_to_compare = find_best(self.how_many,local)

        transformation_data_list[R_x][R_y] = compare_best(R,list_to_compare,D_list)

    print "it took: ", (datetime.datetime.now() - time) 

    return transformation_data_list

  def decompression(self,compression_data,Base,R_block_size):
    """
        img_size should be a matrix ([sizeX,sizeY])
        transform list should be the result of fractal.compression()
        as a result saves image (should be fixed, to return array to be compared with 
        data found)
    """

    decompressed = transform(Base,compression_data['t'])*compression_data['s'] + compression_data['o']

    for row in decompressed:
      for pixel in row:
        pixel = normalize(pixel,256)

    return decompressed