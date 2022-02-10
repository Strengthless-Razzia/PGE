from calendar import c
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
    delta = np.Infinity
    newPoints  = liste_points + 500
    bloc = np.array(coord_bloc) + 500 
    newPoints = np.concatenate((newPoints, bloc.reshape((1,2)))) 
    alpha = 10
    delta_min = np.Infinity
    newLine = np.array([[coord_ligne[0], coord_ligne[1]], [coord_ligne[2], coord_ligne[3]]]) + 500
    
    #delta en y pour la ligne, a mettre a 0 donc avec les arrondis, au dessus de 2 
    while(delta > 2):
        if(delta< delta_min):
        #tourner l'image dans un sens
            newPoints = np.around(matchpoints.rotate2dPoints(newPoints, alpha))
            newLine = np.around(matchpoints.rotate2dPoints(newLine, alpha))

        if(delta > delta_min ):
        #touner l'image dans l'autre sens si on depasse le delta min en reduisant le alpha a chaque fois
            newPoints = np.around(matchpoints.rotate2dPoints(newPoints, -alpha))
            newLine = np.around(matchpoints.rotate2dPoints(newLine, -alpha))
            alpha = alpha - 1
            
        ####AFFICHAGE DES POINTS
        plt.scatter(newPoints[:40, 0], newPoints[:40, 1], color='red', marker='x')
        plt.scatter(newPoints[40, 0], newPoints[40, 1], color='green', marker='o')
        #plt.show()
        delta = abs(newLine[0, 1]- newLine[1, 1])
        
    # mettre le bloc au dessus s'il ne l'est pas 
    if(newPoints[40, 1] < newLine[1, 1]):
        newPoints = matchpoints.rotate2dPoints(newPoints, 180)
    ##AFFIChAGE DU TOUT
    plt.scatter(newPoints[:40, 0], newPoints[:40, 1], color='red', marker='x')
    plt.scatter(newPoints[40, 0], newPoints[40, 1], color='green', marker='o')
    plt.show()
    return(newPoints[:40, :])


#### Entree :   liste de points d'origine 
 #              liste de points une fois la plaque reorientee
 
#### Sortie :   liste des lignes, chaque ligne un tableau comportant les points qui la composent


def ordoListe(liste_points, liste_reorient):
    sorted_points = []
    liste_y = []
    ligne = []
    temp_x = []
    temp = []
    
    #on recupere tous les y qui sont dans la liste reoriente 
    for point in liste_reorient:
        liste_y.append(point[1])
    liste_y = sorted(liste_y)

    min_dist = 20
    i = 0
    
    #on harmonise tous les y qui ont ete arrondis pour qu'ils aient tous la meme valeur
    while i < len(liste_y):
        value_to_change = None
        for j in range(len(liste_y)):
            if abs(liste_y[i] - liste_y[j]) < min_dist and abs(liste_y[i] - liste_y[j]) > 0.0:
                value_to_change = liste_y[i]
                ind = j
                break
     
        if value_to_change is not None:
            liste_y[ind] = value_to_change
        else:    
            i +=1
    #on recupere les y des lignes         
    for  y in liste_y:
        if(y not in ligne):
            ligne.append(y)  
            
    #pour ces lignes on recupere les x correspondants et on les reordonne dans une liste temporaire 
    for y in ligne :                 
        for point in liste_reorient : 
            if(point[1] < y + min_dist and point[1] > y - min_dist) : 
                temp_x.append([point[0], y])
        #cette ligne est rearrangee pour etre dans le bon ordre
        temp_x = sorted(temp_x)
        #de cette ligne dans le bon ordre, on recupere les points correspondants dans la liste de points originelle
        for point in temp_x: 
            temp.append(liste_points[np.where(liste_points, point)])
        sorted_points.append(temp)
        temp_x = []  
        temp = []             

    return sorted_points 
      
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
        circles = np.around(circles)

    return circles[0,:,:2]


if __name__ == '__main__':
    imgPath = "Data/Plate/image2.bmp"
    #position du bloc
    markX, markY = np.around(matchpoints.findMarkPosition(imgPath, debug=False))
    #position des deux points formant la ligne de la plaque la plus proche
    foundLine = matchpoints.detectClosestEdge(imgPath,markX, markY)
    #recuperation de toutes les coordonnees 2d des points de la plaque
    points = hough(imgPath)
    #reorientation de la plaque et calcul des nouvelles pos des points 
    newPoints = reOrient(points, [markX, markY], foundLine)
    #ordonnancement des points dans une liste des lignes trouvees
    liste = ordoListe(points, newPoints)
    print(liste)
    
    
