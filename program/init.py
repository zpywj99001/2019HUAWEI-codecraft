# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 19:37:50 2019

@author: V.J.
"""

from _FindShortPath import _Cross, _Road, _Channel, _Path, _Map, _FindShortPath
from _Car import _Car
from _Traffic import _Traffic
from CarSorted import CarSorted

def ReadCartxt(folder, file):                                                  # 读取车辆信息
    fileDict = {file+'Id': file+'_attr_list'}
    fileIdOrder = []
    with open(folder+"/"+file+".txt", "r") as f:
	        lines = f.readlines()[1:]
#    txt = open(folder+"\\"+file+".txt", "r")
#    lines = txt.readlines()[1:]
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
    with open(folder+"/"+file+".txt", "r") as f:
	        lines = f.readlines()[1:]
#    txt = open(folder+"\\"+file+".txt", "r")
#    lines = txt.readlines()[1:]
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
    with open(folder+"/"+file+".txt", "r") as f:
        lines = f.readlines()[1:]
#    txt = open(folder+"\\"+file+".txt", "r")
#    lines = txt.readlines()[1:]
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
        newRoad.channelListF = list(range(1, newRoad.channelNum + 1))
        if newRoad.isTwoWay == 1:
            newRoad.channelListB = list(range(1, newRoad.channelNum + 1))
        fileDict[newRoad.ID] = newRoad
        fileIdOrder.append(line[0])
        fileIdOrder.sort()
    return fileDict, fileIdOrder

def SaveAnswerToTxt(filePath, carIdOrder, optPath):  
    answerLine = []
    answerLine.append("#(carId, StartTime, RoadIdList)")
    for carId in carIdOrder:
        optPathStr = ", ".join(str(i) for i in optPath[carId])
        optPathStr = "(" + str(carId)+", " + str(carDict[carId].startTime) + "," + optPathStr + ")"
        answerLine.append(optPathStr)
    answerTxt = "\n".join(answerLine)
    with open(filePath, "w") as f:
        f.write(answerTxt)
        print("Save answer.txt successfully!\n")

def RelativeRoad(startCross, endCross):
    for road in startCross.roadList:
        if road != -1 and (road.endID == endCross.ID or road.startID == endCross.ID):
            nowRoad = road
            return nowRoad.ID
        
# =============================================================================

fileDir = r"G:\VJ\华为软挑\2019华为软件精英挑战赛\2019软挑-初赛-SDK\SDK_python\CodeCraft-2019\config"

crossDict, crossIdOrder = ReadCrosstxt(fileDir, "cross")
roadDict, roadIdOrder = ReadRoadtxt(fileDir, "road")
carDict, carIdOrder = ReadCartxt(fileDir, "car")


for roadID in roadIdOrder:                                                     # 将各道路的车道列表内元素配置为_Channel类
    nowRoad = roadDict[roadID]
    for channel in range(nowRoad.channelNum):
        newChannelF = _Channel()
        newChannelF.ID = nowRoad.channelListF[channel]
        newChannelF.remainCapacity = nowRoad.length
        nowRoad.channelListF[channel] = newChannelF
        if nowRoad.isTwoWay == 1:
            newChannelB = _Channel()
            newChannelB.ID = nowRoad.channelListB[channel]
            newChannelB.remainCapacity = nowRoad.length
            nowRoad.channelListB[channel] = newChannelB
            
        


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

optPathCross = dict()                    # 存放各车辆最短路径经过的路口字典

optPathRoad = dict()                   # 存放各车辆最短路径经过的道路字典

for car in carIdOrder:
    
    nowCar = carDict[car]
    nowOptPath = _FindShortPath()
    nowOptPath.InitEachPath(thisMap, nowCar.start)
#    print('\n')
#    print('carID:',car)
#    print('nowCar.start:', nowCar.start, 'nowCar.end:', nowCar.end)
    nowOptPath.FindShortPath(thisMap, nowCar.maxSpeed)
    nowOptPath = nowOptPath.pathDic[nowCar.end].pathCrossList
    nowOptPath.append(nowCar.end)
    optPathCross[car] = nowOptPath
    carDict[car].path.extend(nowOptPath)
    nowOptRoad = []
#    print('nowOptPath', nowOptPath)
    for cross in range(len(nowOptPath) - 1):
        nowCross = nowOptPath[cross]
        nextCross = nowOptPath[cross + 1]
        startCross = crossDict[nowCross]
        endCross = crossDict[nextCross]
#        print('startCross:', startCross.ID, 'endCross', endCross.ID)
        pathRoad = RelativeRoad(startCross, endCross)
        nowOptRoad.append(pathRoad)
#    print('nowOptRoad', nowOptRoad)
    optPathRoad[car] = nowOptRoad
        
SaveAnswerToTxt(fileDir + '/answer.txt', carIdOrder, optPathRoad)

sortedCar = CarSorted(fileDir + '/answer.txt')

console = _Traffic()
lockedCar = console.CrossControl(crossIdOrder, crossDict, sortedCar, carDict, roadIdOrder, roadDict)
    
    


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

