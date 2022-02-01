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

        # Coefs de distortion de la camera calcule grace a la calibration
        self.distortion_coefs =  np.array([ -0.11133023,  
                                            1.96562876, 
                                            -0.00787018, 
                                            0.01009623, 
                                            -7.61314684])

        # Matrice des params intrinseque de la camera calcule grace a la calibration
        self.intrinsic_mat = np.array([ [4.95789049e+03, 0.00000000e+00, 1.39806998e+03],
                                        [0.00000000e+00, 4.90165198e+03, 6.86145950e+02],
                                        [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
        
        # On initialise la matrice extrinseque 
        self.extrinsic_mat = np.ones((4,4))

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
            #self.process_pnp()
            self.draw_model()
            self.update_plot_signal.emit()
            self.sleep(2)

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
    
    def update_image_points(self, points):
        self.image_points = points[:,:2].astype(np.float32)
        #print("Updated points :", points)

    def process_pnp(self):
        
        if len(self.picked_lines_RO) < 4:
            print("You have to pick at least 4 points")
            return False

        object_points = np.array(self.picked_lines_RO)
        image_points = self.image_points[:object_points.shape[0],:]



        #rotation_matrix, t_vec = pnp(object_points, image_points, self.intrinsic_mat)

        #self.extrinsic_mat_remi[:3,:3] = rotation_matrix
        #self.extrinsic_mat_remi = np.ones((4, 4))
        #self.extrinsic_mat_remi[:3,3] = t_vec.T

        success, rotation_vector, translation_vector = cv2.solvePnP(
            object_points,
            image_points,
            self.intrinsic_mat,
            self.distortion_coefs,
            flags=0)
        
        #print("Success :", success)

        self.extrinsic_mat = construct_matrix_from_vec(np.concatenate([rotation_vector, translation_vector]))

        #print("Extrinseque Remi \n", self.extrinsic_mat_remi)
        print("Extrinseque Opencv \n", self.extrinsic_mat)

        #self.extrinsic_mat = self.extrinsic_mat_remi
        return success

    def update_draw_model_pnp_result(self, state):
        self.draw_model_pnp_result = state == 2
    
    def clear_picked_lines_RO(self):
        self.picked_lines_RO = []
        self.nb_picked_points_signal.emit(0)
        for plot_element in self.plot_elements:
            plot_element.remove()
        self.plot_elements = []

    def draw_model(self):
        #print("Draw model")
        self.axes2D.cla()
        self.axes2D.imshow(mpimg.imread("./Data/Plaque1/Cognex_LED/image2.bmp"))
        if self.draw_model_pnp_result:
            transform_and_draw_model(self.model3D_Ro, self.intrinsic_mat, self.extrinsic_mat, self.axes2D)  # 3D model drawing

        self.axes2D.scatter(self.image_points[:, 0], self.image_points[:, 1], marker='x', color='r')
        for i, point in enumerate(self.image_points):
            self.axes2D.text(point[0], point[1], str(i+1), color='white')

        


