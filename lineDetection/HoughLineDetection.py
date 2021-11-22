"""
@file hough_lines.py
@brief This program demonstrates line finding with the Hough transform
"""
import math
import os
import cv2 as cv
import numpy as np

def getCenter(l):
    
    x1 = l[0]
    y1 = l[1]
    x2 = l[2]
    y2 = l[3]
    centerX = (x2+x1)/2
    centerY = (y2+y1)/2
    
    return (int(centerX),int(centerY))


def main(img):
    
    # Loads an image
    src = cv.imread(img, cv.IMREAD_GRAYSCALE)
    # Check if image is loaded fine
    if src is None:
        print ('Error opening image!')
        return -1
    
    
    dst = cv.Canny(src, 50, 200, None, 3)
    
    # Copy edges to the images that will display the results in BGR
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)
    
    lines = cv.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)
    
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv.line(cdst, pt1, pt2, (0,0,255), 1, cv.LINE_AA)
    
    
    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)
    
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 1, cv.LINE_AA)
            



    cv.imshow("Source", src)
    cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
    cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)
    
    cv.waitKey()
    return linesP

listOfLines = {}

if __name__ == "__main__":
    listOfFiles = os.listdir("lineDetection\dataset")
    for f in listOfFiles:
        if ".png" in f or ".jpg" in f:
            listOfLines[f] = main("lineDetection\\dataset\\"+f)
    print(listOfLines)
    files = listOfLines.keys()
    for currentFile in files:
        for currentLine in listOfLines[currentFile]:
            currentLine =currentLine[0]
            print(str(currentFile) + " : " + str(currentLine))
            ctr = getCenter(currentLine)
            src = cv.imread("lineDetection\\dataset\\"+currentFile)
            cv.line(src, [currentLine[0],currentLine[1]], [currentLine[2],currentLine[3]], (0,0,255), 1, cv.LINE_AA)
            cv.circle(src,ctr,2,(0,255,0))
            cv.imshow("LineDisplay",src)
            cv.waitKey()