import cv2
from PyQt5.QtCore import pyqtSignal, QThread
import numpy as np


class PNPResultVisualization(QThread):
    def __init__(self,) -> None:
        super().__init__()
        self._run_flag = True

    def run(self):
    
        while self._run_flag:
            pass

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()