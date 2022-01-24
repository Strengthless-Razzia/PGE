from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
from slider_widget import CustomSlider

from hough_visualization_thread import HoughVisualizationThread





class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt hough parametres")
        self.disply_width = 1000
        self.display_height = 1000
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabel = QLabel('Parametres')
        
        # create sliders
        self.p1_slider = CustomSlider(30, 1.0, 100, "p1")
        self.p2_slider = CustomSlider(7, 1.0, 100, "p2")

        self.minR_slider = CustomSlider(10, 0, 100, "minR")
        self.maxR_slider = CustomSlider(60, 0, 100, "maxR")
        self.minDist_slider = CustomSlider(295, 0, 500, "minDist")
        self.brightness_value_slider = CustomSlider(10, 0, 100, "brightness")

        # create a vertical box layout and add the two labels and sliders
        mainbox = QVBoxLayout()
        mainbox.addWidget(self.image_label)

        vbox = QVBoxLayout()
        vbox.addWidget(self.textLabel)
        
        vbox.addWidget(self.p1_slider)
        vbox.addWidget(self.p2_slider)

        vbox.addWidget(self.minR_slider)
        vbox.addWidget(self.maxR_slider)
        vbox.addWidget(self.minDist_slider)
        vbox.addWidget(self.brightness_value_slider)
        # set the vbox layout as the widgets layout
        mainbox.addLayout(vbox)
        self.setLayout(mainbox)

        # create the video capture thread
        self.thread = HoughVisualizationThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # connect sliders

        self.p1_slider.valueChangedSignal.connect(self.thread.update_p1)
        self.p2_slider.valueChangedSignal.connect(self.thread.update_p2)
        self.minR_slider.valueChangedSignal.connect(self.thread.update_minR)
        self.maxR_slider.valueChangedSignal.connect(self.thread.update_maxR)
        self.minDist_slider.valueChangedSignal.connect(self.thread.update_minDist)
        self.brightness_value_slider.valueChangedSignal.connect(self.thread.update_brightness_value)
        # start the thread
        self.thread.start()

    def closeEvent(self, event):
        self.thread.stop()
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
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())