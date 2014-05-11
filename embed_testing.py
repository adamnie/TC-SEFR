from embed import *
import numpy as np
d = {}
d['x'] = 30
d['y'] = 14
d['t'] = 4
d['s'] = -24
d['o'] = 18

B = [1,20,3,54,6,3]
C = [1,2,3,25,6,3]

block = np.arange(64).reshape([8,8])
block2 = np.arange(121).reshape([11,11])
wm_block = embed_watermark(block,d,B,C)
checked_block = embed_checksum(wm_block)
data = retrieve_watermark_and_checksum(checked_block)
print errors_occured(checked_block,data)

print checksum(block2)
