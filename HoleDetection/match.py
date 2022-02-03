import numpy as np
from matUtils import *
import matchpoints

def recoligne(liste_droite, liste_point):
    points_ordonnes = []
    seuil_min = np.Infinity
    seuil_max = 0
    seuil = 10
    
    for droite in liste_droite :
        points_associes = appartenance(droite, liste_point, seuil)
        for point in new_liste :
            dist = np.linalg.norm(new_liste[point]-new_liste[point+1])
            if(dist <dist_min):
                dist_min = dist
                points_ordonnes.append(point)
        
    return(points_ordonnes)
        

    
def appartenance(droite, liste_point, seuil):
    points_associes=[]
    for point in liste_point :
        distance_point =np.cross(droite[0]- droite[1],point-droite[0])/np.linalg.norm(droite[1]-droite[0])
        if(distance_point < seuil and len(points_associes) < 8):
            points_associes.append(point)   
    return(points_associes)
                 
if __name__ == '__main__':
    liste_2d = matchpoints.generateNewGrid()
    point_debut = 50
    point_fin = 10
    print(recoligne(np.array([point_debut, point_fin]) ,liste_2d))
    


        

#def appartenance(droite, liste_point, seuil_min, seuil_max):
 #   points_associes = []
  #  for point in liste_point :
   #     distance_point =np.cross(droite[0]- droite[1],point-droite[0])/np.linalg.norm(droite[1]-droite[0])
    #    if(distance_point < seuil_min and points_associes.size() < 8):
     #       seuil_min = distance_point
      #      points_associes.append(point)
       # if(distance_point > seuil_max and distance_point < 1.5*seuil_max and points_associes.size() <8):
        #    seuil_max = distance_point
         #   if(point not in points_associes):
          #      points_associes.append(point)    
   #     return(points_associes, seuil_max)