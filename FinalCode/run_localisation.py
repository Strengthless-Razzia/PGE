#!/usr/bin/env python
# coding: utf-8

import numpy as np
import rospy
import rospkg
from deplacement_robot.srv import Robot_move_predef, Move_predef
from deplacement_robot.msg import Localisation
from communication.srv import capture
from cv_bridge import CvBridge
from useful_robot import pose_msg_to_homogeneous_matrix,get_fk
from pyquaternion import Quaternion
from main_loc import main_localisation as main_loc
from localisation_exception import UntrustworthyLocalisationError, MatchingError
from localisation_cognex import localisation
import matplotlib.pyplot as plt



def pub_state(pub, msg):
    if not pub is None:
        pub.publish(msg)

def localiser(type_plaque,model_path,image,M_hom_3D,M_pass_oc,M_intr,coeff_distr):
    try:
        trans,rot,matrice_extr,bryant = main_loc(type_plaque,model_path,image,M_hom_3D,M_pass_oc,M_intr,coeff_distr)
        #trans,rot,matrice_extr,bryant = localisation(type_plaque,model_path,image,M_hom_3D,M_pass_oc,M_intr,coeff_distr)
        return trans,rot,matrice_extr,bryant
    except(UntrustworthyLocalisationError,MatchingError),e:
        return str(e)

def move_to_point(p,pub=None):
    pub_state(pub,"moving to point "+str(p))
    move_robot = rospy.ServiceProxy("move_predef", Move_predef)
    move_robot("localisation_"+str(p))
   


def send_results(pts):
    message = Localisation()
    bridge=CvBridge()
    message.x = pts[0]
    message.y = pts[1]
    message.z = pts[2]
    message.a = pts[3]
    message.b = pts[4]
    message.g = pts[5]
    message.image = bridge.cv2_to_compressed_imgmsg(get_image())

def get_image():
    #capturer l'image
    bridge=CvBridge()
    capture_image = rospy.ServiceProxy("camera/capture", capture)
    img = capture_image()
    rosimage = img.image
    cv_image = bridge.imgmsg_to_cv2(rosimage,'bgr8')
    
    assert (len(cv_image.shape) == 3),"(1) probleme dimensions, image BGR ?"
    return cv_image



def run_localisation(path,pub=None):
    distortion_coefs = np.array([   1.55284357e-01,
                                    -3.07067931e+00,  
                                    5.16274059e-03, 
                                    -4.78075223e-03,
                                    1.80663250e+01])

    intrinsic_mat = np.array([  [4.78103205e+03, 0.00000000e+00, 1.20113948e+03],
                                [0.00000000e+00, 4.77222528e+03, 1.14533714e+03],
                                [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
    
    M_pass_oc = np.array([                [ 0.,  -1.,  0., -0.035],
                                          [1.,  0.,  0., -0.035],
                                          [ 0.,  0.,  1., 0.05],
                                          [ 0.,   0.,  0.,1.]])
    move_parking = rospy.ServiceProxy('move_robot_parking', Robot_move_predef)
    for i in range(4):
        move_to_point(i+1)
        #capturer l'image
        img = get_image()
        pose_get_fk = get_fk()
        Mtrix_hom_3D = pose_msg_to_homogeneous_matrix(pose_get_fk)
        try:
            res = localiser(type_plaque="Tole plate",model_path=path,image=img,M_hom_3D=Mtrix_hom_3D,M_pass_oc=M_pass_oc,M_intr=intrinsic_mat,coeff_distr=distortion_coefs)
	   
	    if not res is None:
                trans, rot, extrinseque, bryant = res
                print(extrinseque)
                print(bryant)
                pub_state(pub,"plaque localisée avec sucess")
                move_parking()
                pub_state(pub,"moving back to parking")
                #send_results([trans,rot])
                break
        except (TypeError,ValueError) , e:
            pub_state(pub,"plaque non trouvée")
	    print(e)

	except MatchingError as e:
            pub_state(pub,"Erreur de matching")

        except UntrustworthyLocalisationError as e:
	    pub_state(pub,"L'erreur de localisation est trop grande")
	
	except Exception as e:
            pub_state(pub,"Autre erreurs")
	    print(type(e))

  


if __name__ == "__main__":
    rospy.init_node('test_localisation', anonymous=True)
    rospack = rospkg.RosPack()
    path = rospack.get_path("deplacement_robot")+"/plaques/Tole plate.stp"
    run_localisation(path)


