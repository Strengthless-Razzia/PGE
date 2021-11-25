"""
@file fusion.py
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

radius_point = 3
cred = (255,0,0)
cgreen = (0,255,0)
cblue = (0,0,255)
cyellow = (0,255,255)


def matchLinesPoints(imgPath,liste_lines):
    img = cv.imread(imgPath)

    points = getHarrisCorner(img)
    lines = liste_lines
    linesClean = np.array([])

    pointTrouve = False
    compteurPointTrouve = 0

    # Passage d'un tableau de ligne defini par deux points...
    # ...a un tableau de ligne defini par coeff directeur et ordonnee a l'origine
    for line in lines:
        linesClean = np.append(linesClean,equationDroite(line),axis=0)    
    
    # Mise sous forme de tableau 2 colonnes * N lignes
    # une ligne du tableau : [a,b] -> coeff directeur, ordonnee a l'origine
    s = int(linesClean.size/2)
    linesClean = linesClean.reshape(s,2) 
    lines = lines.reshape(s,4) # utile pour venir tracer une ligne ensuite en utilisant deux points et non les coeff <a> et <b>

    # A chaque <point> detecte par Harris's corner algorithm, calcule s'il appartient a une des droites de <linesClean>
    for point in points:
        for line in linesClean:
            if appartientDroite(point,line):
                index = np.where(lines == line) #TODO verifier si c'est bien trouver. Return array de toutes les positions possibles
                displayPointLine(point,lines[index[0][0]],img,cblue)
                pointTrouve = True
                compteurPointTrouve = compteurPointTrouve + 1
                break
        
        # Le point n'a pas ete trouve, il est affiche d'une couleur differente
        if pointTrouve == False:
            #displayPoint(point,img,cred)
            pass
            
        
        pointTrouve = False
        
    print(compteurPointTrouve)

def appartientDroite(point,line):

    x = point[0][0]
    y = point[0][1]

    a = line[0]
    b = line[1]

    e = y - a*x - b
    if (e == 0):
        return True
    else:
        return False


def displayPointLine(point,line,img,color):
    """
    in :
        point : point {x,y}
        line : lignes {x1,y1,x2,y2}
        img : image a afficher
        color : couleur utilisee pour point et line
    out:

    Fonction affichant un point et une ligne de la meme couleur
    """
    start_point = [line[0],line[1]]
    end_point = [line[2],line[3]]

    img = cv.circle(img, (point[0][0],point[0][1]), radius_point, color, -1)
    img = cv.line(img, start_point, end_point, color, 1)
    cv.imshow("PointLine",img)
    cv.waitKey()


def displayPoint(point,img,color):
    img = cv.circle(img, (point[0][0],point[0][1]), radius_point, color, -1)
    cv.imshow("Point",img)
    cv.waitKey()


if __name__ == "__main__":
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
            matchLinesPoints(imgPath, cleanedList)