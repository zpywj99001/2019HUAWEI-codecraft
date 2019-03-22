# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 19:37:50 2019

@author: V.J.
"""

from _FindShortPath import _Cross, _Road, _Channel, _Path, _Map, _FindShortPath
from _Car import _Car


def ReadCartxt(folder, file):                                                  # 读取车辆信息
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

def ReadCrosstxt(folder, file):                                                # 读取路口信息
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

def ReadRoadtxt(folder, file):                                                 # 读取道路信息
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
        newRoad.channelList = list(range(1,newRoad.channelNum+1))
        fileDict[newRoad.ID] = newRoad
        fileIdOrder.append(line[0])
        fileIdOrder.sort()
    return fileDict, fileIdOrder

fileDir = r"G:\VJ\华为软挑\2019华为软件精英挑战赛\2019软挑-初赛-SDK\SDK_python\CodeCraft-2019\config"

crossDict, crossIdOrder = ReadCrosstxt(fileDir, "cross")
roadDict, roadIdOrder = ReadRoadtxt(fileDir, "road")
carDict, carIdOrder = ReadCartxt(fileDir, "car")


for roadID in roadIdOrder:                                                     # 将各道路的车道列表内元素配置为_Channel类
    nowRoad = roadDict[roadID]
    for channel in range(nowRoad.channelNum):
        newChannel = _Channel()
        newChannel.ID = nowRoad.channelList[channel]
        newChannel.remainCapacity = nowRoad.length
        nowRoad.channelList[channel] = newChannel


for crossID in crossIdOrder:                                                   # 将各道路属性配置到对应路口的道路列表中
    nowCross = crossDict[crossID]
    for road in range(len(nowCross.roadList)):
        nowRoadId = nowCross.roadList[road]
        if nowRoadId != -1:
            nowCross.roadList[road] = roadDict[nowRoadId]
        



thisMap = _Map()

for ID in crossIdOrder:
    thisMap.getCross(crossDict[ID])

for ID in roadIdOrder:
    thisMap.getRoad(roadDict[ID])

optPath = dict()
for car in carIdOrder:
    nowCar = carDict[car]
    nowOptPath = _FindShortPath()
    nowOptPath.InitEachPath(thisMap, nowCar.start)
    print('carID:',car)
    print('nowCar.start:', nowCar.start)
    nowOptPath.FindShortPath(thisMap)
    optPath[car] = nowOptPath.pathDic[nowCar.end]




    
    


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

