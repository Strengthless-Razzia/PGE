import numpy as np
import cv2
from matUtils import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

if __name__ == '__main__':
    
    aip_camera_matrix = np.array([  [86486 * 0.12,  0.,           320.],
                                    [0.,            61892 * 0.12, 240.],
                                    [0.,            0.,           1.  ]])

    raph_camera_matrix = np.array([ [1.98877058e+03, 0.00000000e+00, 2.43388762e+02],
                                    [0.00000000e+00, 1.96741747e+03, 4.87086762e+02],
                                    [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

    unity_camera_matrix = np.array([[2592*31*10.16, 0.0,              2592/2],
                                    [0.0,           1944*31*10.16,    1944/2],
                                    [0.0,           0.0,              1.0]])

    with open('HoleDetection/Points3D/picked_points_Ro_Unity.npy', 'rb') as f:
        picked_points_Ro = np.load(f, allow_pickle=False)

    with open('HoleDetection/Points2D/clicked_points_Unity.npy', 'rb') as f:
        clicked_points = np.load(f, allow_pickle=False)

    #print(picked_points_Ro)
    #print(clicked_points)

    #random_index = np.unique(np.random.randint(len(picked_points_Ro), size=10))
    #print(random_index)

    #clicked_points = np.delete(clicked_points, obj=random_index, axis=0)
    #picked_points_Ro = np.delete(picked_points_Ro, obj=random_index, axis=0)

    dist_coeffs = np.zeros((4,1))

    success, rotation_vector, translation_vector = cv2.solvePnP(
        picked_points_Ro, 
        clicked_points, 
        unity_camera_matrix, 
        dist_coeffs,
        flags=0)

    print("Sucess :", success)
    print("Rotation vect :\n", rotation_vector)
    print("Translation vect :\n", translation_vector)
    print("Iniliers \n", )

    extrinsic_mat = construct_matrix_from_vec(np.concatenate([rotation_vector, translation_vector]))


    print("Extrinsic matrix :\n", extrinsic_mat)

    model_points_3DRo = np.loadtxt("Data/Plaque1/Model/Plaque_1.xyz", dtype=float)
    model_edges = np.loadtxt("Data/Plaque1/Model/Plaque_1.edges", dtype=int)

    XYZ1_Ro = model_points_3DRo[model_edges[:, 0]]
    XYZ2_Ro = model_points_3DRo[model_edges[:, 1]]
    model3D_Ro = np.concatenate([XYZ1_Ro, XYZ2_Ro], axis=1)

    fig1 = plt.figure(1)
    ax1 = fig1.add_subplot(111)
    plt.imshow(mpimg.imread("./Data/Plaque1/PhotoUnity/plaque=1_position=(0.0, -1800.0, 0.0)_rotation=(270.0, 0.0, 0.0)_date=2022-01-19_14-19-15.png"))
    transform_and_draw_model(model3D_Ro, unity_camera_matrix, extrinsic_mat, ax1)  # 3D model drawing

    plt.scatter(clicked_points[:, 0], clicked_points[:, 1], marker='x', color='g')


    plt.show(block=True)


