from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
from slider_widget import CustomSlider

class HoughVisualizationThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.original_image = cv2.imread("Data/Plaque1/PhotoUnity/plaque=1_position=(0.0, -1800.0, 0.0)_rotation=(270.0, 0.0, 0.0)_date=2022-01-19_14-19-15.png")

        self.p1 = 30
        self.p2 = 7
        self.blur = 5
        self.dp = 1.5
        self.minDist = 295 #270
        self.minR = 10
        self.maxR = 60
        self.minV = 10
        self.maxV = 60
        self.brightness_value = 10
    
    def increase_brightness(self, img, value=10):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        limLow = 155 - value #200
        limHigh = 205 - value #200

        bright_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        rows = img.shape[0]
        cols=img.shape[1]
        brightness = np.sum(bright_img) / (255 * cols * rows)
        #print(brightness)
        if (brightness <0.28 or brightness>0.33): #while 0.4
            v[v <= limLow] += value
            v[v >= limHigh] -= value
            final_hsv = cv2.merge((h, s, v))
            img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
            bright_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            brightness = np.sum(bright_img) / (255 * cols * rows)
            #print(brightness)

        return img

    def hough(self):
        #increase brightness
        img = self.increase_brightness(self.original_image.copy(), value=self.brightness_value)
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #adaptive threshold
        imgGray = cv2.medianBlur(imgGray, self.blur)
        imgGray = cv2.adaptiveThreshold(imgGray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,41,3) #41
        imgGray = cv2.medianBlur(imgGray, self.blur)
        imgGray[imgGray ==1] = 255
        #kernel = np.ones((7,7),np.uint8)
        kernel = cv2.getStructuringElement(shape=cv2.MORPH_ELLIPSE, ksize=(9,9))
        imgGray = cv2.morphologyEx(imgGray, cv2.MORPH_OPEN, kernel)

        circles = cv2.HoughCircles(imgGray, cv2.HOUGH_GRADIENT, self.dp, self.minDist,
                                    param1=self.p1,param2=self.p2,minRadius=self.minR,maxRadius=self.maxR)
    
        imgCanny = cv2.Canny(imgGray, self.p1//2, self.p1)
        nb_c = 0
        if( not (circles is None)):
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                if i[2] >= self.minV and i[2] <= self.maxV:
                    cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),10)
                    cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
                    nb_c += 1

        return np.concatenate((img, cv2.cvtColor(imgCanny, cv2.COLOR_GRAY2BGR)), axis=0)

    def run(self):
    
        while self._run_flag:
            self.change_pixmap_signal.emit(self.hough())

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

    def update_p1(self, p1):
        self.p1 = abs(p1)
    
    def update_p2(self, p2):
        self.p2 = abs(p2)
    
    def update_minR(self, minR):
        self.minR = int(minR)

    def update_maxR(self, maxR):
        self.maxR = int(maxR)
    
    def update_minDist(self, minDist):
        self.maxminDist = int(minDist)

    def update_brightness_value(self, brightness_value):
        self.brightness_value = int(brightness_value)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt hough parametres")
        self.disply_width = 1000
        self.display_height = 600
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
        mainbox = QHBoxLayout()
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