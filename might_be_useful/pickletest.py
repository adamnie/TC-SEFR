#pickletest.py

import pickle

a = {'hello': 'world'}

with open('filename.pickle', 'wb') as handle:
  pickle.dump(a, handle)

with open('filename.pickle', 'rb') as handle:
  b = pickle.load(handle)

print a == b



#gettest.py
# print imageC.get({"x1":0, "x2":8, "y1":0, "y2":8})

# test = imageA.cutsquare(0,0,8).view(wm_img)
# print test

# aco = np.arange(9)
# aco = np.reshape(aco, (3,3))
# aco = wm_img(aco.view(img))

# list = {"x" : 5, "y" : 5}
# test.save(aco,list)

# print test