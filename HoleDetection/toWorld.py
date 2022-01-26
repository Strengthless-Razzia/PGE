import numpy as np
import cv2
from matUtils import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def imageToWorld(intrinsic_mat, extrinsic_mat_tab, twod_point_tab) :  
     
    A = intrinsic_mat   
    res_glob = []
    
    for n in range(np.size(twod_point_tab, 0)) : 
        #keeping the homogenous parameters for inversing, and getting rid of it after 
        extrinsic_mat_inv =np.linalg.inv(extrinsic_mat_tab[n])
        
        real_world = np.dot(np.dot(twod_point_tab[n], np.linalg.inv(A)),  extrinsic_mat_inv[:3, :4])
        res_glob.append(real_world) 
    
    return(res_glob)

if __name__ == '__main__':
    intrinsic = np.array([[4.95789049e+03, 0.00000000e+00, 1.39806998e+03],
                         [0.00000000e+00, 4.90165198e+03, 6.86145950e+02],
                         [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
    
    extrinsic = [np.array([[-5.82229102e-01,  6.12568023e-01, -5.34574307e-01, 9.32292553e+14],
                          [-7.56142475e-01, -1.66370223e-01,  6.32905606e-01, 1.45674165e+15],
                          [ 2.98760490e-01,  7.72710402e-01,  5.60054287e-01, 1.25558309e+15],
                          [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00, 1.00000000e+00]])]
    
    twod_test = [np.array([115, 220, 1])]
    #, np.array([118,200,1])
    result = imageToWorld(intrinsic, extrinsic, twod_test)
