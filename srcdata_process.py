# -*- coding: utf-8 -*-

# =================read data from txt===============
def Readtxt(folder, file):
    fileDict = {file+'Id': file+'_attr_list'}
    fileIdOrder = []
    txt = open(folder+"\\"+file+".txt", "r")
    lines = txt.readlines()[1:]
    for line in lines:
        line = line.strip('( )\n')
        line = line.split(',')
        for i in range(len(line)):
            line[i] = int(line[i])
        fileDict[line[0]] = line[1:]
        fileIdOrder.append(line[0])
        fileIdOrder.sort()
    return fileDict, fileIdOrder

# ====================for test======================
if __name__ == "__main__":
    crossDict, crossIdOrder = Readtxt("config", "cross")
    roadDict, roadIdOrder = Readtxt("config", "road")
    carDict, carIdOrder = Readtxt("config", "car")

    for Id in crossIdOrder:
        print(Id)
    for Id in crossIdOrder:
        print(crossDict[Id])
    for Id in roadIdOrder:
        print(Id)
    for Id in roadIdOrder:
        print(roadDict[Id])
    for Id in carIdOrder:
        print(Id)
    for Id in carIdOrder:
        print(carDict[Id])