from matUtils import *
import numpy as np
import cv2

#vec = np.pi*2*np.array([[1.],[1.],[1.]])/(3*np.sqrt(3))
vec = np.array([[np.pi/2],[np.pi/2],[np.pi/2]])
print(vec)
print(cv2.Rodrigues(vec)[0])
print(R_to_bryant(cv2.Rodrigues(vec)[0]))
print(angle_to_R((np.pi/2,np.pi/2,0)))