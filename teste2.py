import cv2

im = cv2.imread("data/frames/frames0/000212.jpg")
cv2.rectangle(im,(50,50),(50,50),(0,255,0),1)
cv2.imshow('sdfad',im)
cv2.waitKey(0)
cv2.destroyAllWindows()