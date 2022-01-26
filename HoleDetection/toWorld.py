import numpy as np
import cv2
from matUtils import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def imageToWorld(intrinsic_mat, extrinsic_mat, twod_point) :  
    A = intrinsic_mat
    
    r1 = extrinsic_mat[:3, 0]
    r2 = extrinsic_mat[:3, 1]
    r3 = extrinsic_mat[:3, 2]
    R = np.array([r1],[r2],[r3])
    #r3 redondant car produit en croix des 2 premieres
    t = extrinsic_mat[:3, 3]
    
    #Calcul de l'homographie normalisee en divisant par t3
    H = intrinsic_mat*[r1, r2, t]/t[2]       #eqn 8.1, Hartley and Zisserman
    
    p = [twod_point[0], twod_point[1], 1]
    projection = H * p                 

    #solving for real world X Y Z coordinates
    real_world = (twod_point.append(1)*np.linalg.inv(A) - t )*np.linalg.inv(R)
    return(real_world)
    #return(world_point)

if __name__ == '__main__':
    intrinsic = np.array([[4.95789049e+03, 0.00000000e+00, 1.39806998e+03],
                         [0.00000000e+00, 4.90165198e+03, 6.86145950e+02],
                         [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
    
    extrinsic = np.array([[-5.82229102e-01,  6.12568023e-01, -5.34574307e-01, 9.32292553e+14],
                          [-7.56142475e-01, -1.66370223e-01,  6.32905606e-01, 1.45674165e+15],
                          [ 2.98760490e-01,  7.72710402e-01,  5.60054287e-01, 1.25558309e+15],
                          [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00, 1.00000000e+00]])
    
    twod_test = (115, 220)
    result = imageToWorld(intrinsic, extrinsic, twod_test)
    print(result)
