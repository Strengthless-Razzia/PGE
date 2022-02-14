import cv2
import numpy as np
from localisation_exception import UntrustworthyLocalisationError, MatchingError
from hole_detection import hough
from pnp_solving import process_pnp, calcule_erreur
from matUtils import construct_matrix_from_vec
from extractHoles import getAllCircles
import sys
from matchPoints import generatePointLines, removeNonSimilarLines, formatPointsForPnP

def main_localisation(  type_plaque, 
                        chemin_modele, 
                        chemin_image,
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
    
    try:
        photo =  cv2.imread(chemin_image)
    
    except Exception as e:
        print(e)

    image_points = hough(photo)


    try:
        with open(chemin_modele) as f:
            file = f.readlines()
        object_points = getAllCircles(file)
        object_points = np.delete(object_points, 3, axis=1)
        
    except Exception as e:
        print(e)
    
    #================================ Matching des points ================================

    try:
        lines3D, lines2D = generatePointLines(chemin_image,  image_points, chemin_modele)
        lines2D,lines3D = removeNonSimilarLines(lines2D,lines3D)
        readyForPnP_2D, readyForPnP_3D = formatPointsForPnP(lines2D,lines3D)

    except Exception as e:
        raise MatchingError(str(e))

    # S'assurer que les objects points image points sont de taille (n, 3) et (n, 2) avec n >= 4

    print(readyForPnP_2D.shape)
    print(readyForPnP_3D.shape)

    try:
        rotation_vector, translation_vector, inliers = process_pnp(readyForPnP_3D, readyForPnP_2D, matrice_intrinseque, coefficients_de_distortion)

    except Exception as e:
        print(e)

    try:
        matrice_extrinseque = construct_matrix_from_vec(np.concatenate([rotation_vector, translation_vector]))

    except Exception as e:
        print(e)

    try:
        erreur = calcule_erreur(readyForPnP_3D, readyForPnP_2D, inliers, matrice_extrinseque, matrice_intrinseque)
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
        "Data/Plaque1/Model/Plaque_1.stp", 
        "HoleDetection/ShittyDataset/1.bmp", 
        None, 
        None, 
        intrinsic_mat, 
        distortion_coefs)