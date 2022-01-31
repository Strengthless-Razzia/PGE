# needed libraries
from random import random
import cv2 as cv
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

def generateNewGrid(deletion = False, amountToDelete = 5):
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
    if deletion:
        for i in range(amountToDelete):
            newPoints = np.delete(newPoints,0,axis=0)
    return newPoints

def sortPoints(points, sortAxis = 0):
    sortedPoints = np.zeros([0,2])
    while len(points) > 0:
        foundIndex = -1
        temp=-1
        for i in range(len(points)):
            if points[i,sortAxis] >= temp:
                temp = points[i,sortAxis]
                foundIndex=i
        if foundIndex != -1:
            sortedPoints=np.vstack((sortedPoints,points[foundIndex,:]))
        points = np.delete(points,foundIndex,axis=0)
    return sortedPoints


def findMarkPosition(imgPath, debug = True):
    im = cv.imread(imgPath, cv.IMREAD_GRAYSCALE)
    _,im = cv.threshold(im,50,256,cv.THRESH_BINARY)
    params = cv.SimpleBlobDetector_Params() 

    params.minDistBetweenBlobs = 10
    params.minRepeatability = 1
    params.minThreshold = 0
    params.maxThreshold = 10
    params.filterByArea = True
    params.minArea = 20
    params.maxArea = 500000

    params.filterByCircularity = False
    params.minCircularity = 0.7
    params.maxCircularity = 0.8

    params.filterByConvexity = False
    params.minConvexity = 0.87

    params.filterByInertia = False
    params.minInertiaRatio = 0.01
    
    detector = cv.SimpleBlobDetector_create(params)
    keypoints = detector.detect(im)
    if debug:
        # Show keypoints
        im_with_keypoints = cv.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        im_with_keypoints = cv.resize(im_with_keypoints,(1000,1000))
        cv.imshow("Keypoints", im_with_keypoints)
        cv.waitKey(0)
    x = keypoints[0].pt[0]
    y = keypoints[0].pt[1]

    return (x,y)
        

with open('HoleDetection\Points3D\Plaque1.npy', 'rb') as f:
    picked_points_Ro = np.load(f, allow_pickle=False)

print(findMarkPosition("HoleDetection\ShittyDataset\image3.bmp"))

#
# while True:
    #print "Nouvelle grille"
    #grid = generateNewGrid(True,5)    
    #newGrid =rotate2dPoints(grid,(random()*360-180))

    #straightGrid=getPointsStraight(newGrid,grid, 0.05,display=True)