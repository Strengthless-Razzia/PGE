# import the required library
import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys
  
  
# read the image
img = cv2.imread(sys.argv[1])
  
# convert image to gray scale image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
# detect corners with the goodFeaturesToTrack function.
corners = cv2.goodFeaturesToTrack(gray, 27, 0.01, 10)
corners = np.int0(corners)
  


line1 = [(79/36),-198.25] # a b
line2 = [28,-58]
line3 = [15,20]

lines = [line1,line2,line3]


for i in corners:
    color = (255,0,0)
    x, y = i.ravel()

    # test appartenance à une ligne
    for line in lines:
        a = line[0]
        b = line[1]

        if (-a*x+y-b==0):
            print("le point suivant appartient à une ligne x:"+str(x)+"  y:"+str(y))
            #cv2.line(img,(1,int(a-b)),(50,int(50*a-b)),(0,255,0),3);
            color = (0,0,255)


    cv2.circle(img, (x, y), 3, color, -1)

plt.imshow(img), plt.show()

