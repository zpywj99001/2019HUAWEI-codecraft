# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 19:37:50 2019

@author: V.J.
"""
from _FindShortPath import _Cross, _Road
from _Car import _Car


def ReadCartxt(folder, file):
    fileDict = {file+'Id': file+'_attr_list'}
    fileIdOrder = []
    txt = open(folder+"\\"+file+".txt", "r")
    lines = txt.readlines()[1:]
    for line in lines:
        line = line.strip('( )\n')
        line = line.split(',')
        for i in range(len(line)):
            line[i] = int(line[i])
        newCar = _Car(line[0], line[1], line[2], line[3], line[4])
        fileDict[newCar.ID] = newCar
        fileIdOrder.append(line[0])
        fileIdOrder.sort()
    return fileDict, fileIdOrder

def ReadCrosstxt(folder, file):
    fileDict = {file+'Id': file+'_attr_list'}
    fileIdOrder = []
    txt = open(folder+"\\"+file+".txt", "r")
    lines = txt.readlines()[1:]
    for line in lines:
        line = line.strip('( )\n')
        line = line.split(',')
        for i in range(len(line)):
            line[i] = int(line[i])
        newCross = _Cross()
        newCross.ID = line[0]
        newCross.roadList.extend(line[1:])
        fileDict[newCross.ID] = newCross
        fileIdOrder.append(line[0])
        fileIdOrder.sort()
    return fileDict, fileIdOrder

def ReadRoadtxt(folder, file):
    fileDict = {file+'Id': file+'_attr_list'}
    fileIdOrder = []
    txt = open(folder+"\\"+file+".txt", "r")
    lines = txt.readlines()[1:]
    for line in lines:
        line = line.strip('( )\n')
        line = line.split(',')
        for i in range(len(line)):
            line[i] = int(line[i])
        newRoad = _Road()
        newRoad.ID = line[0]
        newRoad.length = line[1]
        newRoad.limitSpeed = line[2]
        newRoad.channelNum = line[3]
        newRoad.startID = line[4]
        newRoad.endID = line[5]
        newRoad.isTwoWay = line[6]
        fileDict[newRoad.ID] = newRoad
        fileIdOrder.append(line[0])
        fileIdOrder.sort()
    return fileDict, fileIdOrder

fileDir = r"G:\VJ\华为软挑\2019华为软件精英挑战赛\2019软挑-初赛-SDK\SDK_python\CodeCraft-2019\config"

crossDict, crossIdOrder = ReadCrosstxt(fileDir, "cross")
roadDict, roadIdOrder = ReadRoadtxt(fileDir, "road")
carDict, carIdOrder = ReadCartxt(fileDir, "car")


# =============================================================================
# for ID in crossIdOrder:
#     print('crossID:', ID, 'corssData:', crossDict[ID])
#     
# print('\n')
# 
# for ID in roadIdOrder:
#     print('roadID:', ID, 'roadData:', roadDict[ID])
#     
# print('\n')
# 
# for ID in carIdOrder:
#     print('carID:', ID, 'carData:', carDict[ID])
# =============================================================================

