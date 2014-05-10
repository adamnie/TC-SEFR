import numpy as np
from numpy import linalg as LA 


def mean_by_four(block):
  """
      Averages four neighbouring pixels
  """
  newShape = len(block)/2
  block_av = np.empty([newShape,newShape])
  for i in range(0,newShape):
      for j in range(0,newShape):
          block_av[i,j] =  block[2*i:2*(i+1),2*j:2*(j+1)].mean()
  return block_av

def get_quantization_coefficients(quant_block):
    for x in quant_block:
        for y in x:
            y = round(y)

    coefficients = []
    coefficients.append(quant_block[0,0])
    coefficients.append(quant_block[0,1])
    coefficients.append(quant_block[1,0])
    coefficients.append(quant_block[2,0])
    coefficients.append(quant_block[1,1])
    coefficients.append(quant_block[0,2])

    return coefficients

def find_best(how_many,dct_transform_list):

    sorted_dct = sorted(dct_transform_list,key= lambda dct_transform : dct_transform['Distance'])
    return sorted_dct[:how_many]

def compare_best(R,list_to_compare,D_list):
    best = {'E':float('inf')}
    for match in list_to_compare:
        D = transform(D_list[match['x']][match['y']],match['t'])
        params = compare(R,D)  
        if params['E'] < best['E']:      
            best = params 
            best['x'] = match['x']
            best['y'] = match['y']
            best['t'] = match['t']
    return best

def transform(D,type):
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

def compare(R,D):

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
