import numpy as np
from numpy import linalg as LA
from PIL import ImageFile
from PIL import Image
from img import *
from wm_img import *
from dct import *
import datetime

# y - vertical , x - horizontal
#[y,x]

"""
    future optimization : instead of x and y indexes hash should be used

    flat lists with smart indecies instead of slow 2d lists

    C should be used to improve compare function
"""

class fractal:

    def __init__(self):
        self.DCT = DCT()

    def compare(self,R,D):

        """
        computes best match Domain block(D) for Range Block (R)

        E(R, D) = norm(R - (s*D + o*U))

        lowest E defines best match
        """
        Res = {}

        R_average = R.mean();
        D_average = D.mean();
        s = (np.array(R-R_average)*np.array(D-D_average)).sum() / (np.array(D-D_average)*np.array(D-D_average)).sum()
        o = R_average - s* D_average;
        E = LA.norm(R*(s*D+o))

        Res['E'] = E
        Res['s'] = s
        Res['o'] = o
        Res['x'] = -1
        Res['y'] = -1
        Res['t'] = -1

        return Res

    def transform(self,D,type):
        """
          possible rotations (in degrees): 0 , 90 , 180 , 270
          possible flips: left-to-right
          types: 0-3 only rotation
                 4-7 rotation + flip
        """

        if type >= 4:
            return np.rot90(np.fliplr(D),type%4)
        else:
            return np.rot90(D,type%4)

    def compression(self,R_size,image_R,image_D):
        """
            function finds best match Domain Block (D) for every Range Block (R)
            saves data (x,y,s,o,E,t) into transform_list(not yet)
        """

        print "Starting compression"
        time = datetime.datetime.now()
        MAX_ERROR = float('inf')
        how_many = 20

        #calculating number of R and D blocks
        R_number = [image_R.block_number_y(R_size) , image_R.block_number_x(R_size)]
        D_number = [image_D.block_number_y(2*R_size) , image_D.block_number_x(2*R_size)]
        # getting full list of D blocks (so D blocks doesn't hae to be calculated multiple times )
        D_list = self.get_D_blocks(image_D,D_number,R_size)

        transform_list = []
        for R_y in range(0,R_number[0]):
            transform_list.append([])
            for R_x in range (0,R_number[1]):
                R = image_R.blockR(R_x,R_y,R_size)
                transform_list[R_y].append({'E': MAX_ERROR})
                local_DCT_transform_list = []
                for D_y in range(0,D_number[0]):
                    for D_x in range (0,D_number[1]):
                        for T_type in range(7):
                            local_dict = {}
                            local_dict['Distance'] = self.DCT.compare(R,self.transform(D_list[D_x][D_y],T_type))
                            local_dict['x'] = D_x
                            local_dict['y'] = D_y
                            local_dict['t'] = T_type
                            local_DCT_transform_list.append(local_dict)

                list_to_compare = self.find_best(how_many,local_DCT_transform_list)

                transform_list[R_y][R_x] = self.compare_best(R,list_to_compare,D_list)


        print "it took: ", (datetime.datetime.now() - time)                        

        return transform_list

    def find_best(self,how_many,dct_transform_list):

        sorted_dct = sorted(dct_transform_list,key= lambda dct_transform : dct_transform['Distance'])
        return sorted_dct[:how_many]

    def compare_best(self,R,list_to_compare,D_list):
        best = {'E':float('inf')}
        for match in list_to_compare:
            D = self.transform(D_list[match['x']][match['y']],match['t'])
            params = self.compare(R,D)  
            if params['E'] < best['E']:      
                best = params 
                best['x'] = match['x']
                best['y'] = match['y']
                best['t'] = match['t']
        return best

    def get_D_blocks(self,image,D_number,R_size,delta=None,avg=True):
        D_list = []
        for D_y in range(0,D_number[0]):
            D_list.append([])
            for D_x in range (0,D_number[1]):
                D = image.blockD(D_x,D_y,R_size,delta)
                if avg==True:             # if avg == True, returns R_size x R_size
                    D = self.average(D)   # if avg == False, returns 2*R_size x 2*R_size
                D_list[D_y].append(D)

        return D_list

    def open_img_PGM(self,filename):
        """
        Opens .PGM image using pillow library

        should return 2D list / numpy.array of pixels in gray scale
        """

        fp = open(filename,'rb')

        p = ImageFile.Parser()

        while True :
            s = fp.read(1024)
            if not s:
                break
            p.feed(s)

        im = p.close()

        pixels = np.asarray(im)
        return pixels.view(img)

    def decompression(self,transform_list,img_size,blockSize):
        """
            img_size should be a matrix ([sizeX,sizeY])
            transform list should be the result of fractal.compression()
        """

        Base = np.zeros(img_size)+127

        print "Starting decompression"
        time = datetime.datetime.now()

        for iteration in range(0,2):
            for i in range(Base.shape[0]/blockSize):
                for j in range(Base.shape[0]/blockSize):
                    Base[blockSize*i:blockSize*(i+1),blockSize*j:blockSize*(j+1)] = (self.transform(self.average(Base[transform_list[i][j]['y']:transform_list[i][j]['y']+2*blockSize,transform_list[i][j]['x']:transform_list[i][j]['x'] + 2*blockSize]),transform_list[i][j]['t']))*transform_list[i][j]['s'] + transform_list[i][j]['o']
        
        img = Image.fromarray(numpy.uint8(numpy.matrix(Base)))
        img.save('lena_frac.pgm')
        print "it took: ", (datetime.datetime.now() - time) 

    def average(self,D):
        """
            Averages four neighbouring pixels
        """
        newShape = len(D)/2
        D_av = np.empty([newShape,newShape])
        for i in range(0,newShape):
            for j in range(0,newShape):
                D_av[i,j] =  D[2*i:2*(i+1),2*j:2*(j+1)].mean()
        return D_av

