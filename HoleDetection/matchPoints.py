# needed libraries
from linecache import getline
from random import random
import cv2 as cv
import numpy as np
import math 
import matplotlib.pyplot as plt
import extractHoles


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
        foundIndex = -10000
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
    bordersize = 10
    im = cv.copyMakeBorder(
        im,
        top=bordersize,
        bottom=bordersize,
        left=bordersize,
        right=bordersize,
        borderType=cv.BORDER_CONSTANT,
        value=255
    )

    _,im = cv.threshold(im,50,256,cv.THRESH_BINARY)
    params = cv.SimpleBlobDetector_Params() 

    params.minDistBetweenBlobs = 10
    params.minRepeatability = 1
    params.minThreshold = 0
    params.maxThreshold = 10
    params.filterByArea = True
    params.minArea = 20
    params.maxArea = 500000

    params.filterByCircularity = True
    params.minCircularity = 0.4
    params.maxCircularity = 0.9

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
    if len(keypoints) != 0: 
        x = keypoints[0].pt[0]-bordersize
        y = keypoints[0].pt[1]-bordersize
        return (x,y)
    else:
        return (0,0)

def getHoughLines(img):
    """
    in :
        img : Path vers une image
    out:
        lines : array de N lignes {x1,y1,x2,y2}
        Return None si erreur de lecture de l'image
    Fonction generant les lignes Probabilistes de Hough
    """
    
    # Loads an image
    src = cv.imread(img, cv.IMREAD_GRAYSCALE)
    # Check if image is loaded fine
    if src is None:
        print ('Error opening image!')
        return None
    

    imgEdges = cv.Canny(src, 50, 200, None, 3)
    lines = cv.HoughLinesP(imgEdges, 1, np.pi / 180, 50, 2, 400, 200)
    #Enlever une dimension inutile de HoughLinesP pour faciliter l'utilisation de lines
    (x,y,z) = lines.shape
    lines = np.resize(lines, (x,z))
    i = 0
    while i < len(lines):
        if abs(lines[i,0]-lines[i,2])+abs(lines[i,1]-lines[i,3]) < 100:
            lines = np.delete(lines,i,axis=0)
        else:
            i+=1
    return lines

def getCenter(line):
    return ((int(line[0])+int(line[2]))/2, (int(line[1])+int(line[3]))/2)

def displayImgWithLines(img, lines, title):
    """
    in :
        img : Path vers une image
        lines : Array des lignes detectees sur une image 
        title : Titre de la fenetre d'affichage
    out:
        None
    Fonction affichant une image avec les lignes detectees dessus
    Bloque le deroulement jusqu'a la pression d'une touche du clavier
    """

    # Loads an image
    src = cv.imread(img, cv.IMREAD_GRAYSCALE)
    # Check if image is loaded fine
    if src is None:
        print ('Error opening image!')
        return -1   
    src = cv.cvtColor(src,cv.COLOR_GRAY2RGB)

    if lines is not None:
        for i in range(0, len(lines)):
            l = lines[i]
            cv.line(src, (int(l[0]), int(l[1])), (int(l[2]), int(l[3])), (0,0,255), 1, cv.LINE_AA)
            cv.circle(src,getCenter(l),5,(0,255,0))  

    src = cv.resize(src,(1000,1000))        
    cv.imshow(title,src)
    cv.waitKey()

def getLineEquation(line):

    if line[2]==line[0] :
        slope = -1
        b = -1   
    else:
        slope = (line[3]-line[1]) / (line[2]-line[0])
        b = line[1] - line[0]*slope

    return slope, b 

def getPerpendicularSlope(slope):
    if slope == -1:
        return 0
    elif slope == 0:
        return -1
    else:
        return -1/slope

def getSearchZone(line, slopePerp):
    line1_B = line[1] - line[0]*slopePerp
    line2_B = line[3] - line[2]*slopePerp
    
    return np.sort([line1_B, line2_B])

def isMarkCloseby(line, markX,markY):
    
    slope, posAtOrigin = getLineEquation(line)
    slopePerp = getPerpendicularSlope(slope)
    if slopePerp == -1:
        if markY <= max((line[1],line[3])) and markY >= min((line[1],line[3])):
            return True
        else:
            return False

    l_low,l_high = getSearchZone(line,slopePerp)

    if markY <= markX*slopePerp + l_high and markY >= markX*slopePerp + l_low:
        return True
    else:
        return False

def getLineDistanceToMark(line, markX,markY):

    a,b=getLineEquation(line)
    if a == -1:
        return abs(markX-line[0])
    return abs(markY - a*markX - b)/np.sqrt(1+a**2)

def displayUniqueLine(imgPath,foundLine,title):
    src = cv.imread(imgPath, cv.IMREAD_GRAYSCALE)
    src = cv.cvtColor(src,cv.COLOR_GRAY2RGB)
    cv.line(src, (int(foundLine[0]), int(foundLine[1])), (int(foundLine[2]), int(foundLine[3])), (0,0,255), 5, cv.LINE_AA)
    cv.circle(src,getCenter(foundLine),5,(0,255,0))  
    src = cv.resize(src,(1000,1000))        
    cv.imshow(title,src)
    cv.waitKey()

def detectClosestEdge(imgPath, markX,markY):
    lines = getHoughLines(imgPath)
    displayImgWithLines(imgPath,lines,"Before Traitement")
    i = 0
    while i < len(lines):
        if not isMarkCloseby(lines[i], markX,markY):
            lines = np.delete(lines,i,axis=0)
        else:
            i+=1
    displayImgWithLines(imgPath,lines,"afterwards")
    
    foundLineDistance = 9999999
    foundLine = None

    for currentLine in lines:
        currentDistance = getLineDistanceToMark(currentLine, markX,markY)


        if currentDistance<foundLineDistance:
            foundLine = currentLine
            foundLineDistance = currentDistance     
    if foundLine is None:
        print "not found"
        return None
    else:
        displayUniqueLine(imgPath,foundLine,"LineFound")
        return foundLine

def getLinesToFind(plaqueModelPath):
    with open('./Data/Plaque3/Model/Plaque_3.stp') as f:
        file = f.readlines()

    holeList = extractHoles.getAllCircles(file)
    holeList = np.delete(holeList,3,axis=1)
    holeList = np.delete(holeList,2,axis=1)
    
    sortedList = sortPoints(holeList, 1)
    print sortedList

def generatePointLines(imgPath,detectedPoints,plaqueModelPath):
    markX, markY = findMarkPosition(imgPath)
    foundLine = detectClosestEdge(imgPath,markX, markY)
    getLinesToFind(plaqueModelPath)


    #Labelliser les points
    #Remet l'image droite sans perdre les labels (?)
    #Reorganiser les points de haut en bas
    #quand ecart trop grand, considere que nouvelle ligne
    #reorganiser les lignes en X
    #inshallah on a pas perdu les labels, et on renvoie les listes de points originaux mais dans le bon ordre cette fois
    
    pass


generatePointLines("HoleDetection\ShittyDataset\image2.bmp",  None, "Data\Plaque1\Model\Plaque_1.stp")
#with open('HoleDetection\Points3D\Plaque1.npy', 'rb') as f:
#    picked_points_Ro = np.load(f, allow_pickle=False)

#for i in range(1,5):
#    markX, markY = findMarkPosition("HoleDetection\ShittyDataset\image%u.bmp"%i)
#    detectClosestEdge("HoleDetection\ShittyDataset\image%u.bmp"%i,markX, markY)
