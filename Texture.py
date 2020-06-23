import mahotas as mt
import cv2
from os import listdir
import matplotlib.pyplot as plt
import numpy as np

class Texture:

    def __init__(self):
        self.colors = ['r','g','b','y']
    
    def channels(self,img):
        red = np.zeros(img.shape)
        green = np.zeros(img.shape)
        blue = np.zeros(img.shape)
        gray = np.zeros(img.shape)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                red[i,j,0] = img[i,j,0]
                green[i,j,1] = img[i,j,1]
                blue[i,j,2] = img[i,j,2]
                gp = int(sum(img[i,j,:])/3)
                gray[i,j,0] = gp
                gray[i,j,1] = gp
                gray[i,j,2] = gp
        return red,green,blue,gray

    def haralick_features(self,img):
        textures = mt.features.haralick(img)
        features = textures.mean(axis=0)
        return features
    
    def analize(self,images,selected_feature):
        features = []
        for img in images:
            feat = self.haralick_features(img)
            features.append(feat[selected_feature])
        return features
    
    def plot(self,data):
        x = list(range(len(data)))
        plt.plot(x,data,self.colors[0],label="Feature")
        plt.title("Haralick Feature")
        plt.legend()
        plt.show()