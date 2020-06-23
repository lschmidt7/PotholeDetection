# -*- coding: utf-8 -*-
'''
Autor: Leonardo de Abreu Schmidt
Data inicio: 10/02/2017
Versão: 1.0
'''

import PIL
from PIL import Image
import PIL.ImageOps

class Imagem:

	def __init__(self):
		self.img = None
		self.pixels2 = []
		self.matrix = []
		self.size = (0,0)

	def new(self,w,h):
		self.img = Image.new('RGB', (w,h), "white") # create a new black image
		self.size = (w,h)

	def resize(self,basewidth,hsize):
		self.img = self.img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
		self.size = (basewidth,hsize)

	def save(self,name):
		self.img.save(name)

	def open(self,name):
		self.img = Image.open(name)
		self.size = self.img.size

	def show(self):
		self.img.show()

	def getSize(self):
		return self.img.size

	def load(self):
		self.pixels2 = self.img.load()

	def greyScale(self):
		self.img = self.img.convert('L')

	def vectorize(self):
		pixels = []
		for w in range(self.img.size[0]):
			for h in range(self.img.size[1]):
				g = self.img.getpixel((w,h))
				pixels.append(g)
		return pixels
	
	def inverse(self):
		self.img = PIL.ImageOps.invert(self.img)

	def toMatrix(self):
		px = []
		for w in range(self.img.size[0]):
			px = []
			for h in range(self.img.size[1]):
				g = self.img.getpixel((w,h))
				px.append(g)
			self.matrix.append(px)
		return self.matrix

	def setMatrix(self,matrix):
		for i in range(self.img.size[0]):
			for j in range(self.img.size[1]):
				self.pixels2[i,j] = matrix[i][j]

	def vectorToMatrix(self,vector):
		for i in range(self.img.size[0]):
			for j in range(self.img.size[1]):
				self.pixels2[i,j] = (vector[i * self.img.size[1] + j], vector[i * self.img.size[1] + j], vector[i * self.img.size[1] + j])

	def clear(self):
		self.load()
		for i in range(self.img.size[1]):
			for j in range(self.img.size[0]):
				if(self.pixels2[j,i] > 150):
					self.pixels2[j,i] = 255
				else:
					self.pixels2[j,i] = 0

	def cropHeight(self,val):
		b = False
		pos = 0
		i = 0
		for h in range(self.img.size[1]):
			for w in range(self.img.size[0]):
				if(self.img.getpixel((w,h)) > val and b == False):
					b = True
					pos = i
			i+=1
		self.img = self.img.crop((0,pos,self.img.size[0],self.img.size[1]))
		b = False
		i = self.size[1] - pos
		pos = 0
		for h in reversed(range(self.img.size[1])):
			for w in range(self.img.size[0]):
				if(self.img.getpixel((w,h)) > val and b == False):
					b = True
					pos = i
			i-=1
		self.img = self.img.crop((0,0,self.img.size[0],pos))

	def cropWidth(self,val):
		b = False
		pos = 0
		i = 0
		for w in range(self.img.size[0]):
			for h in range(self.img.size[1]):
				if(self.img.getpixel((w,h)) > val and b == False):
					b = True
					pos = i
			i+=1
		self.img = self.img.crop((pos,0,self.img.size[0],self.img.size[1]))
		b = False
		i = self.size[0] - pos
		pos = 0
		for w in reversed(range(self.img.size[0])):
			for h in range(self.img.size[1]):
				if(self.img.getpixel((w,h)) > val and b == False):
					b = True
					pos = i
			i-=1
		self.img = self.img.crop((0,0,pos,self.img.size[1]))

	def cropMargin(self):
		val = 20
		self.cropWidth(val)
		self.cropHeight(val)


		'''img = cv2.imread('000041.jpg')

		#blur = cv2.bilateralFilter(img,1,75,50)
		#blur = cv2.GaussianBlur(img,(3,3),0)
		#blur = cv2.blur(img,(9,9))
		#kernel = np.ones((5,5),np.float32)/25
		#blur = cv2.filter2D(img,-1,kernel)
		blur = cv2.medianBlur(img,5)
		
		cv2.imshow('',blur)
		cv2.waitKey(0)
		cv2.destroyAllWindows()'''