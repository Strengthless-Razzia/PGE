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
from HarrisCornerDetection import *

radius_point = 3
cred = (0,0,255)
cgreen = (0,255,0)
cblue = (255,0,0)
cyellow = (0,255,255)
cmarroon = (126,25,126)



def matchLinesPoints(imgPath,liste_lines):
    img = cv.imread(imgPath)

    points = getHarrisCorner(img)
    lines = liste_lines
    linesClean = np.array([])
    pointsContour = np.array([])
    linesContour = np.array([])

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
    cpt = 0
    # A chaque <point> detecte par Harris's corner algorithm, calcule s'il appartient a une des droites de <linesClean>
    # img.fill(255)

    for point in points:
        cpt = cpt +1
        for line in linesClean:
            if appartientDroite(point,line):
                index = np.where(linesClean == line) 
                displayPointLine(point,lines[index[0][0]],img,cblue)
                [pointsContour,linesContour] = updateContourPlaque(pointsContour,linesContour,point,lines[index[0][0]])
                
                # il peux y a voir plusieurs lignes correlles avec un seul point 
                if pointTrouve == False:
                    compteurPointTrouve = compteurPointTrouve + 1
                pointTrouve = True
                
        
        # Le point n'a pas ete trouve, il est affiche d'une couleur differente
        if pointTrouve == False:
            #displayPoint(point,img,cred)
            pass
            
        
        pointTrouve = False
        
    s = int(pointsContour.size/2)
    pointsContour = pointsContour.reshape(s,2)
    linesContour = linesContour.reshape(s,2)
    
    displayContourPlaque(pointsContour,linesContour,cv.imread(imgPath),cmarroon)

    print(str(compteurPointTrouve) + " points correles avec " + str(int(points.size/2)) + " angles et " + str(int(linesClean.size/2)) + " lignes detectes.")  
    #print(str(pointsContour) + "\n")
    #print(str(linesContour) + "\n")
    cv.waitKey()
    


def appartientDroite(point,line):
    n = 8  # nombre de pixel d'ecart aceptable
    x = point[0][0]
    y = point[0][1]

    a = line[0]
    b = line[1]

    e = y - a*x - b
    if (e == 0):
        return True
    elif (abs(e) <= 8):
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
    start_point = (int(line[0]),int(line[1]))
    end_point = (int(line[2]),int(line[3]))
    color = (255,0,0)

    img = cv.circle(img, (point[0][0],point[0][1]), radius_point, color, -1)
    img = cv.line(img, start_point, end_point, color, 1)


    cv.imshow("PointLine",img) 
    cv.imwrite('PointLine.png',img)
    #cv.waitKey()



def displayPoint(point,img,color):
    """
    in :
        point : point {x,y}
        img : image a afficher
        color : couleur utilisee pour point
    out:

    Fonction affichant un point
    """
    img = cv.circle(img, (point[0][0],point[0][1]), radius_point, color, -1)
    cv.imshow("PointLine",img)

def updateContourPlaque(liste_points, liste_lines, point, line):
    liste_lines = np.append(liste_lines, equationDroite(line), axis=0)
    liste_points = np.append(liste_points, point[0], axis=0)
    return [liste_points,liste_lines]
    

def displayContourPlaque(liste_points, liste_lines, img, color):
    for point in liste_points:
        index1 = np.where(liste_points == point)[0][0]
        # pour chaque point on regarde les autres points...
        for p in liste_points:
            index2  = np.where(liste_points == p)[0][0]
            if index1 != index2:
                a1 = liste_lines[index1][0]
                b1 = liste_lines[index1][1]
                a2 = liste_lines[index2][0]
                b2 = liste_lines[index2][1]

                # deux points on la meme ligne de reference
                if (a1==a2) and (b1==b2):
                    #print(str(int(index1+1)) + " = " + str(int(index2+1)))
                    img = cv.line(img, (int(point[0]),int(point[1])), (int(p[0]),int(p[1])), color, 2)

    cv.imshow("Contour",img)
    cv.imwrite('Contour.png',img)


if __name__ == "__main__":
    listOfFiles = os.listdir("cornerDetection/dataset")
    for f in listOfFiles:
        if ".png" in f or ".jpg" in f:
            a_t = 0.5
            b_t = 5
            imgPath = "cornerDetection/dataset/"+f

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