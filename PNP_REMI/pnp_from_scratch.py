import numpy as np
import itertools
import cv2

#////////////////////////////#
#//  Données essentielles  //#
#////////////////////////////#
Points_3D = np.array([[-150., -175., 5.],
                    [ -80., -175., 5.],
                    [ -10., -175., 5.],
                    [ -10.,  175., 5.],
                    [  60.,  175., 5.],
                    [ 130.,  175., 5.]])
                            
Points_2D = np.array([[ 411.86363636, 322.44805195],
                    [ 674.85064935, 317.18831169],
                    [ 937.83766234, 306.66883117],
                    [ 990.43506494, 1590.04545455],
                    [1237.64285714, 1579.52597403],
                    [1500.62987013, 1574.26623377]])



Intrinsec = np.array([[4.957e03, 0, 1.398e03],
                        [0, 4.901e03, 6.861e02],
                        [0, 0, 1]])


#/////////////////#
#//  Fonctions  //#
#/////////////////#
def pnp(Point3D,Point2D,IntrinsicMat):
    equations = np.zeros([18,12])
    C = np.array([[0, 0 ,0 ,0 ,0, 0, 0, 0, 0, 0, 0, 0]])

    for p2,p3 in itertools.zip_longest(Point2D, Point3D):
        x = p2[0]
        y = p2[1]

        X = p3[0]
        Y = p3[1]
        Z = p3[2]

        A = np.array([  [0, 0, 0, 0, -X, -Y, -Z, -1, y*X, y*Y, y*Z, y],
                        [Y, Y, Z, 1, 0, 0, 0, 0, -x*X, -x*Y, -x*Z, -x],
                        [-y*X, -y*Y, -y*Z, -y, x*X, x*Y, x*Z, x, 0, 0, 0, 0]]) 
        
        C = np.append(C, [A[0]], 0)
        C = np.append(C, [A[1]], 0)
        C = np.append(C, [A[2]], 0)


    # Résolution du système 18 équations, 12 inconnus
    u, s, vh = np.linalg.svd(C, full_matrices=True)
    # La matrice de projection est la dernière colonne de la matrice vh  shape:(12,12)
    Mp = vh[:,11]
    Mp = Mp.reshape((3, 4))

    # Obtention de la matrice de rotation et du vecteur de translation
    K_inv = np.linalg.inv(IntrinsicMat)
    cameraMatrix, rotMatrix, transVect, rotMatrixX, rotMatrixY, rotMatrixZ, eulerAngles = cv2.decomposeProjectionMatrix(Mp)
    transVect = transVect[:3] / transVect[3]
        
    return rotMatrix, transVect



if __name__ == '__main__':
    rotM, transV = pnp(Points_3D,Points_2D,Intrinsec)
    print(rotM)
    print(transV)

