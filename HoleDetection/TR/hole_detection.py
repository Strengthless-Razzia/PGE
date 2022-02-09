import cv2
import numpy as np

def increase_brightness(img, value=20):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    limLow = 155 - value #200
    limHigh = 205 - value #200

    bright_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    rows = img.shape[0]
    cols=img.shape[1]
    brightness = np.sum(bright_img) / (255 * cols * rows)
    print(brightness)
    if (brightness <0.28 or brightness>0.33): #while 0.4
        v[v <= limLow] += value
        v[v >= limHigh] -= value
        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        bright_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        brightness = np.sum(bright_img) / (255 * cols * rows)
        print(brightness)

    return img

#Partie test des paramètres
def le_hough(img, minV=10,maxV=60):
    
    blur = 5
    dp = 1
    minDist = 295 #270
    p1 = 30    #55 #100
    p2 = 7  #7   #5
    minR = 10
    maxR = 60

    imgOrg= img.copy()
    #increase brightness
    img = increase_brightness(img)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #adaptive threshold
    imgGray = cv2.medianBlur(imgGray,blur)
    imgGray = cv2.adaptiveThreshold(imgGray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,41,3) #41
    imgGray = cv2.medianBlur(imgGray,blur)
    imgGray[imgGray ==1] = 255
    #kernel = np.ones((7,7),np.uint8)
    kernel = cv2.getStructuringElement(shape=cv2.MORPH_ELLIPSE, ksize=(9,9))
    imgGray = cv2.morphologyEx(imgGray, cv2.MORPH_OPEN, kernel)

    circles = cv2.HoughCircles(imgGray, cv2.HOUGH_GRADIENT, dp, minDist,
                                param1=p1,param2=p2,minRadius=minR,maxRadius=maxR)
    imgCanny = cv2.Canny(imgGray, p1//2, p1)
    nb_c =0
    if( not (circles is None)):
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            if i[2] >= minV and i[2] <= maxV:
                cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),10)
                cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
                nb_c += 1

    #imgOrg = cv2.resize(imgOrg, (400,600))
    #img = cv2.resize(img, (400,600))
    #imgGray = cv2.resize(imgGray, (400,600))
    #imgCanny = cv2.resize(imgCanny, (400,600))

    show = np.concatenate((
        np.concatenate((imgOrg,img),axis=1),
        cv2.cvtColor(np.concatenate((imgGray,imgCanny), axis=1),cv2.COLOR_GRAY2BGR)
        ), axis=0)
    return show, nb_c, circles

if __name__ == '__main__':
    
    img = cv2.imread('./Data/Plaque1/CameraAIP/capture.png')

    
    #pitit pixel
    show, nb_c, circles = le_hough(img, 14, 60)
    cv2.imwrite("./HoleDetection/result.jpg", show)

    print(circles)

    cv2.waitKey(0) 

    #closing all open windows 
    cv2.destroyAllWindows() 