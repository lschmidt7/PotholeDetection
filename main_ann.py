# verificar a feature 11 (pode ser a representação do não buraco)

from Texture import Texture
import cv2
from Slicer import Slicer
from os import listdir
from Threshold import Threshold
from tensorflow.keras.models import model_from_json
from Hog import Hog
from Boxes import Boxes, Box
from Cells import Cells
from timeit import default_timer as timer
from multiprocessing import Pool
from Config import Config
from Video import Video
import pickle
from Network import Network

#---------------------- PARAMETERS ----------------------#
threads = 1

path = "data/frames/frames0/"
path_out = "data/frames/out_frames0/"

sizew=25
sizeh=25

thresh = 0.5

haralick_feature = 3

hog_block_size = 2
hog_cell_size = 16
hog_orientations = 5

resize_img = (100,100)
#---------------------- PARAMETERS ----------------------#



#------------------- CONST & OBJECTS --------------------#

imgs_list = []

files = list(listdir(path))
batch_size = int(len(files)/threads)

vid = Video()

#------------------- CONST & OBJECTS --------------------#

def tracker(i):
	boxes = Boxes(len(files))
	tex = Texture()
	ims = Slicer()
	th = Threshold()
	hog = Hog()
	cells = Cells(sizeh,sizew)

	names = list(listdir(path))
	names = names[i:i+batch_size]

	net = Network()
	net.load('data/net/dataset_184_nets_ann/','compile_config.txt',hog_block_size,hog_cell_size,hog_orientations)

	index = 0

	while(len(names)>0):
		
		index = len(names)-1
		name = names.pop()

		img = cv2.imread(path+name)
		img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		
		images,coords = ims.split(img_grey,sizeh,sizew,sizeh,sizew)
		signal = tex.analize(images,haralick_feature)
		indexes = th.threshold_mean(signal)
		#coords_f = []
		#for x in indexes:
		#	coords_f.append(coords[x])
		coords = coords[indexes]
		coords = cells.group(coords)
		coords = cells.reorganize_coords(coords)
		
		for c in coords:
			part_img = img_grey[c[2]:c[3],c[0]:c[1]]
			part_img = cv2.resize(part_img,resize_img)
			part = hog.runOne(part_img,orient=hog_orientations,pixels=hog_cell_size,cells=hog_block_size)
			part = part.reshape((1,part.shape[0]))
			Y = net.predict(part)[0,0]
			if(Y>thresh and c[0]!=0 and c[1]!=500 and abs(c[0]-c[1])*abs(c[2]-c[3])>625 ):
				cells.box2(img,c)
				box = Box()
				box.box = [c[0],c[2],c[1],c[3]]
				boxes.add(index,box)
		cv2.imwrite(path_out+name,img)
	boxes.save('boxes_predicted_ann_25.b')

if __name__ == '__main__':
	i=0
	pos = []
	for t in range(threads):
		pos.append(i*batch_size)
		i+=1
	ti = timer()
	with Pool(threads) as p:
		p.map(tracker, pos)
	print(timer()-ti)