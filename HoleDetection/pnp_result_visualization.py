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
from extractHoles import getAllCircles

class PNPResultVisualizationWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedHeight(800)
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111)

        layout = QVBoxLayout(self)

        layout.addWidget(self.canvas)

        

    def update_canvas(self):
        self.canvas.draw()

class PNPResultVisualizationThread(QThread):

    update_plot_signal = pyqtSignal()

    def __init__(self, fig_axis) -> None:
        super().__init__()
        self._run_flag = True
        self.fig_axis = fig_axis
        
        self.image_points = np.array([[0.,0.], [1., 1.], [2., 2.], [3., 3.]])

        self.distortion_coefs =  np.array([ -0.11133023,  
                                            1.96562876, 
                                            -0.00787018, 
                                            0.01009623, 
                                            -7.61314684])

        self.intrinsic_mat = np.array([ [4.95789049e+03, 0.00000000e+00, 1.39806998e+03],
                                        [0.00000000e+00, 4.90165198e+03, 6.86145950e+02],
                                        [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
        
        self.extrinsic_mat = np.ones((4,4))

        self.step_file_path = "Data/Plaque1/Model/Plaque_1.stp"
        with open(self.step_file_path) as f:
            file = f.readlines()
        self.holes_point_3D, diameters = getAllCircles(file, getBothFaces=False)

        model_points_3DRo = np.loadtxt("Data/Plaque1/Model/Plaque_1.xyz", dtype=float)
        model_edges = np.loadtxt("Data/Plaque1/Model/Plaque_1.edges", dtype=int)

        XYZ1_Ro = model_points_3DRo[model_edges[:, 0]]
        XYZ2_Ro = model_points_3DRo[model_edges[:, 1]]
        self.model3D_Ro = np.concatenate([XYZ1_Ro, XYZ2_Ro], axis=1)
        

    def run(self):
    
        while self._run_flag:
            self.process_pnp()
            self.draw_model()
            self.update_plot_signal.emit()
            self.sleep(2)

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
    
    def update_image_points(self, points):
        self.image_points = points[:,:2]
        #print("Updated points :", points)

    def process_pnp(self):
        #print("Process pnp")
        # A changer
        holes_point_3D = self.holes_point_3D[:self.image_points.shape[0],:]

        #print(holes_point_3D.shape, self.image_points.shape)


        success, rotation_vector, translation_vector, inliners = cv2.solvePnPRansac(
            holes_point_3D, 
            self.image_points, 
            self.intrinsic_mat, 
            self.distortion_coefs,
            flags=0)
        
        #print("Success :", success)

        self.extrinsic_mat = construct_matrix_from_vec(np.concatenate([rotation_vector, translation_vector]))


    def draw_model(self):
        #print("Draw model")
        self.fig_axis.cla()
        self.fig_axis.imshow(mpimg.imread("./Data/Plaque1/Cognex/image1.bmp"))
        #transform_and_draw_model(self.model3D_Ro, self.intrinsic_mat, self.extrinsic_mat, self.fig_axis)  # 3D model drawing

        self.fig_axis.scatter(self.image_points[:, 0], self.image_points[:, 1], marker='x', color='r')


