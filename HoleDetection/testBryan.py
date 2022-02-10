from matUtils import *
import numpy as np
import cv2

i = 0
j = 0
ok = True
while ok:
    v = np.random.normal(scale=1000.,size=(3,1))
    R = cv2.Rodrigues(v)[0]
    i = i+1
    if i == 10000:
        j=j+1
        print(j)
        i=0
    if(np.isclose(bryant_to_R(R_to_bryant(R)),R).all()==True):
        pass
    else:
        ok = False
        print(R)
        print(R_to_bryant(R))