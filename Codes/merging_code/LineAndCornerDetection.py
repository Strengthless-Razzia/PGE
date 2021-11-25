"""
@file LineAndCornerDetection.py
@brief Ce programme fusionne la detection de ligne de Hough avec la detection d'angle de Harris. 
Permet d'obtenir une detection d'angle renforcé pouvant etre utilisee pour la localisation d'un objet 3D type plaque.
"""
from matplotlib import pyplot as plt
import numpy as np
import cv2 as cv
import math
import sys
import os

from HoughLineDetection import *
from cornerDetection import *

def displayCorner(imgPath, lines):
    img = cv.imread(imgPath)
    corners = getHarrisCorner(img)
    nbPointCorrele = 0

    # Array de couleur:
    couleur = [ 
        [0,255,255],
        [255,0,0],
        [255,255,0],
        [255,0,255],
        [126,126,126],
        [126,0,126],
        [0,126,126],
        [0,0,126],
        [50,0,0],
        [0,50,0],
        [0,0,50],
        [0,50,50],
        [50,50,0],
        [50,0,50],
        [255,50,0],
        [0,255,50],
        [50,0,255],
        [255,0,50],
        [0,50,255],
        [50,255,0],
        [126,0,50],
        [50,0,126],
        [50,126,0],
        [126,50,0],
        [0,126,50],
        [0,50,126],
        [75,255,40]
    ]
    compteurCouleur = 0

    for i in corners:
        isPart = False
        x, y = i.ravel()

        lastLine = 0
        # test appartenance à une ligne parmis une liste de lignes
        for line in lines:
            if(isPartOfLine(equationDroite(line),[x,y],0,2)==True):
                isPart = True
                lastLine = line
                break

        if isPart == True:
            color = couleur[compteurCouleur]
            nbPointCorrele = nbPointCorrele + 1
            cv.circle(img, (x, y), 3, color, -1)
            cv.line(img, (int(lastLine[0]),int(lastLine[1])), (int(lastLine[2]),int(lastLine[3])), color, 1, cv.LINE_AA)
            compteurCouleur = compteurCouleur + 1
        else:
            color = (0,0,255)
            cv.circle(img, (x, y), 3, color, -1)


    print(str(nbPointCorrele) + " sur " + str(corners.size/2))
    
    cv.imshow("CornerDisplay",img)
    cv.waitKey()


if __name__ == "__main__":
    #For all img files in directory dataset
    listOfFiles = os.listdir("Codes/merging_code/dataset")
    for f in listOfFiles:
        if ".png" in f or ".jpg" in f:
            a_t = 0.5
            b_t = 5
            imgPath = "Codes/merging_code/dataset/"+f

            lines = getHoughLines(imgPath)
            
            old = lines.shape
            mergedList=mergeSimilarLines(lines,a_t,b_t)
            
            new = mergedList.shape
            while new!= old:
                old = mergedList.shape
                mergedList=mergeSimilarLines(mergedList,a_t,b_t)
                new = mergedList.shape
            cleanedList = removeSimilarLines(mergedList,10)

            displayImgWithLines(imgPath, cleanedList, "Cleaned")
            displayHarrisCorner(imgPath)
            displayCorner(imgPath,cleanedList)

