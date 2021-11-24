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
            cv.line(src, (int(l[0]), int(l[1])), (int(l[2]), int(l[3])), (0,0,255), 1, cv.LINE_AA)
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
        cv.line(src, (int(line[0]),int(line[1])), (int(line[2]),int(line[3])), (0,0,255), 1, cv.LINE_AA)
        cv.circle(src,ctr,2,(0,255,0))
        cv.imshow("LineDisplay",src)
        cv.waitKey()

def calcVector(l):
    """
    in :
        array {x1,y1,x2,y2}
    out:
        tuple (a,b) from ax+b 
    Calcul de l'expression mathématique de la ligne ax+b 
    """
    #Calc direction of line
    if l[2]-l[0] == 0:
        a = 10000
    else:
        a = (l[3]-l[1])/(l[2]-l[0])
    #Calc position in 0
    b = l[1]-l[0]*a 
    return [a,b]

def mergeTwoLines(l1, l2):
    """
    in : 
        l1 : array {x1,y1,x2,y2}
        l2 : array {x1,y1,x2,y2}
    out : 
        l  : array {x1,y1,x2,y2}
    Create a new line using two of them
    """
    pts = np.zeros([4,2])
    pts[0] = [l1[0],l1[1]]
    pts[1] = [l1[2],l1[3]]
    pts[2] = [l2[0],l2[1]]
    pts[3] = [l2[2],l2[3]]
    
    x = [l1[0],l1[2],l2[0],l2[2]]
    pointLeft  = x.index(min(x))
    pointRight = x.index(max(x))
    return np.append(pts[pointLeft],pts[pointRight])
    

def mergeSimilarLines(lines, threshold_a,threshold_b):
    """
    in :
        lines : array [N, 4] de lignes 
    out:
        mergedLines : array [l, 4] de lignes
    Rassemble les lignes similaire 
    """
    

    
    [N,tmp] = lines.shape
    listOfExpressions = np.zeros([N,2])
    mergedLines = np.empty([0,4])
    for i in range(N):
        listOfExpressions[i] =  calcVector(lines[i])
    
    i = 0
    while i < N:
        found = False
        j = i
        while j < N:
            if j != i:
                #Si les deux lignes sont suffisamment proches 
                if abs(listOfExpressions[i][0] - listOfExpressions[j][0]) <= threshold_a and abs(listOfExpressions[i][1] - listOfExpressions[j][1]) <= threshold_b:
                    #Si on en a pas déjà rajouté une
                    if not found:
                        newLine = mergeTwoLines(lines[i],lines[j])
                        mergedLines = np.vstack([mergedLines,newLine])
                    else: 
                        newLine = mergeTwoLines(mergedLines[-1],lines[j])   #Si on en a déjà rajouté une, on la merge avec la nouvelle ligne
                        mergedLines[-1] = newLine
                    found = True
                    lines = np.delete(lines, j,axis=0)
                    listOfExpressions = np.delete(listOfExpressions, j,axis=0)
                    [N,tmp] = lines.shape
            j += 1
        
        if not found:
            mergedLines = np.vstack([mergedLines,lines[i]])
        i += 1
    return mergedLines

def linesAreSimilar(l1,l2,t):
    """
    in : 
        l1 : array {x1,y1,x2,y2}
        l2 : array {x1,y1,x2,y2}
        t  : threshold de détection
    out : 
        isSimilar : Bool
    Retourne vrai si les deux lignes en entrée sont similaires selon le seuil t
    """
    pts1a = [l1[0],l1[1]]
    pts1b = [l1[2],l1[3]]
    pts2a = [l2[0],l2[1]]
    pts2b = [l2[2],l2[3]]

    #si pt1a = pt2a & pt1b = pt2b 
    if abs(pts1a[0] - pts2a[0]) + abs(pts1a[1] - pts2a[1]) <= t:
        if abs(pts1b[0] - pts2b[0]) + abs(pts1b[1] - pts2b[1]) <= t:
            return True
    #si pt1a = pt2b et pt1b = pt2a
    if abs(pts1a[0] - pts2b[0]) + abs(pts1a[1] - pts2b[1]) <= t:
        if abs(pts1b[0] - pts2a[0]) + abs(pts1b[1] - pts2a[1]) <= t:
            return True
    return False
    

def removeSimilarLines(lines,threshold):
    """
    in :
        lines : array [N, 4] de lignes 
    out:
        cleanedLines : array [l, 4] de lignes
    Supprime les doublons 
    """
    [N,tmp] = lines.shape
    cleanedLines = np.empty([0,4])
    
    for i in range(N):
        stop = False
        for j in range(i,N):
            if i != j:
                #Si les deux points sont suffisamment similaire
                if linesAreSimilar(lines[i],lines[j],threshold):
                    stop = True
                    break
        if not stop: #Si aucune autre ligne n'est similaire on sauvegarde la ligne
            cleanedLines = np.vstack([cleanedLines,lines[i]])
    return cleanedLines

if __name__ == "__main__": 
    #For all img files in directory dataset
    listOfFiles = os.listdir("lineDetection\dataset")
    for f in listOfFiles:
        if ".png" in f or ".jpg" in f:
            a_t = 0.5
            b_t = 5
            imgPath = "lineDetection\\dataset\\"+f

            lines = getHoughLines(imgPath)
            #displayImgWithLines(imgPath, lines, "Display")
            
            old = lines.shape
            mergedList=mergeSimilarLines(lines,a_t,b_t)
            
            new = mergedList.shape
            while new!= old:
                old = mergedList.shape
                mergedList=mergeSimilarLines(mergedList,a_t,b_t)
                new = mergedList.shape
                print(str(old)+":"+str(new))
            cleanedList = removeSimilarLines(mergedList,10)
            displayImgWithLines(imgPath, lines, "Original")
            print("lines shape" + str(lines.shape))
            print("merge shape" + str(mergedList.shape))
            print("clean shape" + str(cleanedList.shape))
            print(lines)
            print(mergedList)
            displayImgWithLines(imgPath, mergedList, "Merged")
            displayImgWithLines(imgPath, cleanedList, "Cleaned")
            displayIndividualLinesOfImage(imgPath,cleanedList)
