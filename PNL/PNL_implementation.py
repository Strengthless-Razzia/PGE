# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 00:35:00 2019

@author: thgerm
"""

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np

import matTools


class PNL:
    EPS = 0.5
    def __init__(self, nb_segments, pick_lines_Ro, normal_vectors, model3D_Ro, intrinsic_matrix,) -> None:

        self.nb_segments = nb_segments
        self.pick_lines_Ro = pick_lines_Ro
        self.normal_vectors = normal_vectors
        self.model3D_Ro = model3D_Ro
        self.intrinsic_matrix = intrinsic_matrix
            

        
        self.param_solution = np.array([-2.1, 0.7, 2.7, 3.1, 1.3, 18.0])
        self.extrinsic_matrix = matTools.construct_matrix_from_vec(self.param_solution)

        self.pick_lines_Rc = np.copy(self.pick_lines_Ro)

        self.pick_lines_Rc[:, [0, 1, 2]] = matTools.transform_point_with_matrix(self.extrinsic_matrix, self.pick_lines_Ro[:, [0, 1, 2]])
        self.pick_lines_Rc[:, [3, 4, 5]] = matTools.transform_point_with_matrix(self.extrinsic_matrix, self.pick_lines_Ro[:, [3, 4, 5]])
    

    def run(self, image_path = None):

        initial_error = self.calculate_error()
        print('Initial criteria : ' + str(initial_error))

        l = 0.0001  # lambda value
        it = 0
        while True:
            J = np.zeros((2 * self.nb_segments, 6))
            F = np.zeros((2 * self.nb_segments))
            lig = 0

            self.pick_lines_Rc[:, [0, 1, 2]] = matTools.transform_point_with_matrix(self.extrinsic_matrix, self.pick_lines_Ro[:, [0, 1, 2]])
            self.pick_lines_Rc[:, [3, 4, 5]] = matTools.transform_point_with_matrix(self.extrinsic_matrix, self.pick_lines_Ro[:, [3, 4, 5]])

            for p in range(self.nb_segments):
                normal_vector = np.copy(self.normal_vectors[p, [0, 1, 2]])
                [partial_deriv, crit_X0] = partial_derivatives(normal_vector, self.pick_lines_Rc[p, [0, 1, 2]])
                J[lig, :] = partial_deriv.T
                F[lig] = -crit_X0
                lig = lig + 1

                [partial_deriv, crit_X0] = partial_derivatives(normal_vector, self.pick_lines_Rc[p, [3, 4, 5]])
                J[lig, :] = partial_deriv.T
                F[lig] = -crit_X0
                lig = lig + 1

            #print('Jacobienne : \n' + str(J))

            JJ = np.dot(J.T, J)
            for i in range(JJ.shape[0]):
                JJ[i, i] = JJ[i, i] * (1.0 + l)

            # ********************************************************************* #
            # A COMPLETER.                                                          #
            delta_solution = np.dot(np.dot(np.linalg.inv(JJ), J.T), F)
            #@ est le produit matriciel                                              #
            delta_extrinsic = matTools.construct_matrix_from_vec(delta_solution)  #
            self.extrinsic_matrix = np.dot(delta_extrinsic, self.extrinsic_matrix)
            #print(self.extrinsic_matrix)
            #dans ce sens sinon ça meurt                                               #
            # ********************************************************************* #

            self.param_solution = matTools.construct_vec_from_matrix(self.extrinsic_matrix)
            self.pick_lines_Rc[:, [0, 1, 2]] = matTools.transform_point_with_matrix(self.extrinsic_matrix, self.pick_lines_Ro[:, [0, 1, 2]])
            self.pick_lines_Rc[:, [3, 4, 5]] = matTools.transform_point_with_matrix(self.extrinsic_matrix, self.pick_lines_Ro[:, [3, 4, 5]])

            new_error = self.calculate_error()
            if new_error < self.EPS or abs(initial_error - new_error) < 10 ** -10:
                break

            print('Iteration[' + str(it) + '] : ' + str(new_error))
            it = it + 1
            initial_error = new_error

        print('6-tuplet solution : ' + str(self.param_solution))
        print('Error after convergence : ' + str(new_error))

        if image_path is not None:

            fig4 = plt.figure(4)
            ax4 = fig4.add_subplot(111)
            plt.imshow( mpimg.imread(image_path))
            transform_and_draw_model(self.model3D_Ro[12:], self.intrinsic_matrix, self.extrinsic_matrix, ax4)  # 3D model drawing
            plt.show(block=True)

        

    def calculate_error(self):
        # ***************************************************************** #
        # A COMPLETER.                                                      #
        # Input:                                                            #
        #   nb_segments : par defaut 5 = nombre de segments selectionnes    #
        #   normal_vectors : ndarray[Nx3] - normales aux plans              #
        #                    d'interpretation des segments selectionnes     #
        #                    N = nombre de segments                         #
        #                    3 = coordonnees (X,Y,Z) des normales dans Rc   #
        #   segments_Rc : ndarray[Nx6] = segments selectionnes dans Ro      #
        #                 et transformes dans Rc                            #
        #                 N = nombre de segments                            #
        #                 6 = (X1, Y1, Z1, X2, Y2, Z2) des points P1 et     #
        #                 P2 des aretes transformees dans Rc                #
        # Output:                                                           #
        #   err : float64 - erreur cumulee des distances observe/attendu    #
        # ***************************************************************** #

        err = 0
        for p in range(self.nb_segments):
            f = np.power(np.dot(self.normal_vectors[p], self.pick_lines_Rc[p,:3]),2) + np.power(np.dot(self.normal_vectors[p], self.pick_lines_Rc[p,3:]),2)
            err = err + f

        err = np.sqrt(err / 2 * self.nb_segments)
        return err


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

    P1_cam = matTools.transform_point_with_matrix(extrinsic, edges_Ro[:,:3])
    P2_cam = matTools.transform_point_with_matrix(extrinsic, edges_Ro[:,3:])

    [u_1, v_1] = perspective_projection(intrinsic, P1_cam)
    [u_2, v_2] = perspective_projection(intrinsic, P2_cam)

    for p in range(edges_Ro.shape[0]):
        fig_axis.plot([u_1[p], u_2[p]], [v_1[p], v_2[p]], 'k')


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


def calculate_normal_vector(p1_Ri, p2_Ri, intrinsic):
    # ********************************************************* #
    # A COMPLETER.                                              #
    # Fonctions utiles disponibles :                            #
    #   np.dot, np.cross, np.linalg.norm, np.linalg.inv         #
    # Input:                                                    #
    #   p1_Ri : list[3]                                         #
    #           3 = (u, v, 1) du premier point selectionne      #
    #   p2_Ri : list[3]                                         #
    #           3 = (u, v, 1) du deuxieme point selectionne     #
    #   intrinsic : ndarray[3x3] des intrinseques               #
    # Output:                                                   #
    #   normal_vector : ndarray[3] contenant la normale aux     #
    #                   segments L1_c et L2_c deduits des       #
    #                   points image selectionnes               #
    # ********************************************************* #
    
    p1_C = np.dot(np.linalg.inv(intrinsic), p1_Ri)
    p2_C = np.dot(np.linalg.inv(intrinsic), p2_Ri)

    l2 = p2_C - p1_C
    l1 = p1_C
    
    normal_vector = np.cross(l1,l2)/np.linalg.norm(np.cross(l1,l2))

    return normal_vector





def partial_derivatives(normal_vector, P_c):
    # ****************************************************ur le segment     #
    #                   auquel appartient P_c                               #
    #   P_c : ndarray[3] le point de l'objet transformé dans Rc             #
    # Output:                                                               #
    #   partial_derivative : ndarray[6] derivee partielle du critere        #
    #               d'erreur pour chacun des parametres extrinseques        #
    #   crit_X0 : float64 - valeur du critere pour les parametres           #
    #               courants, qui servira de valeur initiale avant          #
    #               la mise a jour et le recalcul de l'erreur               #
    # ********************************************************************* #

    X, Y, Z = P_c[0], P_c[1], P_c[2]
    partial_derivative = np.zeros((6))

    # Variable a remplir
    partial_derivative[0] = np.dot(normal_vector, [0 ,-Z, Y])
    partial_derivative[1] = np.dot(normal_vector, [Z ,0, -X])
    partial_derivative[2] = np.dot(normal_vector, [-Y ,X, 0])
    partial_derivative[3] = normal_vector[0]
    partial_derivative[4] = normal_vector[1]
    partial_derivative[5] = normal_vector[2]
    # ********************************************************************
    crit_X0 = normal_vector[0] * X + normal_vector[1] * Y + normal_vector[2] * Z
    return partial_derivative, crit_X0




    # fig5 = plt.figure(5)
    # ax5 = fig5.add_subplot(111)
    # ax5.set_xlim(0, 720)
    # ax5.set_ylim(480)
    # plt.imshow(image_2)

    # # A completer avec la matrice de passage du repere Ro vers Rc2, avec les matrices
    # # Ro -> Rc et Rc -> Rc2
    # Ro_to_Rc2 = ...

    # transform_and_draw_model(model3D_Ro[12:], intrinsic_matrix, Ro_to_Rc2, ax5)
    # plt.show(block=True)

    # ****** Bonus - a decommenter a la fin
    # fig6 = plt.figure(6)
    # ax6, lines = utils.plot_3d_model(model3D_Ro_final, fig6)
    #
    # fig7 = plt.figure(7)
    # ax7 = fig7.add_subplot(111)
    # ax7.set_xlim(0, 720)
    # plt.imshow(image)
    # transform_and_draw_model(model3D_Ro_final[12:], intrinsic_matrix, extrinsic_matrix, ax7)
    # plt.show(block=True)
