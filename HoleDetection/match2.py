import numpy as np
from matUtils import *
import matchpoints
import cv2
from matplotlib import pyplot as plt


#### Entree :   liste de points d'origine 
 #              coordonnees du bloc
 #              coordonnees de deux points situees sur la premiere ligne detectee, donnant l'orientation
 #              Image
 
#### Sortie :   liste des lignes, chaque ligne un tableau comportant les points qui la composent

def reOrient(liste_points, coord_bloc, coord_ligne):
    delta = abs(coord_ligne[1]- coord_ligne[3])
    newPoints  = liste_points
    alpha = 5
    wasNeg = False
    wasPos = False
    #delta en y pour la ligne, a mettre a 0
    while(delta < -1  or delta > 1):
        if(delta>0):
        #tourner l'image dans un sens
            newPoints = matchpoints.rotate2dPoints(newPoints, alpha)
            wasPos = True
            if(wasNeg):
               alpha = alpha-0.1
        if(delta<0):
        #touner l'image dans l'autre sens
            newPoints = matchpoints.rotate2dPoints(newPoints, -alpha)
            wasNeg = True
            if(wasPos):
                alpha = alpha - 0.1
        ####AFFICHAGE DES POINTS
        plt.show(newPoints)
        # si on a deja ete trop dans un sens et qu'on est dans l'autre, on reduit le alpha. 

    # mettre le bloc au dessus s'il ne l'est pas 
    if(coord_bloc[1] < coord_ligne[1]):
        newPoints = matchpoints.rotate2dPoints(newPoints, 180)
    plt.show(newPoints)
    ##AFFIChAGE DU TOUT
    print(newPoints)
    return(newPoints)


#### Entree :   liste de points d'origine 
 #              liste de points une fois la plaque reorientee
 
#### Sortie :   liste des lignes, chaque ligne un tableau comportant les points qui la composent

def ordoListe(liste_points, liste_reorient):
    sorted = []
    temp = []
  #  for point in liste_reorient:
 #       if()
            #temp.append(liste_points(liste_reorient.index(point))) 
 #       temp = []
  #      sorted.append(temp)
    return sorted 

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

    circles = cv2.HoughCircles(imgGray, cv2.HOUGH_GRADIENT, dp, minDist, param1=p1,param2=p2,minRadius=0,maxRadius=100)

    
    scale_percent = 30 # percent of original size
    width = int(imgGray.shape[1] * scale_percent / 100)
    height = int(imgGray.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    imgGray = cv2.resize(imgGray, dim, interpolation = cv2.INTER_AREA) 
    cv2.imshow("", imgGray)
    cv2.waitKey(0) 
    cv2.destroyAllWindows()
    if( not (circles is None)):
        circles = np.uint16(np.around(circles))
        
    return circles[0,:,:2]


if __name__ == '__main__':
    imgPath = "Data\Plate\image2.bmp"
    #position du bloc
    markX, markY = matchpoints.findMarkPosition(imgPath)
    #position des deux points formant la ligne de la plaque la plus proche
    foundLine = matchpoints.detectClosestEdge(imgPath,markX, markY)
    print(foundLine)
    #recuperation de toutes les coordonnees 2d des points de la plaque
    #points = hough(imgPath)
    #reorientation de la plaque et calcul des nouvelles pos des points 
    #newPoints = reOrient(points, [markX, markY], foundLine)
    #ordonnancement des points dans une liste des lignes trouvees
    #liste = ordoListe(points, newPoints)
    