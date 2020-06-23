import statistics
import matplotlib.pyplot as plt
import numpy as np
import cv2
from Texture import Texture
from Slicer import Slicer
from Threshold import Threshold

tex = Texture()
ims = Slicer()
th = Threshold()

img = cv2.imread("000475.jpg")
img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		
images,coords = ims.split(img,50,50,50,50)

'''i=0
for img in images:
    if(i%2==0):
        cv2.rectangle(img, (0,0),(50,50), (225,105,65), 2)
        cv2.imwrite('img'+str(i)+'.jpg',img)
    i+=1'''

l = tex.analize(images,3)

mean_l = statistics.mean(l)
std_l = statistics.stdev(l)

print(mean_l)
print(std_l)

x = list(range(0,len(l)))

top = max(l)-mean_l

plt.plot(x,l,linestyle='-', marker='o', color='c')

plt.plot(x,len(l)*[mean_l],'g')

plt.plot(x,len(l)*[std_l],'b')

for l1 in l:
    print(l1)

for p,i,c in zip(l,images,coords):
    if(p>mean_l and p<top):
        cv2.rectangle(img, (c[0],c[2]), (c[1],c[3]), (0,255,0), 2)

cv2.imshow('image',img)
plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()