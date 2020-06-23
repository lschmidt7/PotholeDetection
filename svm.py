# verificar a feature 11 (pode ser a representação do não buraco)

from Texture import Texture
import cv2
from Slicer import Slicer
from os import listdir
from Threshold import Threshold
from Hog import Hog
from Boxes import Boxes, Box
from Cells import Cells
from timeit import default_timer as timer
from multiprocessing import Pool
from Config import Config
import pickle

#---------------------- PARAMETERS ----------------------#
threads = 1

path = "data/frames/frames0/"
path_out = "data/frames/out_frames0/"

sizew=25
sizeh=25

thresh = 0.6

haralick_feature = 3

hog_block_size = 2
hog_cell_size = 8
hog_orientations = 2

resize_img = (100,100)

size_video = (500,200)
#---------------------- PARAMETERS ----------------------#



#------------------- CONST & OBJECTS --------------------#

files = list(listdir(path))
batch_size = int(len(files)/threads)

#------------------- CONST & OBJECTS --------------------#

def tracker(i):
	boxes = Boxes(len(files))
	tex = Texture()
	ims = Slicer()
	th = Threshold()
	cells = Cells(sizeh,sizew)

	names = list(listdir(path))
	names = names[i:i+batch_size]
	
	
	f = open('svmsemhog.svm','rb')
	clf = pickle.load(f)
	f.close()

	while(len(names)>0):
		index = len(names)-1
		name = names.pop()

		img = cv2.imread(path+name)
		img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		images,coords = ims.split(img_grey,sizeh,sizew,sizeh,sizew)
		signal_p = tex.analize(images,haralick_feature)
		indexes = th.threshold_mean(signal_p)
		coords_f = []
		for x in indexes:
			coords_f.append(coords[x])

		coords = cells.group(coords_f)
		coords = cells.reorganize_coords(coords)
		for c in coords:
			part_img = img_grey[c[2]:c[3],c[0]:c[1]]
			part_img = cv2.resize(part_img,resize_img).flatten()
			print(part_img)
			input()
			Y = clf.predict(part_img)
			if(Y>thresh and c[0]!=0 and c[1]!=500 and abs(c[0]-c[1])*abs(c[2]-c[3])>625 ):
				cells.box2(img,c)
				box = Box()
				box.box = [c[0],c[2],c[1],c[3]]
				boxes.add(index,box)
		cv2.imwrite(path_out+name,img)
	boxes.save('boxes_predicted_svm.b')

if __name__ == '__main__':
	i=0
	tracker(i)
	'''pos = []
	for t in range(threads):
		pos.append(i*batch_size)
		i+=1
	ti = timer()
	with Pool(threads) as p:
		p.map(tracker, pos)
	print(timer()-ti)'''