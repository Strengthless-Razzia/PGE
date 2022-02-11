#!/usr/bin/python2.6
# -*-coding:Latin-1 -*

import numpy as np
from matUtils import *
import matchpoints
import cv2
from matplotlib import pyplot as plt
from enum import Enum



class Position(Enum):
    RIGHT = 0,
    LEFT = 1,
    UP = 2,
    DOWN = 3

# Réduit la taille de l'image
# in: img à réduire, pourcentage de l'image de base

def resize_img(img,pourcentage):
    scale_percent = pourcentage 
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA) 
    return img


# Affiche l'image de base avec le côté de la plaque le plus proche du cube et les points 2d trouvés
# in : chemin de le l'image, coordonnée de la ligne (x1,y1,x2,y2), liste des points 2d

def display_closest_edge(imgPath,line,circles):
    img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)

    start_point = (line[0], line[1])
    end_point = (line[2], line[3])
    radius = 5
    color = (0,0,255)
    thickness = 10

    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    img = cv2.line(img, start_point, end_point, (255,0,0), 20)
    temp = 0
    for circle in circles:
        if temp == 0:
            img = cv2.circle(img, (circle[0], circle[1]), radius, (255,0,0), thickness)
            temp = 1
        else:    
            img = cv2.circle(img, (circle[0], circle[1]), radius, color, thickness)
    
    img = resize_img(img,30)

    cv2.imshow("ligne et points 2d", img)
    cv2.waitKey(0) 
    cv2.destroyAllWindows()


# Trouve la liste des points 2d dans l'image
# in : chemin vers l'image

def hough(imgPath):
    p1 = 100
    p2 = 20
    blur = 5
    dp = 1
    minDist = 150
    
    img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    imgGray = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    imgGray = cv2.cvtColor(imgGray, cv2.COLOR_BGR2GRAY)

    imgGray = cv2.medianBlur(imgGray, blur)

    circles = cv2.HoughCircles(imgGray, cv2.HOUGH_GRADIENT, dp, minDist,
                                param1=p1,param2=p2,minRadius=0,maxRadius=100)

    if( not (circles is None)):
        circles = np.uint16(np.around(circles))

    return circles[0,:,:2]



def cube_left(imgPath,line,circles):
    # décalage de la droite du coté de la plaque à l'opposé du cube
    # appartenance du premier point à la droite
    # récupération de la ligne/colonne de point
    img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)

    xa = line[0]
    ya = line[1] 
    xb = line[2]
    yb = line[3]
 
    treshold = 3
    amount = 5

    point_found = False

    while point_found == False:
        
        for circle in circles:
            xp = circle[0]
            yp = circle[1]

            if (xp+treshold > xb) and (xp-treshold < xb):
                point_found = True

                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                img = cv2.line(img, (xb, ya), (xb, yb), (255,0,0), 20)
                img = cv2.circle(img, (xp, yp), 5, (0,0,255), 10)
                img = resize_img(img,30)

                cv2.imshow("point trouvé", img)
                cv2.waitKey(0) 
                cv2.destroyAllWindows()
                break
            # appartenance d'un point 2d à la droite
        
        xb+=amount
            

        pass



# Calcul la position du cube par rapport à la ligne
# in : chemin vers l'image, coordonnées des deux points formant la ligne, coordonée du point central du cube

def position_cube_ligne(imgPath,line,cubex,cubey):
    # calcul equation droite
    xa = line[0]
    ya = line[1] 
    xb = line[2]
    yb = line[3]

    # cas d'une ligne verticale
    if xb-xa == 0:
        if cubex > xa:
            return Position.RIGHT
        elif cubex < xa:
            return Position.LEFT
    # ligne non verticale
    else:
        m = (yb - ya) / (xb - xa)
        p = yb - m*xb

        if cubey - ( m * cubex + p ) < 0:
            return Position.UP
        else:
            return Position.DOWN


if __name__ == '__main__':
    imgPath = "Data\Plate\image2.bmp"
    #position du bloc
    markX, markY = matchpoints.findMarkPosition(imgPath)
    
    #position des deux points formant la ligne de la plaque la plus proche
    foundLine = matchpoints.detectClosestEdge(imgPath,markX, markY)

    #recuperation de toutes les coordonnees 2d des points de la plaque
    circles = hough(imgPath)

    display_closest_edge(imgPath,foundLine,circles)
    pos = position_cube_ligne(imgPath,foundLine,markX,markY)

    if (pos == Position.LEFT):
        print("Cube a gauche")
        cube_left(imgPath,foundLine,circles)
    elif (pos == Position.RIGHT):
        pass
    elif (pos == Position.UP):
        pass
    elif (pos == Position.DOWN):
        pass