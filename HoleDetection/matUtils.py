from matplotlib import projections
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def construct_matrix_from_vec(vec_solution):
    a = vec_solution[0]
    b = vec_solution[1]
    g = vec_solution[2]
    x = vec_solution[3]
    y = vec_solution[4]
    z = vec_solution[5]

    matPos = np.array([[1.0, 0.0, 0.0, 0.0],
                       [0.0, 1.0, 0.0, 0.0],
                       [0.0, 0.0, 1.0, 0.0],
                       [0.0, 0.0, 0.0, 1.0]])

    matPos[0, 0] = np.cos(g) * np.cos(b)
    matPos[0, 1] = np.cos(g) * np.sin(b) * np.sin(a) - np.sin(g) * np.cos(a)
    matPos[0, 2] = np.cos(g) * np.sin(b) * np.cos(a) + np.sin(g) * np.sin(a)
    matPos[0, 3] = x

    matPos[1, 0] = np.sin(g) * np.cos(b)
    matPos[1, 1] = np.sin(g) * np.sin(b) * np.sin(a) + np.cos(g) * np.cos(a)
    matPos[1, 2] = np.sin(g) * np.sin(b) * np.cos(a) - np.cos(g) * np.sin(a)
    matPos[1, 3] = y

    matPos[2, 0] = -np.sin(b)
    matPos[2, 1] = np.cos(b) * np.sin(a)
    matPos[2, 2] = np.cos(b) * np.cos(a)
    matPos[2, 3] = z
    return matPos

def transform_and_draw_model(edges_Ro, intrinsic, extrinsic, fig_axis):
    # ********************************************************************* #
    # A COMPLETER.                                                          #
    # UTILISER LES FONCTIONS :                                              #
    #   - perspective_projection                                            #
    #   - transform_point_with_matrix                                       #
    # Input:                                                                #
    #   edges_Ro : ndarray[Nx6]                                             #
    #             N = nombre d'aretes dans le modele                        #
    #             6 = (X1, Y1, Z1, X2, Y2, Z2) les coordonnees des points   #
    #                 P1 et P2 de chaque arete                              #
    #   intrinsic : ndarray[3x3] - parametres intrinseques de la camera     #
    #   extrinsic : ndarray[4x4] - parametres extrinseques de la camera     #
    #   fig_axis : figure utilisee pour l'affichage                         #
    # Output:                                                               #
    #   Pas de retour de fonction, mais calcul et affichage des points      #
    #   transformes (u1, v1) et (u2, v2)                                    #
    # ********************************************************************* #

    # A remplacer #
    #u_1 = np.zeros((edges_Ro.shape[0], 1))
    #u_2 = np.zeros((edges_Ro.shape[0], 1))
    #v_1 = np.zeros((edges_Ro.shape[0], 1))
    #v_2 = np.zeros((edges_Ro.shape[0], 1))
    ###############

    P1_cam = transform_point_with_matrix(extrinsic, edges_Ro[:,:3])
    P2_cam = transform_point_with_matrix(extrinsic, edges_Ro[:,3:])

    [u_1, v_1] = perspective_projection(intrinsic, P1_cam)
    [u_2, v_2] = perspective_projection(intrinsic, P2_cam)

    for p in range(edges_Ro.shape[0]):
        fig_axis.plot([u_1[p], u_2[p]], [v_1[p], v_2[p]], color='pink')


def perspective_projection(intrinsic, P_c):
    # ***************************************************** #
    # A COMPLETER.                                          #
    # Fonction utile disponible :                           #
    #   np.dot                                              #
    # Input:                                                #
    #   intrinsic : ndarray[3x3] - parametres intrinseques  #
    #   P_c : ndarray[Nx3],                                 #
    #         N = nombre de points à transformer            #
    #         3 = (X, Y, Z) les coordonnees des points      #
    # Output:                                               #
    #   u, v : deux ndarray[N] contenant les                #
    #          coordonnees Ri des points P_c transformes    #
    # ***************************************************** #
    
    Z = P_c[:,2]
    [u,v,tmp] = (1/Z) * np.dot(intrinsic, P_c.T)



    return u, v


def transform_point_with_matrix(transformation_matrix, initial_point):
    initial_point_cpy = np.ones((initial_point.shape[0], 4))
    initial_point_cpy[:, 0:3] = np.copy(initial_point)

    transformed_point = np.dot(transformation_matrix, initial_point_cpy.T)

    return transformed_point[0:3, :].T


def plot_3d_model(model, fig, sub=111):
    ax = fig.add_subplot(sub, projection='3d')

    lines = []
    for idx in range(model.shape[0]):
        lines.append(ax.plot([model[idx, 0], model[idx, 3]],
                                [model[idx, 1], model[idx, 4]],
                                [model[idx, 2], model[idx, 5]],
                                color='k', picker=5)[0])
    ax.scatter(0, 0, 0, color='r', s=30)
    ax.set_xlabel('x (mm)')
    ax.set_ylabel('y (mm)')
    ax.set_zlabel('z (mm)')
    ax.set_title('3D model')

    return ax, lines