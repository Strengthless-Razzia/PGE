# needed libraries
from random import random
from cv2 import rotate
import numpy as np
import math 
import matplotlib.pyplot as plt



def rotate2dPoints(points, alpha):
    # angle of rotation 10 degrees
    alpha = -alpha*math.pi/180
    # calculating "center of gravity" = rotation point 
    mean = np.mean(points,axis=0)
    X_mean = mean[0]
    Y_mean = mean[1]
    # subtracting mean from original coordinates and saving result to X_new and Y_new 
    X_new = []
    Y_new = []
    for i in range(len(points)):
        X_new.append(points[i,0] - X_mean)
        Y_new.append(points[i,1] - Y_mean)
    # rotating coordinates from which mean has been subtracted
    X_apu = []   #temporary help variable
    Y_apu = []   #temporary help variable
        
    for i in range(len(points)):
        X_apu.append(math.cos(alpha)*X_new[i]-math.sin(alpha)*Y_new[i])
        Y_apu.append(math.sin(alpha)*X_new[i]+math.cos(alpha)*Y_new[i])
            
    # adding mean back to rotated coordinates
    X_new = X_apu + X_mean
    Y_new = Y_apu + Y_mean

    newPoints = np.zeros([len(X_new),2])
    newPoints[:,0] = X_new
    newPoints[:,1] = Y_new
    return newPoints

def generateNewGrid():
    X = []
    Y = []
    startX = random() * 1000
    startY = random() * 1000
    step = 10

    for i in range(8):
        for j in range(5):
            X.append(startX + i*step)
            Y.append(startY + j*step)
    newPoints = np.zeros([len(X),2])
    newPoints[:,0] = X
    newPoints[:,1] = Y
    np.random.shuffle(newPoints)
    return newPoints

def sortPoints(points, sortAxis = 0):
    sortedPoints = np.zeros([0,2])
    while len(points) > 0:
        temp=-1
        for i in range(len(points)):
            if points[i,sortAxis] >= temp:
                temp = points[i,sortAxis]
                foundIndex=i

        sortedPoints=np.vstack((sortedPoints,points[foundIndex,:]))
        points = np.delete(points,foundIndex,axis=0)
    return sortedPoints
        

def getAlignement(points):
    sortedOnX = sortPoints(points,0)
    sortedOnY = sortPoints(points,1)
    pointsAlignment = abs(sortedOnY[0][1] - sortedOnY[7][1])
    direction = abs(sortedOnY[0][0]-sortedOnX[0][0])<=abs(sortedOnY[0][0]-sortedOnX[-1][0]) #Renvoie False si il faut tourner en negatif, True sinon 
    return pointsAlignment, direction
    

with open('HoleDetection\Points3D\Plaque1.npy', 'rb') as f:
    picked_points_Ro = np.load(f, allow_pickle=False)

grid = generateNewGrid()    
newGrid =rotate2dPoints(grid,(random()*90-45))

[flatness, dir] = getAlignement(newGrid)
print flatness, dir
# plotting data
plt.scatter(newGrid[:,0], newGrid[:,1], c='b', marker='x', label='1')
plt.scatter(grid[:,0], grid[:,1], c='r', marker='s', label='-1')
plt.show()