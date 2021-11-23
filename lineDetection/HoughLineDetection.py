"""
@file hough_lines.py
@brief This program demonstrates line finding with the Hough transform
"""
import math
import os
import cv2 as cv
import numpy as np



def getCenter(l):
    """
        in : array {x1,y1,x2,y2}
        out : tuple (xc,yc) - INT
        Calcule et retourne le pixel correspondant au centre d'une ligne
    """
    x1 = l[0]
    y1 = l[1]
    x2 = l[2]
    y2 = l[3]
    centerX = (x2+x1)/2
    centerY = (y2+y1)/2
    return (int(centerX),int(centerY))




def getHoughLines(img):
    """
    in :
        img : Path vers une image
    out:
        lines : array de N lignes {x1,y1,x2,y2}
        Return None si erreur de lecture de l'image

    Fonction générant les lignes Probabilistes de Hough
    """
    
    # Loads an image
    src = cv.imread(img, cv.IMREAD_GRAYSCALE)
    # Check if image is loaded fine
    if src is None:
        print ('Error opening image!')
        return None
    
    ## TODO Potentiel : Ajouter un prétraitement de l'image pour avoir une meilleure détection des edges

    imgEdges = cv.Canny(src, 50, 200, None, 3)
    lines = cv.HoughLinesP(imgEdges, 1, np.pi / 180, 50, None, 50, 10)
    #Enlever une dimension inutile de HoughLinesP pour faciliter l'utilisation de lines
    (x,y,z) = lines.shape
    lines = np.resize(lines, (x,z))
    return lines




def displayImgWithLines(img, lines, title):
    """
    in :
        img : Path vers une image
        lines : Array des lignes détectées sur une image 
        title : Titre de la fenêtre d'affichage
    out:
        None

    Fonction affichant une image avec les lignes détectées dessus
    Bloque le déroulement jusqu'à la pression d'une touche du clavier
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
            cv.line(src, (l[0], l[1]), (l[2], l[3]), (0,0,255), 1, cv.LINE_AA)
    cv.imshow(title,src)
    cv.waitKey()


def displayIndividualLinesOfImage(img,lines):
    """
    in :
        img : Path vers une image
        lines : Array des lignes détectées sur une image 
    out:
        None

    Fonction affichant les lignes d'une image une par une
    Bloque le déroulement jusqu'à ce que la dernière ligne soit montrée
    """
    for line in lines:
        line = line
        ctr = getCenter(line)
        src = cv.imread(img)
        cv.line(src, [line[0],line[1]], [line[2],line[3]], (0,0,255), 1, cv.LINE_AA)
        cv.circle(src,ctr,2,(0,255,0))
        cv.imshow("LineDisplay",src)
        cv.waitKey()
    

if __name__ == "__main__":
    #For all img files in directory dataset
    listOfFiles = os.listdir("lineDetection\dataset")
    for f in listOfFiles:
        if ".png" in f or ".jpg" in f:
            
            imgPath = "lineDetection\\dataset\\"+f
            
            lines = getHoughLines(imgPath)
            displayImgWithLines(imgPath, lines, "Display")
            displayIndividualLinesOfImage(imgPath,lines)
    
    
