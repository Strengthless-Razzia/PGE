import numpy as np
from matUtils import *
import matchpoints

def recoligne(liste_droite, liste_point):
    points_ordonnes = []
    seuil = 5
    
    for droite in liste_droite :
        points_associes = appartenance(droite, liste_point, seuil)
        for point in points_associes :
            dist = np.linalg.norm(points_associes[point]-points_associes[point+1])
            #la le point+1 pose souci, mettre une limite 
            if(dist <dist_min):
                dist_min = dist
        for point in points_associes : 
            if(dist < dist_min*1.5):
                points_ordonnes.append(point)
            else : 
                for i in range(int(dist/dist_min)):
                    points_ordonnes.append(0)
                points_ordonnes.append(point)            
        
    return(points_ordonnes)

                 
if __name__ == '__main__':
    liste_2d = matchpoints.generateNewGrid()
    point_debut = np.array((0, 10))
    point_fin = np.array((100, 50))
    print(recoligne(np.array(([point_debut, point_fin], [point_fin, point_debut])) ,liste_2d))
    