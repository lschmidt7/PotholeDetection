from Slicer import Slicer
from Texture import Texture
from Threshold import Threshold
import cv2
import matplotlib.pyplot as plt
import statistics


def transform(signal,media):
    for i in range(len(signal)):
        s = signal[i]
        if(s<=media):
            s=0
        signal[i] = s
    return signal

def media(signal):
    med = 0
    i=0
    for s in signal:
        if(s>0):
            med+=s
            i+=1
    return med/i

slicer = Slicer()
tex = Texture()
ths = Threshold()

img_p = cv2.imread("data/frames/frames0/000235.jpg")
img_n = cv2.imread("data/frames/frames0/000270.jpg")

imgs_p, coords = slicer.split(img_p,25,25,25,25)
imgs_n, coords = slicer.split(img_n,25,25,25,25)

# 1 - energia
# 2 - entropia
# 3 - correlação
# 5 - inércia

signal_p = tex.analize(imgs_p,1)[1:]
media_p = media(signal_p)
#signal_p = transform(signal_p,media_p)
#media_p = media(signal_p)
#signal_p = transform(signal_p,media_p)

#signal_n = tex.analize(imgs_n,3)[1:]
#media_n = media(signal_n)
#signal_n = transform(signal_n,media_n)
#media_n = media(signal_n)
#signal_n = transform(signal_n,media_n)

x = range(len(signal_p))
        

#plt.subplot(121)
#plt.plot(x,[media_p]*len(signal_p),'-r')
plt.plot(x,signal_p,'-c')
plt.plot(x,signal_p,'.b')
plt.xlabel("Célula do Grid",fontsize=15)
plt.ylabel("Haralick Value",fontsize=15)
plt.title("Energia",fontsize=20)

#plt.subplot(122)
#plt.plot(x,[media_n]*len(signal_n),'-r')
#plt.plot(x,signal_n,'-c')
#plt.plot(x,signal_n,'.b')

plt.show()