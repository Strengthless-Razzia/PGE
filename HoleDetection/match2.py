import numpy as np
from matUtils import *
import matchpoints
import cv2


#### Entree :   liste de points d'origine 
 #              coordonnees du bloc
 #              coordonnees de deux points situees sur la premiere ligne detectee, donnant l'orientation
 #              Image
 
#### Sortie :   liste des lignes, chaque ligne un tableau comportant les points qui la composent

def reOrient(liste_points, coord_bloc, coord_ligne):
    delta = abs(coord_ligne[0][1]- coord_ligne[1][1])
    #delta en y pour la ligne, a mettre a 0
   # if(delta[1] > 0 ):
        #tourner l'image 
        #les points changent
   #     newPoints = 
    # mettre le bloc au dessus en checkant 
    
    #les points changent ou non selon ou est le bloc
    
  #  return(newPoints)


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
    p1 = 30
    minv = 10
    maxv = 60
    img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #adaptive threshold
    imgGray = cv2.medianBlur(imgGray, blur=5)
    imgGray = cv2.adaptiveThreshold(imgGray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,41,3) #41
    imgGray = cv2.medianBlur(imgGray, blur=5)
    imgGray[imgGray ==1] = 255
    #kernel = np.ones((7,7),np.uint8)
    kernel = cv2.getStructuringElement(shape=cv2.MORPH_ELLIPSE, ksize=(9,9))
    imgGray = cv2.morphologyEx(imgGray, cv2.MORPH_OPEN, kernel)

    circles = cv2.HoughCircles(imgGray, cv2.HOUGH_GRADIENT, dp=1.5, minDist=295,
                                param1=p1,param2=30,minRadius=10,maxRadius=60)

    imgCanny = cv2.Canny(imgGray, p1//2, p1)
    nb_c = 0
    if( not (circles is None)):
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            if i[2] >= minv and i[2] <= maxv:
                cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),10)
                cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
                nb_c += 1

    return np.concatenate((img, cv2.cvtColor(imgCanny, cv2.COLOR_GRAY2BGR)), axis=1), circles[0,:]


if __name__ == '__main__':
    imgPath = "Data\Plate\image2.bmp"
    #position du bloc
    markX, markY = matchpoints.findMarkPosition(imgPath)
    #position des deux points formant la ligne de la plaque la plus proche
    foundLine = matchpoints.detectClosestEdge(imgPath,markX, markY)
    #recuperation de toutes les coordonnees 2d des points de la plaque
    points = hough(imgPath)[2]
    print(points)
    #reorientation de la plaque et calcul des nouvelles pos des points 
    newPoints = reOrient(points, [markX, markY], foundLine)
    #ordonnancement des points dans une liste des lignes trouvees
    liste = ordoListe(points, newPoints)
    