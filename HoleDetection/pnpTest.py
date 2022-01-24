import numpy as np
import cv2
from matUtils import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

if __name__ == '__main__':

    cognex_calibration_camera_matrix = np.array([[4.95789049e+03, 0.00000000e+00, 1.39806998e+03],
                                        [0.00000000e+00, 4.90165198e+03, 6.86145950e+02],
                                        [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

    cognex_distortion_coef = np.array([-0.11133023,  
                                        1.96562876, 
                                        -0.00787018, 
                                        0.01009623, 
                                        -7.61314684])

    with open('HoleDetection\Points3D\clicked_points_reel.npy', 'rb') as f:
        picked_points_Ro = np.load(f, allow_pickle=False)

    with open('HoleDetection\Points2D\picked_points_RO_reel.npy', 'rb') as f:
        clicked_points = np.load(f, allow_pickle=False)

    success, rotation_vector, translation_vector, inliers = cv2.solvePnPRansac(
        picked_points_Ro, 
        clicked_points, 
        cognex_calibration_camera_matrix, 
        cognex_distortion_coef)

    print("Sucess :", success)
    extrinsic_mat = construct_matrix_from_vec(np.concatenate([rotation_vector, translation_vector]))
    print("Extrinsic matrix :\n", extrinsic_mat)

    model_points_3DRo = np.loadtxt("Data\Plaque1\Model\Plaque_1.xyz", dtype=float)
    model_edges = np.loadtxt("Data\Plaque1\Model\Plaque_1.edges", dtype=int)

    XYZ1_Ro = model_points_3DRo[model_edges[:, 0]]
    XYZ2_Ro = model_points_3DRo[model_edges[:, 1]]
    model3D_Ro = np.concatenate([XYZ1_Ro, XYZ2_Ro], axis=1)

    fig1 = plt.figure(1)
    ax1 = fig1.add_subplot(111)
    plt.imshow(mpimg.imread("Data\Plaque1\Cognex\image1.bmp"))
    transform_and_draw_model(model3D_Ro, cognex_calibration_camera_matrix, extrinsic_mat, ax1)  # 3D model drawing

    plt.scatter(clicked_points[:, 0], clicked_points[:, 1], marker='x', color='g')


    plt.show(block=True)