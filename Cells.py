import numpy as np
import cv2

class Cells():
	
	def __init__(self,sizew,sizeh):
		self.sizew = sizew
		self.sizeh = sizeh

	def isNeighbour(self,b1,b2):
		if(b1[0]==b2[0] and b1[1]==b2[1] and abs(b1[2]-b2[2])==self.sizeh and abs(b1[3]-b2[3])==self.sizeh):
			return True
		if(b1[2]==b2[2] and b1[3]==b2[3] and abs(b1[0]-b2[0])==self.sizew and abs(b1[1]-b2[1])==self.sizew):
			return True
		return False

	def group(self,cells):
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
					if(self.isNeighbour(lista_flood[i],c)):
						if(list(c) not in lista_flood):
							lista_flood.append(list(c))
				for x in lista_flood:
					if(x in cells):
						cells.remove(x)
				i+=1
			groups.append(lista_flood)
		return groups

	def reorganize_coords(self,coords):
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

	def box(self,img,indexes,coords):
		for c in indexes:
			cv2.rectangle(img, (coords[c][0],coords[c][2]),(coords[c][1],coords[c][3]), (0,255,0), 2)
	
	def box1(self,img,coords):
		for c in coords:
			cv2.rectangle(img, (c[0],c[2]),(c[1],c[3]), (0,255,0), 2)
	
	def box2(self,img,c):
		cv2.rectangle(img, (c[0],c[2]), (c[1],c[3]), (0,255,0), 2)