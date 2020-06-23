# verificar a feature 11 (pode ser a representação do não buraco)

from mahotas.features import haralick
import cv2
from Slicer import Slicer
from os import listdir
from tensorflow.keras.models import model_from_json
from Boxes import Boxes
from timeit import default_timer as timer
from multiprocessing import Pool
from Config import Config
import pickle
from Network import Network
import numpy as np
from skimage.feature import hog
import statistics

#---------------------- PARAMETERS ----------------------#
threads = 8

path = "data/frames/frames0/"
path_out = "data/frames/out_frames0/"

sizew=50
sizeh=50

thresh = 0.8

haralick_feature = 3

hog_block_size = 2
hog_cell_size = 16
hog_orientations = 5

resize_img = (100,100)
#---------------------- PARAMETERS ----------------------#



#------------------- CONST & OBJECTS --------------------#

files = list(listdir(path))
batch_size = int(len(files)/threads)

#------------------- CONST & OBJECTS --------------------#

def analize_and_threshold(images,selected_feature):
	features = []
	for img in images:
		features.append(haralick(img).mean(axis=0)[selected_feature])
	thresh_value = statistics.mean(features)
	indexes = []
	i=0
	for d in features:
		if(d>thresh_value):
			indexes.append(i)
		i+=1
	return indexes

def reorganize_coords(coords):
	boxes = []
	for g in coords:
		maxx=0
		minx=10000
		maxy=0
		miny=10000
		for c in g:
			if c[0]<minx:
				minx = c[0]
			if(c[1]>maxx):
				maxx = c[1]
			if c[2]<miny:
				miny = c[2]
			if(c[3]>maxy):
				maxy = c[3]
		boxes.append( [minx,maxx,miny,maxy] )
	return boxes

def isNeighbour(b1,b2):
	if(b1[0]==b2[0] and b1[1]==b2[1] and abs(b1[2]-b2[2])==sizeh and abs(b1[3]-b2[3])==sizeh):
		return True
	if(b1[2]==b2[2] and b1[3]==b2[3] and abs(b1[0]-b2[0])==sizew and abs(b1[1]-b2[1])==sizew):
		return True
	return False

def group(cells):
	groups = []
	cells_1 = []
	for x in cells:
		cells_1.append(list(x))
	cells = cells_1

	while(len(cells)>0):
		c = cells[0]
		lista_flood = [list(c)]
		cells.remove(c)
		i=0
		while(i<len(lista_flood)):
			for c in cells:
				if(isNeighbour(lista_flood[i],c)):
					if(list(c) not in lista_flood):
						lista_flood.append(list(c))
			for x in lista_flood:
				if(x in cells):
					cells.remove(x)
			i+=1
		groups.append(lista_flood)
	return groups

def tracker(imagens):
	ims = Slicer()

	net = Network()
	net.load('data/net/dataset_184_nets_ann/','compile_config.txt',2,16,2)

	for img in imagens:
		img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		
		images,coords = ims.split(img_grey,sizeh,sizew,sizeh,sizew)
		indexes = analize_and_threshold(images,haralick_feature)
		coords_f = []
		for x in indexes:
			coords_f.append(coords[x])
		coords = reorganize_coords(group(coords_f))
		for c in coords:
			part = hog(cv2.resize(img_grey[c[2]:c[3],c[0]:c[1]],resize_img),orientations=2,pixels_per_cell=(16,16),cells_per_block=(2,2),block_norm="L2")
			Y = net.predict(part.reshape((1,part.shape[0])))[0,0]
			if(Y>0.85 and c[0]!=0 and c[1]!=500 and abs(c[0]-c[1])*abs(c[2]-c[3])>625 ):
				cv2.rectangle(img, (c[0],c[2]), (c[1],c[3]), (0,255,0), 2)
		#cv2.imwrite(path_out+name,img)

if __name__ == '__main__':
	imagens = []
	images_groups = []
	names = list(listdir(path))
	for name in names:
		imagens.append(cv2.imread(path+name))
	for t in range(threads):
		images_groups.append(imagens[t*batch_size:t*batch_size+batch_size])
	ti = timer()
	with Pool(threads) as p:
		p.map(tracker, images_groups)
	print(540.0/(timer()-ti))