import numpy as np
from matUtils import *


def imageToWorld(extrinsic_mat, coord_3d) :  
     
    R = extrinsic_mat[0:3, 0:3]
    T = extrinsic_mat[0:3,3]
    real_world = np.dot( np.linalg.inv(R), coord_3d - T )
    print(real_world)

    return(real_world)

if __name__ == '__main__':

    extrinsic = [np.array([[ 9.98756305e-01,  4.46229623e-02, -2.22404009e-02, -1.07663870e+02], #image1
       [-4.43514998e-02,  9.98937113e-01,  1.25534231e-02, 7.07322785e+01],
       [ 2.27769328e-02, -1.15514154e-02,  9.99673835e-01, 1.32870728e+03],
       [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00, 1.00000000e+00]]),
                np.array([[ 9.70393994e-01,  2.31006188e-01,  7.05098374e-02, -1.74200453e+02], # image3
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
    
    coord = np.array([415.00, 325.00, 1]) 
    
    result = imageToWorld(extrinsic[0], coord)