"""
@file ShapeDetection.py
@brief Demonstrate the use of Shape detection algorithms
"""
import math
import os
import cv2 as cv
import numpy as np


def pretraitement(img):
    """
    in :
        img : /!\ Pas un path mais bien une image lue avec imread
    out:
        imgTraitee : image prétraitée

    Fonction appliquant un prétraitement a l'image afin d'aider la détection de plaque 
    """
    kernel = np.ones((5,5),np.uint8)    
    return cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)

def getContours(img, debug=False):
    """
    in :
        img : Path vers une image
        debug : bool qui si True, affiche les différentes parties du traitement
    out:
        foundContours : array de forme (N,4,2) avec N le nombre de contours trouvés et 4 sont les 4 angles du rectangle, 2 sont x et y
        Return None si erreur de lecture de l'image

    Fonction générant la liste de contours 
    """
    
    # Loads an image
    src = cv.imread(img, cv.IMREAD_GRAYSCALE)
    # Check if image is loaded fine
    if src is None:
        print ('Error opening image!')
        return None
    

    ## TODO Potentiel : Ajouter un prétraitement de l'image pour avoir une meilleure détection des edges

    imgEdges = cv.Canny(src, 50, 200, None, 3)
    if debug:
        cv.imshow("Original : " + str(img),src)
        cv.imshow("Edges : " + str(img),imgEdges)
        cv.waitKey()

    pretreatedImage = pretraitement(imgEdges)

    if debug:
        cv.imshow("Pretreated : " + str(img),pretreatedImage)
        cv.waitKey()
    
    contours,h = cv.findContours(pretreatedImage,cv.RETR_CCOMP  ,cv.CHAIN_APPROX_TC89_L1)
    
    foundContours = np.empty([0,4,2])

    for currentContour in contours:
        if cv.contourArea(currentContour) >200:
            
            tempImg = imgEdges
            approx = cv.approxPolyDP(currentContour, 0.01 * cv.arcLength(currentContour, True), True)
            approx = np.asarray(approx)
            [x,y,z] = approx.shape
            approx = np.reshape(approx,(1,x,z))
            
            if len(approx[0]) == 4:
                foundContours = np.vstack([foundContours,approx])
    
    return foundContours
    




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
            cv.line(src, (int(l[0]), int(l[1])), (int(l[2]), int(l[3])), (0,0,255), 1, cv.LINE_AA)
    cv.imshow(title,src)
    cv.waitKey()


def displayIndividualContourOfImage(img,lines):
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
        
        src = cv.imread(img)
        cv.line(src, (int(line[0]),int(line[1])), (int(line[2]),int(line[3])), (0,0,255), 1, cv.LINE_AA)
        
        cv.imshow("LineDisplay",src)
        cv.waitKey()



if __name__ == "__main__": 
    #For all img files in directory dataset
    listOfFiles = os.listdir("lineDetection\dataset")
    for f in listOfFiles:
        if ".png" in f or ".jpg" in f:
            
            imgPath = "lineDetection\\dataset\\"+f

            contours = getContours(imgPath, True)
            
