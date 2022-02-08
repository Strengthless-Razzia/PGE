from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QPushButton, QCheckBox, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont
import sys
import cv2
from PyQt5.QtCore import pyqtSlot, Qt
import numpy as np
from slider_widget import CustomSlider

from hough_visualization_thread import HoughVisualizationThread
from pnp_result_visualization import PNPResultVisualizationWidget, PNPResultVisualizationThread


class App(QWidget):
    def __init__(self):
        super(App,self).__init__()
        self.setWindowTitle("Qt hough parametres")
        self.disply_width = 1000
        self.display_height = 1000
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabelParam = QLabel('Parametres')
        self.textLabelTitle= QLabel('Hough Hole Detection')
        
        # create sliders
        self.p1_slider = CustomSlider(100., 1.0, 200., "p1")
        self.p2_slider = CustomSlider(30., 1.0, 200., "p2")

        self.minR_slider = CustomSlider(0., 0., 100., "minR")
        self.maxR_slider = CustomSlider(100., 0., 100., "maxR")
        self.minDist_slider = CustomSlider(150., 0., 500., "minDist")
        self.brightness_value_slider = CustomSlider(10., 0., 100., "brightness")    
        

        vbox_hough = QVBoxLayout()
        vbox_hough.addWidget(self.textLabelTitle)
        vbox_hough.addWidget(self.image_label)
        vbox_hough.addWidget(self.textLabelParam)
        
        vbox_hough.addWidget(self.p1_slider)
        vbox_hough.addWidget(self.p2_slider)

        vbox_hough.addWidget(self.minR_slider)
        vbox_hough.addWidget(self.maxR_slider)
        vbox_hough.addWidget(self.minDist_slider)
        vbox_hough.addWidget(self.brightness_value_slider)
        
        
        textLabelTitlePnP = QLabel("PnP solving")
        self.solvePNPButton = QPushButton("SOLVE PNP", self)
        self.solvePNPButton.setFixedHeight(80)
        self.solvePNPButton.setStyleSheet("background-color: red; color: white")
        font_button = QFont('Times', 20)
        font_button.setBold(True)
        self.solvePNPButton.setFont(font_button)
        draw_pnp_result_checkbox = QCheckBox(self)
        draw_pnp_result_checkbox.setText("Draw Model on Image")
        clear_object_points_button  = QPushButton("Clear 3D points", self)
        self.pnp_widget = PNPResultVisualizationWidget()
        self.error_label = QLabel("-1")
        font_error = QFont('Times', 20)
        font_error.setBold(True)
        self.error_label.setFont(font_error)
        

        vbox_pnp = QVBoxLayout()
        vbox_pnp.addWidget(textLabelTitlePnP)
        vbox_pnp.addWidget(self.solvePNPButton)
        vbox_pnp.addWidget(draw_pnp_result_checkbox)
        vbox_pnp.addWidget(clear_object_points_button)
        vbox_pnp.addWidget(self.pnp_widget)
        vbox_pnp.addWidget(QLabel("Error"))
        vbox_pnp.addWidget(self.error_label)


        mainbox = QHBoxLayout()
        mainbox.addLayout(vbox_hough)
        mainbox.addLayout(vbox_pnp)
        self.setLayout(mainbox)

        # create the video capture thread
        self.threadHough = HoughVisualizationThread()
        self.threadPNP = PNPResultVisualizationThread(self.pnp_widget.fig)
        # connect its signal to the update_image slot
        self.threadHough.change_pixmap_signal.connect(self.update_image)
        self.threadHough.change_points_signal.connect(self.threadPNP.update_image_points)
        self.threadPNP.update_plot_signal.connect(self.pnp_widget.update_canvas)
        self.threadPNP.nb_picked_points_signal.connect(self.update_button)
        self.threadPNP.update_error_signal.connect(self.update_error)

        self.solvePNPButton.clicked.connect(self.threadPNP.process_pnp)
        draw_pnp_result_checkbox.stateChanged.connect(self.threadPNP.update_draw_model_pnp_result)
        clear_object_points_button.clicked.connect(self.threadPNP.clear_picked_lines_RO)
        # connect sliders

        self.p1_slider.valueChangedSignal.connect(self.threadHough.update_p1)
        self.p2_slider.valueChangedSignal.connect(self.threadHough.update_p2)
        self.minR_slider.valueChangedSignal.connect(self.threadHough.update_minR)
        self.maxR_slider.valueChangedSignal.connect(self.threadHough.update_maxR)
        self.minDist_slider.valueChangedSignal.connect(self.threadHough.update_minDist)
        self.brightness_value_slider.valueChangedSignal.connect(self.threadHough.update_brightness_value)
        # start the thread
        self.threadHough.start()
        self.threadPNP.start()

    def closeEvent(self, event):
        self.threadHough.stop()
        self.threadPNP.stop()
        event.accept()


    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
    def update_button(self, nb_points):
        self.solvePNPButton.setText("SOLVE P-{:d}-P".format((nb_points)))
        self.solvePNPButton.setEnabled(nb_points >= 4)
    
    def update_error(self, error):
        self.error_label.setText("{:.2f}".format(error))

    
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())