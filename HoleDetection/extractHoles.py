import numpy as np

def extractCircles(file):
    circles = []
    for currentLine in file:
        if "CIRCLE" in currentLine:
            circles.append(currentLine)
    return circles

def findLineWithId(id, file):
    for line in file:
        if id+"=" in line:
            return line
    return None

def parseCircle(circle, file, debug=False):
    [id,circle] = circle.split("=")
    [trash,circle] = circle.split("(")
    [circle,trash] = circle.split(")")
    [trash,centerId,diameter] = circle.split(",")
        
    foundLine = findLineWithId(centerId, file)
    
    parsed = foundLine.split(",")
    repereId = parsed[1]

    foundLine = findLineWithId(repereId, file)
    [trash, trash,position] = foundLine.split("(")
    [position, trash,trash] = position.split(")")
    [x, y, z] = position.split(",")

    

    positionPoint = (float(x),float(y),float(z))
    if debug:
        print("id : ", id)
        print("diameter : ", diameter)
        print("x y z : ",positionPoint)
    return positionPoint,float(diameter)

def arraysEqual(a,b):
    return a[0] == b[0] and a[1] == b[1] and a[2] == b[2]

def cleanupSimilar(pos3D, d):
    i = 0
    while i < len(pos3D):
        j=0
        while j < len(pos3D):
            if i==j:
                j+=1
                continue

            if arraysEqual(pos3D[i], pos3D[j]):
                pos3D = np.delete(pos3D, j,axis=0)
                d = np.delete(d, j,axis=0)
            j+=1
        i+=1
    return pos3D,d


def getAllCircles(file, getBothFaces=False):
    Circles = extractCircles(file)
    pos_3D = np.zeros([len(Circles),3])
    diameters = np.zeros([len(Circles),1])

    for i in range(len(Circles)):
        [currentPos, currentD] = parseCircle(Circles[i],file)    
        pos_3D[i] = currentPos
        diameters[i] = currentD
    
    pos_3D = np.unique(pos_3D,axis=0) 


    #[pos_3D,diameters] = cleanupSimilar(pos_3D,diameters)
    if not getBothFaces:
        i = 0
        while i < len(pos_3D):
            if pos_3D[i][2] == 0:
                pos_3D = np.delete(pos_3D,i,axis=0)
                diameters = np.delete(diameters,i,axis=0)
            i+=1

    return pos_3D , diameters   

if __name__ == '__main__':
    #Seul code a comprendre, is okay
    with open('./Data/Plaque1/Model/Plaque_1.stp') as f:
        file = f.readlines()

    [points_3D,diameters] = getAllCircles(file, getBothFaces=False) #getBothFaces si vous voulez aussi les points qui correspondent au dessous de la plaque, probablement useless mais sait-on jamais
    #ONLY USE POINTS3D, DIAMETERS DONT WORK WOOPSIE

    print(points_3D)
    #print(diameters.shape)
