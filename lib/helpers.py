import numpy as np
from numpy import linalg as LA 

MAX_S = 128
MAX_O = 256

def mean_by_four(block):
  """
      Averages four neighbouring pixels 
      ex. | 0 7 | would  be returned as | 4 |
          | 0 9 |
  """
  newShape = len(block)/2
  block_av = np.empty([newShape,newShape])
  for i in range(0,newShape):
      for j in range(0,newShape):
          block_av[i,j] =  block[2*i:2*(i+1),2*j:2*(j+1)].mean()
  return block_av

def get_quantization_coefficients(quant_block):
    """
        Prepares 6 quantization_coefficients, similarely to JPEG tech.
        coef. are rounded and normalized normalize(value,max) to range (-max/2, max/2)
    """

    for x in quant_block:
        for y in x:
            y = round(y)

    coefficients = []
    
    coefficients.append(normalize(quant_block[0,0],256))
    coefficients.append(normalize(quant_block[0,1],128))
    coefficients.append(normalize(quant_block[1,0],128))
    coefficients.append(normalize(quant_block[2,0],32))
    coefficients.append(normalize(quant_block[1,1],64))
    coefficients.append(normalize(quant_block[0,2],128))

    return coefficients

def get_coefficients_from_normalized(block):
    coefficients = get_quantization_coefficients(block)
    from_norm = []
    from_norm.append(from_normalized(coefficients[0],256))
    from_norm.append(from_normalized(coefficients[1],128))
    from_norm.append(from_normalized(coefficients[2],128))
    from_norm.append(from_normalized(coefficients[3],32))
    from_norm.append(from_normalized(coefficients[4],64))
    from_norm.append(from_normalized(coefficients[5],128))

    return from_norm

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
    s = normalize(s,128)
    o = normalize(o,256)

    E = LA.norm(R - (s*D+o))

    Res['E'] = int(E)
    Res['s'] = s
    Res['o'] = o
    Res['x'] = -1
    Res['y'] = -1
    Res['t'] = -1

    return Res

def normalize(number, max_value):
  """
  first moves number to range (-max_value/2 -1, max_value/2 -1)
  then add max_value/2 + 1
  return number between <0,max_value-1>
  """
  number = int(number)
  local_max = max_value / 2 - 1
  if number > local_max:
    number = local_max
  if number < - local_max:
    number = -local_max

  normalized = number + local_max + 1
  return normalized

def from_normalized(number, max_value):
  return number - max_value / 2

def replaceTwoLSB(n,lsb2,lsb):
  n = n.astype(int) 
  n = (n & ~(1 << 1)) | (lsb2 << 1) 
  n = (n & ~1) | lsb 
  return n
