from distutils.log import error
from PyQt5.QtCore import pyqtSignal, QThread
from matplotlib import pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.image as mpimg
from mpl_toolkits.mplot3d import Axes3D
from matUtils import *
import cv2
from pnp_from_scratch import pnp

class PNPResultVisualizationWidget(QWidget):
    """
    Widget qui sert a l'integration de matplotlib dans Qt 
    """
    def __init__(self):
        super(PNPResultVisualizationWidget,self).__init__()

        # On lui donne une hauteur fixe mais la largeur change dynamiquement
        self.setFixedWidth(800)
        self.setFixedHeight(800)

        # Figure Matplotlib sur laquelle on fera les plots
        self.fig = Figure()

        # Canvas contenant la figure
        self.canvas = FigureCanvas(self.fig)
        
        # Layout principal pour y mettre le canvas
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

        
    
    def update_canvas(self):
        """Fonction a appeler pour redraw le canvas"""
        self.canvas.draw()


class PNPResultVisualizationThread(QThread):
    """
        Thread qui gere toute la partie calcul de PNP
        Il est important de ce faire les calculs dans un thread separe 
        pour ne pas freeze l'application principale durant les calculs

        Le thread modifie aussi la figure que le Widget affiche
    
    """
    # Signal emit lorsque qu'il faut redraw le canvas 
    # Il est connecte a la fonction update_canvas du widget
    update_plot_signal = pyqtSignal()
    nb_picked_points_signal = pyqtSignal(int)
    update_error_signal = pyqtSignal(float)
    
    def __init__(self, fig):
        """
            Fonction __init__
            le Thread a besoin d'une reference a la figure du widget pour
            pouvoir le modifier directement dans les diffrentes fonction
            (pas ideal)
        """
        super(PNPResultVisualizationThread,self).__init__()

        # Variable indiquant si le thread continue ou non
        self._run_flag = True
        self.fig = fig

        # Variable indiquant si on doit afficher le modele 3D sur la photo
        self.draw_model_pnp_result = False
        
        # Array des points 2D detectes dans l'image 
        self.image_points = np.zeros((2,2))

        self.inliers = None

        # Coefs de distortion de la camera calcule grace a la calibration
        #self.distortion_coefs =  np.array([ -0.11133023,  
        #                                    1.96562876, 
        #                                    -0.00787018, 
        #                                    0.01009623, 
        #                                    -7.61314684])
        
        self.distortion_coefs = np.array([ 1.55284357e-01,
                                            -3.07067931e+00,  
                                            5.16274059e-03, 
                                            -4.78075223e-03,
                                            1.80663250e+01])

        # Matrice des params intrinseque de la camera calcule grace a la calibration
        #self.intrinsic_mat = np.array([ [4.95789049e+03, 0.00000000e+00, 1.39806998e+03],
        #                                [0.00000000e+00, 4.90165198e+03, 6.86145950e+02],
        #                                [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

        self.intrinsic_mat = np.array([ [4.78103205e+03, 0.00000000e+00, 1.20113948e+03],
                                        [0.00000000e+00, 4.77222528e+03, 1.14533714e+03],
                                        [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
        
        # On initialise la matrice extrinseque 
        self.extrinsic_mat = np.array([ [1., 0., 0., 0.],
                                        [0., 1., 0., 0.],
                                        [0., 0., 1., 0.],
                                        [0., 0., 0., 1.]])

        # On recupere la position des trous sur le modele 3D (merci Gael)
        with open('HoleDetection/Points3D/Plaque1.npy', 'rb') as f:
            array = np.load(f, allow_pickle=False)
        
        # On trie les points par diametre descroissant
        # Le diametre est stocke dans la derniere colonne que l'on ne
        # garde pas pour la suite 
        self.holes_point_3D = array[array[:, 3].argsort()][::-1][:, :3]

        # On charge les pts 3D et les eddges qui componsent le model 3D
        # et on construit un model 3D affichable avec matplotlib
        model_points_3DRo = np.loadtxt("Data/Plaque1/Model/Plaque_1.xyz", dtype=float)
        model_edges = np.loadtxt("Data/Plaque1/Model/Plaque_1.edges", dtype=int)

        XYZ1_Ro = model_points_3DRo[model_edges[:, 0]]
        XYZ2_Ro = model_points_3DRo[model_edges[:, 1]]
        self.model3D_Ro = np.concatenate([XYZ1_Ro, XYZ2_Ro], axis=1)
    
        X1_Ro, Y1_Ro, Z1_Ro = XYZ1_Ro[:, 0], XYZ1_Ro[:, 1], XYZ1_Ro[:, 2]
        X2_Ro, Y2_Ro, Z2_Ro = XYZ2_Ro[:, 0], XYZ2_Ro[:, 1], XYZ2_Ro[:, 2]


        
        def on_pick(event, picked_points_Ro):
            """
                Fonction qu'on va lier avec le pick event de la figure du widget
            """
            
            if event.artist in lines:
                
                ind = lines.index(event.artist)
                
                X = (X1_Ro[ind] + X2_Ro[ind]) / 2
                Y = (Y1_Ro[ind] + Y2_Ro[ind]) / 2
                Z = (Z1_Ro[ind] + Z2_Ro[ind]) / 2
                Z = 1.84
                if not (np.equal(np.array([X, Y]), 
                self.holes_point_3D[:,:2]).all(axis=1).any() and \
                    [X, Y, Z] not in picked_points_Ro):
                    return True

                
                picked_points_Ro.append([X, Y, Z])
                self.nb_picked_points_signal.emit(len(picked_points_Ro))

                # Garde des references a ces elements graphiques pour pouvoir les supprimer
                scatter_element = self.axes3D.scatter(X, Y, Z, color='red', marker='x')
                text_element = self.axes3D.text(X, Y, Z, str(len(picked_points_Ro)), color='red')
                self.plot_elements.append(scatter_element)
                self.plot_elements.append(text_element)

                print("[*] 3D Point {:d}: ({:.2f}, {:.2f}, {:.2f})".format(
                    len(picked_points_Ro), X, Y, Z))

        self.picked_lines_RO = []
        
        self.plot_elements = []
        self.axes3D, lines = plot_3d_model(self.model3D_Ro, self.fig, sub=211)
        self.axes3D.scatter(self.holes_point_3D[:,0], self.holes_point_3D[:,1], self.holes_point_3D[:,2])
        self.axes3D.set_zlim(-20,20)
        #A Modifier 
        self.fig.canvas.mpl_connect('pick_event', lambda event: on_pick(event, self.picked_lines_RO))  # Listen to mouse click event within figure 1
        self.axes2D = self.fig.add_subplot(212)

    def run(self):
        self.nb_picked_points_signal.emit(0)
        while self._run_flag:
            self.update_error_signal.emit(self.calculate_error())
            self.sleep(1)


    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

    def undistort(self, xy, iter_num=3):
        k1 = self.distortion_coefs[0]
        k2 = self.distortion_coefs[1]
        p1 = self.distortion_coefs[2]
        p2 = self.distortion_coefs[3]
        k3 = self.distortion_coefs[4]
        fx, fy = self.intrinsic_mat[0, 0], self.intrinsic_mat[1, 1]
        cx, cy = self.intrinsic_mat[:2, 2]
        x, y = xy.astype(float)[:,0], xy.astype(float)[:,1]
        x = (x - cx) / fx
        x0 = x
        y = (y - cy) / fy
        y0 = y
        for _ in range(iter_num):
            r2 = x ** 2 + y ** 2
            k_inv = 1 / (1 + k1 * r2 + k2 * r2**2 + k3 * r2**3)
            delta_x = 2 * p1 * x*y + p2 * (r2 + 2 * x**2)
            delta_y = p1 * (r2 + 2 * y**2) + 2 * p2 * x*y
            x = (x0 - delta_x) * k_inv
            y = (y0 - delta_y) * k_inv
        return np.array((x * fx + cx, y * fy + cy))
    
    def update_image_points(self, points):
        #points_undistorded = cv2.undistortPoints(   points[:,:2].astype(np.float32), 
        #                                            self.intrinsic_mat, 
        #                                            self.distortion_coefs)
        #
        #self.image_points = np.squeeze(points_undistorded, axis=1)
        #
        #self.image_points = self.undistort(points[:,:2]).T

        self.image_points = points[:,:2].astype(np.float32)
        #print(self.image_points.shape)
    
        self.draw_model()
        #print("Updated points :", points)
    
    

    def process_pnp(self):
        
        if len(self.picked_lines_RO) < 4:
            print("You have to pick at least 4 points")
            return False

        object_points = np.array(self.picked_lines_RO, dtype=np.float64)
        image_points = self.image_points[:object_points.shape[0],:]
        image_points = image_points.astype(np.float64)
        
        rotation_guess = np.array([-3.1, 0., 0.])
        translation_guess = np.array([0., 0., 1000.])

        """success, rotation_vector, translation_vector, self.inliers = cv2.solvePnPRansac(
            object_points,
            image_points,
            self.intrinsic_mat,
            self.distortion_coefs,
            useExtrinsicGuess=False,
            flags=0)"""

        success, rotation_vector_list, translation_vector_list, error_list = cv2.solvePnPGeneric(
            object_points,
            image_points,
            self.intrinsic_mat,
            self.distortion_coefs,
            useExtrinsicGuess=False,
            flags=cv2.SOLVEPNP_IPPE,
            reprojectionError=0.0)
        
        #print("Success :", success)

        for rotation_vector, translation_vector, error in zip(rotation_vector_list, translation_vector_list, error_list):

        
            print("Rotation : " + str(rotation_vector))
            print("Translation : " + str(translation_vector))

            self.extrinsic_mat = R_from_vect(np.concatenate([rotation_vector, translation_vector]))

            print("Extrinseque Opencv \n" +  str(self.extrinsic_mat))
            print('Error :' + str(error))
        
        self.extrinsic_mat = R_from_vect(np.concatenate([rotation_vector_list[0], translation_vector_list[0]]))

        return success

    def calculate_error(self):

        if self.inliers is None:
            return -1.

        if len(self.picked_lines_RO) == 0  or self.inliers.shape[0] == 0:
            return -1.
        
        object_points = []
        image_points = []
        for inl in self.inliers:
            object_points.append(self.picked_lines_RO[inl[0]])
            image_points.append(self.image_points[inl[0]])

        object_points = np.array(object_points)
        image_points = np.array(image_points)

        #object_points = np.array(self.picked_lines_RO)
        #image_points = self.image_points[:object_points.shape[0],:]

        P_cam = transform_point_with_matrix(self.extrinsic_mat, object_points)
        u, v  = perspective_projection(self.intrinsic_mat, P_cam)
        reprojected_image_points = np.array([u, v]).T

        error = np.sum(np.sqrt(
            np.dot(reprojected_image_points[:,0] - image_points[:,0], reprojected_image_points[:,0] - image_points[:,0]) + 
            np.dot(reprojected_image_points[:,1] - image_points[:,1], reprojected_image_points[:,1] - image_points[:,1])
            ))/object_points.shape[0]

        
        return error


    def update_draw_model_pnp_result(self, state):
        self.draw_model_pnp_result = state == 2
        self.draw_model()
    
    def clear_picked_lines_RO(self):
        self.picked_lines_RO = []
        self.nb_picked_points_signal.emit(0)
        for plot_element in self.plot_elements:
            plot_element.remove()
        self.plot_elements = []
        self.draw_model()

    def draw_model(self):
        #print("Draw model")
        self.axes2D.cla()
        self.axes2D.imshow(mpimg.imread("./Data/Plaque1/Cognex_LED/image_test.bmp"))
        if self.draw_model_pnp_result:
            transform_and_draw_model(self.model3D_Ro, self.intrinsic_mat, self.extrinsic_mat, self.axes2D)  # 3D model drawing

        self.axes2D.scatter(self.image_points[:, 0], self.image_points[:, 1], marker='x', color='r')
        for i, point in enumerate(self.image_points):
            self.axes2D.text(point[0], point[1], str(i+1), color='white')
        
        self.update_plot_signal.emit()

        


