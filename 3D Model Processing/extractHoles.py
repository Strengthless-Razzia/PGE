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



def getAllCircles(file, getBothFaces=False):
    Circles = extractCircles(file)
    pos_3D = np.zeros([len(Circles),3])
    diameters = np.zeros([len(Circles),1])


    for i in range(len(Circles)):
        [currentPos, currentD] = parseCircle(Circles[i],file)    
        results[i][0:3] = currentPos
        results[i][3] = currentD
    
    results = np.unique(results,axis=0) 


    if not getBothFaces:
        i = 0
        while i < len(results):
            if results[i][2] == 0:
                results = np.delete(results,i,axis=0)
            i+=1
    return results[:,[0,1,2]] , results[:,[3]]

if __name__ == '__main__':
    #Seul code a comprendre, is okay
    with open('./Data/Plaque1/Model/Plaque_1.stp') as f:
        file = f.readlines()

    [points_3D,diameters] = getAllCircles(file, getBothFaces=False) #getBothFaces si vous voulez aussi les points qui correspondent au dessous de la plaque, probablement useless mais sait-on jamais
    #ONLY USE POINTS3D, DIAMETERS DONT WORK WOOPSIE


    print "positions : ", points_3D.shape
    print points_3D

    print "diametres : ", diameters.shape
    print diameters

