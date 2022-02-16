import cv2
from PyQt5.QtCore import pyqtSignal, QThread
import numpy as np

class HoughVisualizationThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    change_points_signal = pyqtSignal(np.ndarray)
    

    def __init__(self):
        super(HoughVisualizationThread,self).__init__()
        self._run_flag = True
        self.original_image = cv2.imread("./HoleDetection/ShittyDataset/image4.bmp")
        self.p1 = 100
        self.p2 = 20
        self.blur = 5
        self.dp = 1
        self.minDist = 150 #270
        self.minR = 0
        self.maxR = 100
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
        img = self.original_image.copy()
        #img = self.increase_brightness(self.original_image.copy(), value=self.brightness_value)
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #adaptive threshold
        imgGray = cv2.medianBlur(imgGray, self.blur)
        #imgGray = cv2.adaptiveThreshold(imgGray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,41,3) #41
        #imgGray = cv2.medianBlur(imgGray, self.blur)
        #imgGray[imgGray ==1] = 255
        #kernel = np.ones((7,7),np.uint8)
        #kernel = cv2.getStructuringElement(shape=cv2.MORPH_ELLIPSE, ksize=(9,9))
        #imgGray = cv2.morphologyEx(imgGray, cv2.MORPH_OPEN, kernel)

        circles = cv2.HoughCircles(imgGray, cv2.HOUGH_GRADIENT, self.dp, self.minDist,
                                    param1=self.p1,param2=self.p2,minRadius=self.minR,maxRadius=self.maxR)
    
        imgCanny = cv2.Canny(imgGray, self.p1//2, self.p1)
        nb_c = 0
        if( not (circles is None)):
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),10)
                cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
                nb_c += 1

        return np.concatenate((img, cv2.cvtColor(imgCanny, cv2.COLOR_GRAY2BGR)), axis=1), circles[0,:]

    def run(self):
    
        while self._run_flag:
            image, points = self.hough()
            self.change_pixmap_signal.emit(image)
            self.change_points_signal.emit(points)
            self.sleep(2)

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
