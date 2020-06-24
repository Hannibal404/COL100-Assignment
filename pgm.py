# name: File path of the pgm image file
# Output is a 2D list of integers
from math import sqrt


def readpgm(name):
	image = []
	with open(name) as f:
		lines = list(f.readlines())
		if len(lines) < 3:
			print("Wrong Image Format\n")
			exit(0)

		count = 0
		width = 0
		height = 0
		for line in lines:
			if line[0] == '#':
				continue

			if count == 0:
				if line.strip() != 'P2':
					print("Wrong Image Type\n")
					exit(0)
				count += 1
				continue

			if count == 1:
				dimensions = line.strip().split(' ')
				print(dimensions)
				width = dimensions[0]
				height = dimensions[1]
				count += 1
				continue

			if count == 2:	
				allowable_max = int(line.strip())
				if allowable_max != 255:
					print("Wrong max allowable value in the image\n")
					exit(0)
				count += 1
				continue

			data = line.strip().split()
			data = [int(d) for d in data]
			image.append(data)
	return image	

# img is the 2D list of integers
# file is the output file path
def writepgm(img, file):
	with open(file, 'w') as fout:
		if len(img) == 0:
			pgmHeader = 'p2\n0 0\n255\n'
		else:
			pgmHeader = 'P2\n' + str(len(img[0])) + ' ' + str(len(img)) + '\n255\n'
			fout.write(pgmHeader)
			line = ''
			for i in img:
				for j in i:
					line += str(j) + ' '
				line += '\n'
			fout.write(line)
def avg_filter(image):
	avim=[]
	for i in image:
		avim.append(i[:])
	i=1
	while i <len(image)-1:
		j=1
		while j <len(image[0])-1:
			avim[i][j]=(image[i-1][j-1]+image[i-1][j]+image[i-1][j+1]+image[i][j-1]+image[i][j]+image[i][j+1]+image[i+1][j-1]+ image[i+1][j]+image[i+1][j+1])//9
			j+=1
		i+=1
	return avim
def edge_det(image):
	x1=[[0 for i in range(len(image[0])+2)]]
	grad=[[0 for i in range(len(image[0])+2)] for j in range (len(image)+2)]
	hdif=[[0 for i in range(len(image[0])+2)] for j in range (len(image)+2)]
	vdif=[[0 for i in range(len(image[0])+2)] for j in range (len(image)+2)]
	for i in range(len(image)):
		x1.append([0]+image[i][:]+[0])
	x1.append([0 for i in range(len(image)+2)])

	for i in range(1,len(x1)-1):
		for j in range(1,len(x1[0])-1):
			hdif[i][j]=x1[i-1][j-1] - x1[i-1][j+1] + (2*(x1[i][j-1]-x1[i][j+1])) + x1[i+1][j-1] - x1[i+1][j+1]
			vdif[i][j]=x1[i-1][j-1] - x1[i+1][j-1] + (2*(x1[i-1][j]-x1[i+1][j])) + x1[i-1][j+1] - x1[i+1][j+1]
			grad[i][j]=int(sqrt((hdif[i][j]**2) + (vdif[i][j]**2)))

	M=0
	for i in range(len(x1)):
		M=max(M,max(grad[i]))

	for i in range(len(x1)):
		for j in range(len(x1[0])):
			grad[i][j]=(grad[i][j]*255)//M
	g1=[]
	for i in range(1,len(grad)-1):
		g1.append(grad[i][1:len(grad[i])-1])	
	return g1
def mpath(f,a,i,j):
	if i==1:
		if j==0:
			if len(a[i])>1:
				m=min(a[i-1][j],a[i-1][j+1])
				if a[i-1][j]==m:
					f[i-1][j]=255
				if a[i-1][j+1]==m:
					f[i-1][j+1]=255
			else:
				f[i-1][j]=255
		elif 0<j<len(a)-1:
			m=min(a[i-1][j-1],a[i-1][j],a[i-1][j+1])
			if a[i-1][j-1]==m:
				f[i-1][j-1]=255
			if a[i-1][j]==m:
				f[i-1][j]=255
			if a[i-1][j+1]==m:
				f[i-1][j+1]=255
		else:
			m=min(a[i-1][j],a[i-1][j-1])
			if a[i-1][j]==m:
				f[i-1][j]=255
			if a[i-1][j-1]==m:
				f[i-1][j-1]=255
	else:
		if j==0:
			if len(a[i])>1:
				m=min(a[i-1][j],a[i-1][j+1])
				if a[i-1][j]==m:
					f[i-1][j]=255
					mpath(f,a,i-1,j)
				if a[i-1][j+1]==m:
					f[i-1][j+1]=255
					mpath(f,a,i-1,j+1)
			else:
				f[i-1][j]=255
				mpath(f,a,i-1,j)
		elif 0<j<len(a)-1:
			m=min(a[i-1][j-1],a[i-1][j],a[i-1][j+1])
			if a[i-1][j-1]==m:
				f[i-1][j-1]=255
				mpath(f,a,i-1,j-1)
			if a[i-1][j]==m:
				f[i-1][j]=255
				mpath(f,a,i-1,j)
			if a[i-1][j+1]==m:
				f[i-1][j+1]=255
				mpath(f,a,i-1,j+1)
		else:
			m=min(a[i-1][j],a[i-1][j-1])
			if a[i-1][j]==m:
				f[i-1][j]=255
				mpath(f,a,i-1,j)
			if a[i-1][j-1]==m:
				f[i-1][j-1]=255
				mpath(f,a,i-1,j-1)

def MinEnergyPath(im):
	x=edge_det(im)
	final=[]
	for i in im:
		final.append(i[:])
	MinEnergy=[[0 for i in range(len(x[0]))]for j in range(len(x))]
	for i in range(len(x[0])):
		MinEnergy[0][i]=x[0][i]
	for i in range(1,len(x)):
		for j in range(1,len(x[0])-1):
			MinEnergy[i][j] = x[i][j] + min(MinEnergy[i-1][j-1], MinEnergy[i-1][j], MinEnergy[i-1][j+1])
		MinEnergy[i][0] = x[i][0] + min(MinEnergy[i-1][0], MinEnergy[i-1][1])
		MinEnergy[i][-1]=MinEnergy[i][-1] = x[i][-1] + min(MinEnergy[i-1][-2], MinEnergy[i-1][-1])
	minen=min(MinEnergy[-1])

	for j in range(len(MinEnergy[-1])):
		if MinEnergy[-1][j]==minen:
			final[-1][j]=255
			mpath(final,MinEnergy,len(MinEnergy)-1,j)

	return final





########## Function Calls ##########
x = readpgm('test.pgm')		# test.pgm is the image present in the same working directory

writepgm(edge_det(x),'edge.pgm')
writepgm(MinEnergyPath(x),'minpath.pgm')
writepgm(avg_filter(x),'avg.pgm')
writepgm(x, 'test_o.pgm')		# x is the image to output and test_o.pgm is the image output in the same working directory
###################################