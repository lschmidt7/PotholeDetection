import cv2
from math import floor
from os import listdir
import numpy as np
import random
import math
from sklearn.utils import shuffle
from PIL import Image

class Slicer():

    def __init__(self):
        pass
    
    def split(self,img_array,bw,bh,stridew,strideh):
        total_width = floor(img_array.shape[0] / strideh)
        total_height = floor(img_array.shape[1] / stridew)
        sub_images = []
        coords1 = []
        for x in range(total_width):
            x_ini = x*strideh
            x_fim = x*strideh+bw
            if(x_fim>img_array.shape[0]):
                diff = x_fim-img_array.shape[0]
                x_ini -= diff
                x_fim -= diff
            for y in range(total_height):
                y_ini = y*stridew
                y_fim = y*stridew+bh
                if(y_fim>img_array.shape[1]):
                    diff = y_fim-img_array.shape[1]
                    y_ini -= diff
                    y_fim -= diff
                sub_images.append(img_array[x_ini:x_fim,y_ini:y_fim])
                coords1.append([y_ini,y_fim,x_ini,x_fim])
        return np.array(sub_images), np.array(coords1)


    def isOverlapping(self,r1,r2):
        if(len(r2)==0):
            return False
        if ( r1[0] > r2[1] or r1[1] < r2[0]):
            return False
        if ( r1[2] > r2[3] or r1[3] < r2[2]):
            return False
        return True

    def OverlapArea(self,r1,r2):
        if(not self.isOverlapping(r1,r2)):
            return 0
        rs = r1
        if(r1[1]>r2[1]):
            r = r1
            r1 = r2
            r2 = r
        x_overlap = max(0, min(r1[1], r2[1]) - max(r1[0], r2[0]))
        y_overlap = max(0, min(r1[3], r2[3]) - max(r1[2], r2[2]))
        if((x_overlap * y_overlap)<=0):
            return 0
        v = (( (rs[1]-rs[0])*(rs[3]-rs[2]) )/(x_overlap * y_overlap))
        return 1/v