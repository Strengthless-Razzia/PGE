"""
@file fusion.py
@brief Ce programme fusionne la detection de ligne de Hough avec la detection d'angle de Harris. 
Permet d'obtenir une detection d'angle renforcé pouvant etre utilisee pour la localisation d'un objet 3D type plaque.
"""
from matplotlib import pyplot as plt
import numpy as np
import cv2 as cv
import math
import sys
import os

from HoughLineDetection import *
from cornerDetection import *


if __name__ == "__main__":
    #For all img files in directory dataset
    listOfFiles = os.listdir("Codes/merging_code/dataset")
    for f in listOfFiles:
        if ".png" in f or ".jpg" in f:
            a_t = 0.5
            b_t = 5
            imgPath = "Codes/merging_code/dataset/"+f

            lines = getHoughLines(imgPath)
            
            old = lines.shape
            mergedList=mergeSimilarLines(lines,a_t,b_t)
            
            new = mergedList.shape
            while new!= old:
                old = mergedList.shape
                mergedList=mergeSimilarLines(mergedList,a_t,b_t)
                new = mergedList.shape
            cleanedList = removeSimilarLines(mergedList,10)

            displayImgWithLines(imgPath, cleanedList, "Cleaned")
            displayHarrisCorner(imgPath)