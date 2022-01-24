import numpy as np
import cv2
from matUtils import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random 


def pnpNDetection(img_names_tab, clicked_tab, picked_tab) :  
    
    ##Declaration de variables
    unity_camera_matrix = np.array([[2592*31*10.16, 0.0,              2592/2],
                                    [0.0,           1944*31*10.16,    1944/2],
                                    [0.0,           0.0,              1.0]])
    
    unity_calibration_camera_matrix = np.array([[1.69595869e+04, 0.00000000e+00, 1.08942376e+03],
                                                [0.00000000e+00, 1.15226265e+04, 9.19251195e+02],
                                                [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

    unity_distortion_coef = np.array([  -1.18224645e+01,  
                                        1.82848852e+03,  
                                        6.38818148e-01, 
                                        -1.59879765e-01,
                                        -6.28018049e+04])
    out = []
    ## Boucles pour les N images donnees en entrees
    
    for n in range(np.size(img_names_tab)) : 
        path2d = 'HoleDetection\Points2D\\' + picked_tab[n] + '.npy'
        path3d = 'HoleDetection\Points3D\\' + clicked_tab[n] + '.npy'
        with open(path2d, 'rb') as f:
            picked_points_Ro = np.load(f, allow_pickle=False)
        random.shuffle(picked_points_Ro)
        with open(path3d, 'rb') as f:
            clicked_points = np.load(f, allow_pickle=False)
        random.shuffle(clicked_points)
        success, rotation_vector, translation_vector, _= cv2.solvePnPRansac(
            picked_points_Ro, 
            clicked_points, 
            unity_calibration_camera_matrix, 
            unity_distortion_coef)

        print("Sucess :", success)

        extrinsic_mat = construct_matrix_from_vec(np.concatenate([rotation_vector, translation_vector]))
    
        print("Extrinsic matrix :\n", extrinsic_mat)

        model_points_3DRo = np.loadtxt("Data\Plaque1\Model\Plaque_1.xyz", dtype=float)
        model_edges = np.loadtxt("Data\Plaque1\Model\Plaque_1.edges", dtype=int)

        XYZ1_Ro = model_points_3DRo[model_edges[:, 0]]
        XYZ2_Ro = model_points_3DRo[model_edges[:, 1]]
        model3D_Ro = np.concatenate([XYZ1_Ro, XYZ2_Ro], axis=1)

        fig = plt.figure(n)
        ax1 = fig.add_subplot(111)
        plt.imshow(mpimg.imread("Data\Plaque1\PhotoUnity\\" + img_names_tab[n]))
        transform_and_draw_model(model3D_Ro, unity_calibration_camera_matrix, extrinsic_mat, ax1)  # 3D model drawing
        plt.show(block = True)
        out = out.append(extrinsic_mat)
        
    return(out)

if __name__ == '__main__':
      
    tab = ["plaque=1_position=(99.0, -2360.0, 1250.0)_rotation=(294.8, 188.0, 192.3)_date=2022-01-19_14-36-37.png", "plaque=1_position=(99.0, -2360.0, 1250.0)_rotation=(294.8, 188.0, 192.3)_date=2022-01-19_14-36-37.png"]
    click_tab = ["clicked_points_Unity1", "clicked_points_Unity2"]
    pick_tab = ["picked_points_Ro_Unity1", "picked_points_Ro_Unity2"]
    result = pnpNDetection(tab, click_tab, pick_tab)
    


  