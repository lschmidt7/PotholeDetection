import numpy as np
import os
import cv2
from skimage.feature import hog
import time

class Hog():

    def __init__(self):
        self.X = []

    def run(self,imgs,orient=9,pixels=8,cells=3):
        for img in imgs:
            norm = hog(
                img,
                orientations=orient,
                pixels_per_cell=(pixels, pixels),
                cells_per_block=(cells, cells),
                block_norm="L2"
            )
            self.X.append(norm)
        return np.array(self.X)
    
    def runOne(self,img,orient=9,pixels=8,cells=3):
        norm = hog(
                img,
                orientations=orient,
                pixels_per_cell=(pixels, pixels),
                cells_per_block=(cells, cells),
                block_norm="L2"
            )
        return norm