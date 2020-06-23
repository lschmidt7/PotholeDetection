import matplotlib.pyplot as plt
import random
from Texture import Texture
import cv2
from Slicer import Slicer

def derivate(signal):
    sigd = []
    for i in range(len(x)-1):
        sigd.append( abs (signal[i+1] - signal[i]) )
    return sigd

ims = Slicer()
tex = Texture()

# 000236.jpg
# 000212.jpg
img = cv2.imread("data/frames/frames0/000212.jpg")
img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

images,coords = ims.split(img_grey,50,50,50,50)
signal_p = tex.analize(images,3)

x = list(range(len(signal_p)))

yd = derivate(signal_p)

plt.plot(x,signal_p)
plt.plot(x[:-1],yd)
plt.show()