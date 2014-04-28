from metrics import fractal

myFractal = fractal()
obraz = myFractal.open_img_PGM('pepper.pgm')
transform_list = myFractal.compression(4,obraz)
myFractal.decompression(transform_list,[256,256],4)
