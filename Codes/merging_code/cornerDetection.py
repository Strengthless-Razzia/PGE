# import the required library
from matplotlib import pyplot as plt
import numpy as np
import cv2 as cv
import warnings
import sys
  

def getHarrisCorner(img):
    """
    in :
        img : Path vers une image
    out:
        points : array de n points {x,y} coordonnees en px de l'image

    Fonction générant les angles de Harris
    """
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    corners = cv.goodFeaturesToTrack(gray, 50, 0.01, 10)
    corners = np.int0(corners)
    return corners


def isPartOfLine(line,point,ea,eb):
    """
    in :
        line : lignes {a,b}
        point : points {x,y} coordonnees en px de l'image
        ea, eb : ecart du point à la ligne (permet d'aggrandir la zone de recherche autour du point)
    out:
        boolean :   <True>  si le point appartient à la ligne, 
                    <False> sinon

    Fonction calculant l'appartenance d'un point à une ligne
    """
    warnings.filterwarnings('error')
    
    a,b = line
    x,y = point
    color = (255,0,0)

    e_a = ea # ecart a la ligne en px pour b
    e_b = eb # ecart a la ligne en px pour a

    res = False
    b = int(round(b))
    a = int(round(a))

    if(e_a == 0) and (e_b==0):
        try:
            eq = -a*x+y-b
        except RuntimeWarning:
            pass
            
        if eq == 0:
            res = True
            return True
    elif(e_a == 0):
        for i in range((b-e_b),(b+e_b+1),1):
            try:
                eq = -a*x+y-i
            except RuntimeWarning:
                pass
                
            if eq == 0:
                res = True
                return True
    elif(e_b == 0):
        pass
    else:
        for j in range((a-e_a),(a+e_a),1):
            for i in range((b-e_b),(b+e_b),1):
                try:
                    eq = -j*x+y-i
                except RuntimeWarning:
                    pass
                
                if eq == 0:
                    res = True
                    return True

    return res



def equationDroite(line):
    """
    in :
        line : lignes {x1,y1,x2,y2}
    out:
        a,b : coefficient directeur et ordonnee a l'origine de la droite {a,b} (y = a*x + b)

    Fonction calculant les paramètres <a> et <b> d'une droite définie par deux points 
    """
    warnings.filterwarnings('error')

    x1 = line[0]
    y1 = line[1]
    x2 = line[2]
    y2 = line[3]
    
    try:
        a = (y2 - y1)/(x2 - x1)
    except RuntimeWarning:
        a = 0
    b = y1 - a*x1 

    return a,b



def displayHarrisCorner(imgPath) :
    img = cv.imread(imgPath)
    corners = getHarrisCorner(img)
    for i in corners:
        x, y = i.ravel()
        cv.circle(img, (x, y), 3, (0,0,255), -1)    
    cv.imshow("HarrisCorner",img)
    cv.waitKey()



if __name__ == "__main__":

    img = cv.imread(sys.argv[1])
    corners = getHarrisCorner(img)
    
    # Liste de ligne définie arbitrairement (par un coeff <a> et <b> ou par deux points)
    line2 = [28,-58] 
    line3 = [15,20]
    line1 = equationDroite([135,98,171,177])
    
    lines = [line1,line2,line3]

    for i in corners:
        isPart = False
        x, y = i.ravel()

        # Test appartenance à une ligne parmis une liste de lignes
        for line in lines:
            if(isPartOfLine(line,[x,y],1,1)):
                isPart = True
                cv.circle(img, (x, y), 3, (0,0,255), -1)

        if isPart == False:
            color = (255,0,0)
            cv.circle(img, (x, y), 3, color, -1)

    plt.imshow(img), plt.show()



if __name__ == "__main2__":
    if(isPartOfLine(equationDroite([10,1,1,10]),[4,7],0,2)):
        print("Point sur la ligne")
    else:
        print("Point non sur la ligne")