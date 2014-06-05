"""
    Implements img class, which extends np.ndarray object
"""
#imports
import numpy as np
from scipy import misc
from helpers import *
import matplotlib.pyplot as plt
import PIL
import numpy

# class for imported image
class img(numpy.ndarray):

    nazwa = None
    format = None

    # initialize
    def __init__(self, obraz):
        self.obraz = obraz
        self.format = "abc"
        self.nazwa = "name"

    def get_nazwa(self):
        return self.nazwa

class img(np.ndarray):

    def __init__(self,stuff):
      pass
    def __new__(self,filename):   
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
    #poki co bez modulo, ok? 

    def how_many_D_in_a_row(self, Rsize, delta=None):
        if (delta == None):
            delta = Rsize
        return (self.width() - 2*Rsize)/delta + 1

    def how_many_D_in_a_column(self, Rsize, delta=None):
        if (delta == None):
            delta = Rsize
        return (self.height() - 2*Rsize)/delta + 1

    def resize(self, size):
        return misc.imresize(self, size, "bilinear", "L")

    # size of block D is 2x size of block R
    # as an argument we pass the same Rsize as to block R! it is multiplied inside the function
    # delta is the step of selecting next image, default it's equal to Rsize 
    # x and y are numbers (indexes) of block D, assuming Dsize=2*Rsize and step=delta

    def blockD(self, x, y, Rsize, delta=None): # OVERLAPPING
        if (x>self.how_many_D_in_a_row(Rsize,delta)-1 or y>self.how_many_D_in_a_column(Rsize,delta)-1):
            print "Blad indeksowania D!!!"
            return -1
        if (delta == None):
            delta = Rsize
        sth = self.cutsquare(x*delta,y*delta,2*Rsize)
        #zapomnialem wczesniej o usrednieniu!!!!
        return sth.view(D_block)

    def meanbyfour(self, Rsize):
        sth_= np.zeros(shape=(Rsize,Rsize))
        for y in range(Rsize):
            for x in range(Rsize):
                sth_[y][x] = self[2*y:2*(y+1),2*x:2*(x+1)].mean()
        return sth_.view(D_block)

    def save_block(self,new_block,coords):
      size = len(new_block)
      for x in range(size):
        for y in range(size):
          self[coords['x']+x][coords['y']+y] = new_block[x][y]

    def export(filename):
      misc.imsave(filename,self)# check this command

    def plot(self):
      black = 0
      white = 255
      plt.imshow(self, cmap = plt.cm.gray, norm=plt.Normalize(black,white))
      plt.show()

    def shift_up(self,shift_amount=4):
      return np.roll(self,-shift_amount,axis=0)

    def shift_left(self,shift_amount=4):
      return np.roll(self,-shift_amount,axis=1)

    def cut_block(self,x,y,size):
      horizontal = self[x:x+size]
      #initialiing empy block with proper shape
      block = np.zeros(shape=(size,size))
      for col in range(size):
          block[col] = (horizontal[col])[y:y+size]
      return block.view(img)

    def get_block(self,coords,size=8):
      return self.cut_block(coords['x'],coords['y'],size)

    def block_number_x(self,blocksize):
      return self.width()/blocksize

    def block_number_y(self,blocksize):
      return self.height()/blocksize

    def width(self):
      return len(self[1])

    def height(self):
      return len(self)

    def how_many_D_in_a_row(self, R_size, delta=None):
      if delta == None :
        delta = R_size
      return (self.width() - 2 * R_size) / delta + 1

    def how_many_D_in_a_column(self, R_size, delta=None):
      if delta == None :
        delta = R_size
      return (self.height() - 2*R_size) / delta + 1

    def block_R(self, x, y, R_size):
      R_block = self.cut_block(x*R_size,y*R_size,R_size)
      return R_block.view()

    def block_D(self, x, y, R_size, delta=None):
      if (x>self.how_many_D_in_a_row(R_size,delta) or y>self.how_many_D_in_a_column(R_size,delta)):
          pass
          print "Indexing D_block error!"
          return -1
      if (delta == None):
          delta = R_size
      returnBlock = self.cut_block(x*delta,y*delta,2*R_size)
      return returnBlock.view(img)
    def get_D_blocks(self,D_number,R_size,delta=None,average=True):
      D_list = []
      for D_x in range(0,D_number[0]-1):
            D_list.append([])
            for D_y in range (0,D_number[1]-1):
                D = self.block_D(D_x,D_y,R_size,delta)
                if average == True:           # if avg == True, returns R_size x R_size
                    D = mean_by_four(D)   # if avg == False, returns 2*R_size x 2*R_size
                D_list[D_x].append(D)

      return D_list
