import matchpoints
import cv2
import numpy as np
import imutils
from matplotlib import pyplot as plt


if __name__ == "__main__":
    
    imgPath = "Data/Plate/image2.bmp"
    # load the image from disk
    image = cv2.imread(imgPath)
    # loop over the rotation angles

    #image = imutils.rotate_bound(image, 135)

    min_value = np.inf
    min_angle = 0
    values = []


    for angle in np.arange(0, 360, 1):
        rotated = imutils.rotate_bound(image, angle)
        rotated = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
        
        mark = matchpoints.findMarkPosition(rotated)
        coord_ligne = matchpoints.detectClosestEdge(rotated, mark[0], mark[1])
        newLine = np.array([[coord_ligne[0], coord_ligne[1]], [coord_ligne[2], coord_ligne[3]]])
        delta = abs(newLine[0, 1]- newLine[1, 1])
        rotated = cv2.circle(rotated, (int(mark[0]), int(mark[1])), 10, (255, 0, 0), 2)
        rotated = cv2.line(rotated, tuple(newLine[0]), tuple(newLine[1]), (255, 0, 0))
        values.append(delta)
        if delta < min_value:
            min_value = delta
            min_angle = angle
        
        #cv2.imshow("Rotated (Correct)", rotated)
        #cv2.waitKey(0)
        
        print(mark)


    print(min_value, min_angle)
    plt.subplot(2, 1, 1)
    plt.imshow(imutils.rotate_bound(image, min_angle))
    plt.subplot(2, 1, 2)
    plt.plot(np.arange(0, 360, 1), values)
    plt.show()