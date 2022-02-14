import cv2
import numpy as np
from localisation_exception import UntrustworthyLocalisationError
from hole_detection import hough
from pnp_solving import process_pnp, calcule_erreur
from matUtils import construct_matrix_from_vec
import sys

def main_localisation(  type_plaque, 
                        chemin_modele, 
                        photo,
                        matrice_homogene_3D_outils,
                        matrice_passage_outils_cam,
                        matrice_intrinseque,
                        coefficients_de_distortion):
    """main_localisation does blah blah blah.

    :type_plaque: "Tole cintree" ou "Tole plate" ou Tole epaisse"
    :chemin_modele: 
    :photo: 
    :matrice_homogene_3D_outils:
    :matrice_passage_outils_cam:
    :matrice_intrinseque:
    :coefficients_de_distortion:
    :return: [x, y, z, alpha, beta, gamma], matrice_extrinseque dans le repere monde OU None si la plaque n'est pas detectee"""
    

    image_points = hough(photo)

    try:
        # On recupere la position des trous sur le modele 3D (merci Gael)
        with open(chemin_modele, 'rb') as f:
            object_points = np.load(f, allow_pickle=False)[:,:3]

    except FileNotFoundError:
        print("Fichier " + str(chemin_modele) + " non trouve")
        

    except OSError:
        print("Impossible d'ouvrir/lire le fichier:", chemin_modele)
        

    except Exception as e:
        print("Numpy n'a pas reussi a ouvrir le fichier:", chemin_modele, e)
        

    #================================ Matching des points ================================


    # S'assurer que les objects points image points sont de taille (n, 3) et (n, 2) avec n >= 4

    print(image_points.shape)
    print(object_points.shape)

    try:
        rotation_vector, translation_vector, inliers = process_pnp(object_points, image_points, matrice_intrinseque, coefficients_de_distortion)

    except Exception as e:
        print(e)

    try:
        matrice_extrinseque = construct_matrix_from_vec(np.concatenate([rotation_vector, translation_vector]))

    except Exception as e:
        print(e)

    try:
        erreur = calcule_erreur(object_points, image_points, inliers, matrice_extrinseque, matrice_intrinseque)
        print(inliers)
        print(erreur)
    except Exception as e:
        print(e)

    if erreur == -1.:
        return None

    elif erreur > 3:
        raise UntrustworthyLocalisationError(erreur)
    

    # ================================ Transformation dans le repere monde ================================

    return translation_vector, rotation_vector, matrice_extrinseque
    



if __name__ == "__main__":

    distortion_coefs = np.array([   1.55284357e-01,
                                    -3.07067931e+00,  
                                    5.16274059e-03, 
                                    -4.78075223e-03,
                                    1.80663250e+01])


    intrinsic_mat = np.array([  [4.78103205e+03, 0.00000000e+00, 1.20113948e+03],
                                [0.00000000e+00, 4.77222528e+03, 1.14533714e+03],
                                [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])


    main_localisation(
        "Tole plate", 
        'HoleDetection/Points3D/Plaque1.npy', 
        cv2.imread("./Data/Plaque1/Cognex_LED/image2.bmp"), 
        None, 
        None, 
        intrinsic_mat, 
        distortion_coefs)