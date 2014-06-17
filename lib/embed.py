from lib.fractal import *
from lib.wm_img import *
from lib.helpers import *
import numpy as np
import math
import hashlib

#constants
BITS_FOR_CHECKSUM = 16

"""
    16 blocks: x(7) + y(7) + t(3) + s(7) + o(8)
    B blocks: 40 bits quantzation table
    C blocks: 40 bits quantization table
    Checksum: 16 bits

    ========
    128 bits

    1) convert information into structure in which all data will be binary
    2) Divide binary data in a consistent way
    3) Clean bits
    4) Embed binary data
    5) retrieve binary data

    TO DO:
    make converting functions dependent on the size of x and y
    case when scale or offset might be < 0
    bin operations should be done with masks

"""

def to_bin_str(A_blocks,B_blocks,C_blocks):
    """
        Converts data from A,B,C blocks and checksum into 1 112 bits long 
        string (len(string) == 112)
    """
    B = ''
    C = ''

    for elem in B_blocks:
      if isinstance(elem,int) == False:
        print "Error, to_bin_str, float instead of int"
        return -1
    for elem in C_blocks:
      if isinstance(elem,int) == False:
        print "Error, to_bin_str, float instead of int"
        return -1

    
    x = "{0:07b}".format(int(A_blocks['x']))
    y = "{0:07b}".format(int(A_blocks['y']))
    t = "{0:03b}".format(int(A_blocks['t']))    
    s = "{0:07b}".format(int(A_blocks['s']))
    o = "{0:08b}".format(int(A_blocks['o']))

    B += "{0:08b}".format(int(B_blocks[0]))
    B += "{0:07b}".format(int(B_blocks[1]))
    B += "{0:07b}".format(int(B_blocks[2]))
    B += "{0:05b}".format(int(B_blocks[3]))
    B += "{0:06b}".format(int(B_blocks[4]))
    B += "{0:07b}".format(int(B_blocks[5]))

    C += "{0:08b}".format(int(C_blocks[0]))
    C += "{0:07b}".format(int(C_blocks[1]))
    C += "{0:07b}".format(int(C_blocks[2]))
    C += "{0:05b}".format(int(C_blocks[3]))
    C += "{0:06b}".format(int(C_blocks[4]))
    C += "{0:07b}".format(int(C_blocks[5]))

    return x + y + t + s + o + B + C


def to_data(bin_string):

    """
        Retrieves data from binary string:
        - transform list (A blocks) 32 bits
        - JPEG like data (B and C blocks) each 40 bits
        - checksum 16 bits
    """
    watermark_data = []
    B_blocks = []
    C_blocks = []
    transform = {}
    transform['x'] = int(bin_string[:7],2)
    transform['y'] = int(bin_string[7:14],2)
    transform['t'] = int(bin_string[14:17],2)
    transform['s'] = from_normalized(int(bin_string[17:24],2),128)      
    transform['o'] = from_normalized(int(bin_string[24:32],2),256)

    watermark_data.append(transform)

    B_blocks.append(int(bin_string[32:40],2))
    B_blocks.append(int(bin_string[40:47],2))
    B_blocks.append(int(bin_string[47:54],2))
    B_blocks.append(int(bin_string[54:59],2))
    B_blocks.append(int(bin_string[59:65],2))
    B_blocks.append(int(bin_string[65:72],2))
    watermark_data.append(B_blocks)

    C_blocks.append(int(bin_string[72:80],2))
    C_blocks.append(int(bin_string[80:87],2))
    C_blocks.append(int(bin_string[87:94],2))
    C_blocks.append(int(bin_string[94:99],2))
    C_blocks.append(int(bin_string[99:105],2))
    C_blocks.append(int(bin_string[105:112],2))
    watermark_data.append(C_blocks)

    checksum = int(bin_string[112:128],2)
    watermark_data.append(checksum)

    return watermark_data

def embed_watermark(block,A_blocks_data,B_blocks_data=0,C_blocks_data=0):
    """
        Inserts data from 3 block types and checksum into 2 last bits of every pixel(grey scale)
        and returns watermarked block (type numpy.array)
    """
    bin_watermark_data = to_bin_str( A_blocks_data, B_blocks_data, C_blocks_data)
    size = int(math.sqrt(block.size))
    watermarked_block = np.empty([size,size])
    for i in range(size):
        for j in range(size):
            if(i < size - BITS_FOR_CHECKSUM/16):
                pixel = block[i,j] - block[i,j] % 4 # seting 2 last bit to 0
                watermarked_block[i,j] = pixel + int(bin_watermark_data[2*(i*size+j):2*(i*size+j+1)],2) # seting 2 last bits to those from watermark
            else:
                watermarked_block[i,j] = block[i,j]
    return watermarked_block
        

def retrieve_watermark_and_checksum(watermarked_block):
    """
        Retrieves data from watermarked image, then converts it from binary to decimal
        returns [transform, B_blocks_coef,C_blocks_coef,checksum]
    """
    size = int(math.sqrt(watermarked_block.size)) # .size returns all elements, and my size should define length of block in either x or y dimension
    bin_watermark_data = ""

    for i in range(size):
        for j in range(size):
            bin_watermark_data += "{0:02b}".format(int(watermarked_block[i,j]) % 4)
    watermark_data = to_data(bin_watermark_data)
    return  watermark_data

def checksum(block,size=8):
    """
        Calculates md5 hash for whole block with
        exception of last 8 bits (where cheksum data will be embedded)
    """
    checksum = hashlib.md5()
    for i in range(size-BITS_FOR_CHECKSUM/16):
        for j in range(size):
            checksum.update(str(int(block[i,j])))
    return checksum.hexdigest()[:4]

def embed_checksum(block):
    size = int(math.sqrt(block.size))
    wm_checksum = "{0:016b}".format(int(checksum(block),16))
    for i in range(size):
        block[size-1,i] = block[size-1,i] - block[size-1,i] % 4
        block[size-1,i] += int(wm_checksum[2*i:2*(i+1)],2)
    return block

def errors_occured(block,original_checksum,size=8):
    if isinstance(original_checksum,int) == False:
        try:
            original_checksum = int(original_checksum,2)
        except ValueError:
            original_checksum = int(original_checksum,16)
    retrieved_checksum = int(checksum(block,size),16)
    if retrieved_checksum == original_checksum:
        return False
    else:
        return True


def print_LSB(block):
    answer = ""
    for i in range(size):
        for j in range(size):
            pixel = block[i,j] % 4 # seting 2 last bit to 0
            answer += str(int(pixel))
    print answer
    return answer


