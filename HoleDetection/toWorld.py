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
        print(real_world)
    
    return(res_glob)

if __name__ == '__main__':
    intrinsic = np.array([[4.95789049e+03, 0.00000000e+00, 1.39806998e+03],
                         [0.00000000e+00, 4.90165198e+03, 6.86145950e+02],
                         [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
    
    extrinsic = [np.array([[ 9.70393994e-01,  2.31006188e-01,  7.05098374e-02, -1.74200453e+02], # image3
       [-2.26407763e-01,  9.71688952e-01, -6.75285468e-02, 3.86785422e+01],
       [-8.41131422e-02,  4.95653217e-02,  9.95222718e-01, 1.30238249e+03],
       [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00, 1.00000000e+00]]),
                 np.array([[ 9.99610419e-01,  2.70929807e-02,  6.70680804e-03, -1.52882226e+02], #image2
       [-2.69198884e-02,  9.99332948e-01, -2.46775038e-02, 9.00518884e+01],
       [-7.37092138e-03,  2.44873434e-02,  9.99672966e-01, 1.27603144e+03],
       [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00, 1.00000000e+00]]),
                 np.array([[ 9.65352751e-01,  2.57334282e-01, -4.32797208e-02, -8.73897853e+01], #image4
       [-2.56145874e-01,  9.66135694e-01,  3.11626601e-02, 7.41918137e+01],
       [ 4.98333038e-02, -1.89970377e-02,  9.98576865e-01, 1.30908946e+03],
       [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00, 1.00000000e+00]])
    ]
    
    twod_test = [np.array([46.00, 310.00, 1]), 
                 np.array([211.00, 370.00, 1]), 
                 np.array([355.00, 473.00, 1])]
    
    result = imageToWorld(intrinsic, extrinsic, twod_test)