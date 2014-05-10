import numpy as np 
from img_refurbished import *
from dct import *
import datetime

#constants

MAX_ERROR = float('inf')


class fractal:

  how_many = 5
  coefficients = [None] * 4

  def __new__(self,how_many=5):
    self.coefficients = [None] * 4
    self.how_many = how_many    

  def compression(self, R_size, image_R, image_D):
    dct = DCT()

    print "Starting compression"
    time = datetime.datetime.now()


    R_count = [image_R.block_number_y(R_size),image_R.block_number_x(R_size)]
    D_count = [image_D.block_number_y(R_size),image_D.block_number_x(R_size)]       

    D_list = image_D.get_D_blocks(D_count,R_size)

    transformation_data_list = []
    for R_x in range(R_count[0]):
      transformation_data_list.append([])
      for R_y in range(R_count[1]):
        R = image_R.block_R(R_x,R_y,R_size)
        transformation_data_list[R_x].append({'E': MAX_ERROR})
        local = []
        for D_x in range(0,D_count[0]-1):
          for D_y in range (0,D_count[1]-1):
            for T_type in range(7):
              local_dict = {}
              D = transform(D_list[D_x][D_y],T_type)
              local_dict['Distance'] = dct.compare(R,D)
              local_dict['x'] = D_x
              local_dict['y'] = D_y
              local_dict['t'] = T_type
              local.append(local_dict)

        list_to_compare = find_best(self.how_many,local)

        transformation_data_list[R_y][R_x] = compare_best(R,list_to_compare,D_list)

    print "it took: ", (datetime.datetime.now() - time) 

    return transformation_data_list

  def decompression(self,transform_list,img_size,blockSize):
    """
        img_size should be a matrix ([sizeX,sizeY])
        transform list should be the result of fractal.compression()
        as a result saves image (should be fixed, to return array to be compared with 
        data found)
    """

    Base = np.zeros(img_size)+127

    print "Starting decompression"
    time = datetime.datetime.now()

    for iteration in range(0,2):
        for i in range(Base.shape[0]/blockSize):
            for j in range(Base.shape[0]/blockSize):
                Base[blockSize*i:blockSize*(i+1),blockSize*j:blockSize*(j+1)] = (transform(average(Base[transform_list[i][j]['x']:transform_list[i][j]['x']+2*blockSize,transform_list[i][j]['y']:transform_list[i][j]['y'] + 2*blockSize]),transform_list[i][j]['t']))*transform_list[i][j]['s'] + transform_list[i][j]['o']
    
    image = numpy.uint8(numpy.matrix(Base))
    print "it took: ", (datetime.datetime.now() - time) 
    return image
