input1 = open('hello.pgm','r')
output1 = open('inversed.pgm','w')

print ("haha")

pixels = []
output = []
picture = input1.readlines()
# int the third line the picture size (x,y) is saved first number of colums then number of rows
size = picture[2].split()

# in the fourth line theres number indicating white (0 is black)
whiteMAX = int(picture[3]) # casting char to int
pixels = picture[4:int(size[1])+4]
for line in range(0,len(pixels)):
	pixels[line] = pixels[line].split()


pixels = [val for subList in pixels for val in subList] #flattening list

pixels = [int(pixel) for pixel in pixels] # converting list elements to ints

pixels = [(15-pixel) for pixel in pixels] # inversing

lines = [pixels[x:x+int(size[0])] for x in range(0,len(pixels),int(size[0]))] # grouping pixels in lines(still as lists)

lines = [" ".join(map(str,line)) for line in lines] # join lists into strings
'\n'.join(lines) # joining pixel lines

output.append(picture[0]) # apending line with P2 (defining type simplifield PGM)
output.append(picture[1]) # apednign line with comment "# feep.pgm"
output.append(picture[2]) # line containing number of pixel colums and rows
output.append(picture[3]) # maximum value defining white
output.append(pixels) # appendign pixel list
'\n'.join(output)

output1.writelines(output)
