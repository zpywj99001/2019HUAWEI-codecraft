# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 09:25:19 2019

@author: V.J.
"""
from copy import deepcopy
#from init import RelativeRoad

def RelativeRoad(startCross, endCross):
    for road in startCross.roadList:
        if road != -1 and (road.endID == endCross.ID or road.startID == endCross.ID):
            nowRoad = road
            return nowRoad.ID

class _Traffic(object):
    def __init__(self):
        self.isJam = 0                        # 当前时刻是否存在卡死 (1):存在   (0):不存在
    
    def OnRoad(self, car, roadDict, crossDict, carDict):
        startCross = crossDict[car.path[0]]
        endCross = crossDict[car.path[1]]
        nextRoad = RelativeRoad(startCross, endCross)              # 过路口后行驶的道路
        nextRoad = roadDict[nextRoad]
        
        if car.path[0] == nextRoad.endID:     # 判断车辆行驶的车道方向（正向OR反向）
            for cl in nextRoad.channelListB:             # 若下条道路有位置且前车为终止状态，则车辆从路口进入下一条道路，否则继续等待 
                if cl.remainCapacity > 0:
                    if cl.carList:
                        frontCar = cl.carList[-1]
                        frontCar = carDict[frontCar]
                        if 1 == frontCar.state:
                            cl.carList.append(car.ID)
                            car.nowChannel = cl.ID
                            car.nowPosition = 0
                            car.isCross = 0
                            return True
                    elif not cl.carList:                     # 无前车
                        cl.carList.append(car.ID)
                        car.nowChannel = cl.ID
                        car.nowPosition = 0
                        car.isCross = 0
                        return True
                    
        elif car.path[0] == nextRoad.startID:
            for cl in nextRoad.channelListF:             # 若下条道路有位置，则车辆从路口进入下一条道路，否则继续等待 
                if cl.remainCapacity > 0:
                    if cl.carList:
                        frontCar = cl.carList[-1]
                        frontCar = carDict[frontCar]
                        if 1 == frontCar.state:
                            cl.carList.append(car.ID)
                            car.nowChannel = cl.ID
                            car.nowPosition = 0
                            car.isCross = 0
                            return True
                    elif not cl.carList:              # 无前车
                        cl.carList.append(car.ID)
                        car.nowChannel = cl.ID
                        car.nowPosition = 0
                        car.isCross = 0
                        return True
        return False
    
    def InitCar(self, roadIdOrder, roadDict, carDict):
        for road in roadIdOrder:
            nowRoad = roadDict[road]
            for channel in nowRoad.channelListF:
                for car in channel.carList:
                    car = carDict[car]
                    car.state = 0
#                    print('InitCar:', car.ID)
            if 1 == nowRoad.isTwoWay:
                for channel in nowRoad.channelListB:
                    for car in channel.carList:
                        car = carDict[car]
                        car.state = 0
#                        print('InitCar:', car.ID)
    def HaveCar(self, roadIdOrder, roadDict, carDict):
        countCar = 0
        for road in roadIdOrder:
            nowRoad = roadDict[road]
            for channel in nowRoad.channelListF:
                for car in channel.carList:
                    countCar += 1
#                    return True
            if 1 == nowRoad.isTwoWay:
                for channel in nowRoad.channelListB:
                    for car in channel.carList:
                        countCar += 1
#                        return True
        return countCar
    
    def CrossControl(self, crossIdOrder, crossDict, carIdOrder, carDict, roadIdOrder, roadDict):         # 路口调度
        cTime = 0
        waitCarTable = deepcopy(carDict)
        priDict = {}                                              # 记录每个路口当前选择的行驶道路
        beforeTable = []                                      # 记录之前各路口等待状态车辆的列表
        while waitCarTable or self.HaveCar(roadIdOrder, roadDict, carDict):
            if not beforeTable :                                  # 当前一个调度时间结束，则判断是否添加待上路的车辆
                cTime += 1
                print('Control Time:', cTime)
                startCross = []
                for car in carIdOrder:
                    if car in waitCarTable:
                        nowCar = carDict[car]
                        if nowCar.startTime <= cTime and nowCar.path[0] not in startCross and self.OnRoad(nowCar, roadDict, crossDict, carDict):
                            startCross.append(nowCar.path[0])
#                            print('onRoad car:', nowCar.ID)
                            del(waitCarTable[car])
                            continue
#                        else:
#                            break
                self.InitCar(roadIdOrder, roadDict, carDict)          # 初始化道路上各车状态为0
                
            for road in roadIdOrder:                                  # 遍历所有道路上的车进行行驶，最终分为等待状态与终止状态的车
                nowRoad = roadDict[road]
                for channel in nowRoad.channelListF:
                    for car in channel.carList:
                        car = carDict[car]
                        print('carID:', car.ID)
                        car.Run(roadDict, crossDict, carDict)
                        print('car.nowPosition', car.nowPosition)
                        if car.nowPosition > 10:
                            return
                if 1 == nowRoad.isTwoWay:
                    for channel in nowRoad.channelListB:
                        for car in channel.carList:
                            car = carDict[car]
                            print('carID:', car.ID)
                            car.Run(roadDict, crossDict, carDict)
                            print('car.nowPosition', car.nowPosition)
                            if car.nowPosition > 10:
                                return
            waitTable = []                                        # 记录当前各路口等待状态车辆的列表
            for cross in crossIdOrder:                            # 遍历各个路口进行第一优先级车辆的调度
                crossCar = []
                nowCross = crossDict[cross]
                for road in nowCross.roadList:
                    firstGoCar = []
                    if road == -1 or (road.startID == nowCross.ID and 0 == road.isTwoWay):
                        continue
                    elif road != -1 and 1 == road.isTwoWay and road.startID == nowCross.ID:
                        for channel in road.channelListB:
                            for car in channel.carList:
                                car = carDict[car]
                                if 1 == car.isCross and (road.ID, channel.ID, 0) not in firstGoCar:
                                    toEnd = road.length - car.hasGone
                                    firstGoCar.append([(road.ID, channel.ID, 0), car, toEnd])
                                    break
                    elif road != -1 and road.endID == nowCross.ID:
                        for channel in road.channelListF:
                            for car in channel.carList:
                                car = carDict[car]
                                if 1 == car.isCross and (road.ID, channel.ID, 1) not in firstGoCar:
                                    toEnd = road.length - car.hasGone
                                    firstGoCar.append([(road.ID, channel.ID, 1), car, toEnd])
                                    break
                    if firstGoCar:
                        firstGoCar = min(firstGoCar, key=lambda x: x[2])
                        crossCar.append(firstGoCar)
                if crossCar:
                    crossCar = sorted(crossCar, key=lambda x: x[0][0])
                    if nowCross.ID not in priDict:                       # 默认按照道路ID升序进行路口调度
                        for car in crossCar:
                            nowCar = car[1]
    #                        roadID = car[0][0]
    #                        channelID = car[0][1]
                            if nowCar.direction == 'S':                  # 若该车辆为直行，则直接通过
                                nowCar.NowCross(roadDict, crossDict, carDict)
                            elif nowCar.direction == 'L':                # 若该车辆为左转，则判断对应道路是否有直行车辆
                                indCar = crossCar.index(car)
                                ind2Car = (indCar - 1) % 3               # 直行车辆所在道路位置
                                if len(crossCar) > ind2Car:
                                    eCar = crossCar[ind2Car][1]
                                    if eCar.direction == 'S':
                                        continue
                                else:
                                    nowCar.NowCross(roadDict, crossDict, carDict)
                            elif nowCar.direction == 'R':                 # 若该车辆为右转，则判断对应道路是否有左转或直行车辆
                                indCar = crossCar.index(car)
                                ind2Car = (indCar + 1) % 4                # 直行车辆所在道路位置
                                ind3Car = (indCar + 2) % 4                # 左转车辆所在道路位置
                                if len(crossCar) > ind2Car:                        
                                    eCar = crossCar[ind2Car][1]
                                    if eCar.direction == 'S':
                                        continue
                                if len(crossCar) > ind3Car:
                                    eCar2 = crossCar[ind3Car][1]
                                    if eCar2.direction == 'L':
                                        continue
                                else:
                                    nowCar.NowCross(roadDict, crossDict, carDict)
                            if nowCar.state == 1:
                                nowInd = crossCar.index(car)
                                priDict[nowCross.ID] = nowInd
                                crossCar.pop(nowInd)
                                waitTable.extend(crossCar)
                                break
                        waitTable.extend(crossCar)
                        
                    elif nowCross.ID in priDict:
                        newCrossCar = list()
                        ind = priDict[nowCross.ID]
                        newCrossCar.extend(crossCar[ind:])
                        newCrossCar.extend(crossCar[:ind])
                        for car in newCrossCar:
                            nowCar = car[1]
    #                        roadID = car[0][0]
    #                        channelID = car[0][1]
                            if nowCar.direction == 'S':                  # 若该车辆为直行，则直接通过
                                nowCar.NowCross(roadDict, crossDict, carDict)
                            elif nowCar.direction == 'L':                # 若该车辆为左转，则判断对应道路是否有直行车辆
                                indCar = crossCar.index(car)
                                ind2Car = (indCar - 1) % 3               # 直行车辆所在道路位置
                                if len(crossCar) > ind2Car:
                                    eCar = crossCar[ind2Car][1]
                                    if eCar.direction == 'S':
                                        continue
                                else:
                                    nowCar.NowCross(roadDict, crossDict, carDict)
                            elif nowCar.direction == 'R':                 # 若该车辆为右转，则判断对应道路是否有左转或直行车辆
                                indCar = crossCar.index(car)
                                ind2Car = (indCar + 1) % 4                # 直行车辆所在道路位置
                                ind3Car = (indCar + 2) % 4                # 左转车辆所在道路位置
                                if len(crossCar) > ind2Car:                        
                                    eCar = crossCar[ind2Car][1]
                                    if eCar.direction == 'S':
                                        continue
                                if len(crossCar) > ind3Car:
                                    eCar2 = crossCar[ind3Car][1]
                                    if eCar2.direction == 'L':
                                        continue
                                else:
                                    nowCar.NowCross(roadDict, crossDict, carDict)
                            if nowCar.state == 1:
                                nowInd = crossCar.index(car)
                                priDict[nowCross.ID] = nowInd
                                crossCar.pop(nowInd)
                                waitTable.extend(crossCar)
                                break
                        waitTable.extend(crossCar)
            print('waitTable Size:', len(waitTable))
            print('beforeTable Size:', len(beforeTable))
            if self.JudgeJam(beforeTable, waitTable):
                return waitTable
                break
            
            
            beforeTable = waitTable
        print('Running success!')
                
            
        
        
#        for cross.ID from small to big:                                     # 路口从小到大遍历
#            while there is car.state == 0 on road:                          # 若道路存在等待状态车辆则实行调度
#                nowRoad = road.ID from small to big                         # 道路ID从小到大遍历
#                nowChannel = ID of nowRoad.channelList from small to big    # 车道从小到大遍历
#                nowCar = nowChannel.carList.pop(0)                          # 车辆以车辆队列顺序遍历
#                if nowCar.state == 1:                                       # 若车辆状态终止则进行下一轮调度
#                    continue
#                elif 0 == nowCar.isCross and (1 == frontCar.state or no frontCar):    # 若车辆不过路口且无前方车辆或
#                                                                                      # 前方车辆为终止状态则行驶至下一位置后更新车辆信息
#                    nowCar run to the next position
#                    update nowCar state
#                    continue
#                elif 0 == nowCar.isCross and 0 == frontCar.state:   # 若车辆不过路口且前方车辆为等待状态则进行下一轮调度              
#                    continue
#                elif 1 == nowCar.isCross and nowCar priority is highest now:    # 若车辆过路口且处于当前最高优先级则行驶至下一位置后更新车辆与车道信息
#                    update nowCar state                           # (注：这里可能出现两种情况：1.车辆由于前方车辆阻挡无法过路口；
#                    update nowChannel state                                   # 2.车辆可以过路口，但需要根据前方道路情况(有无前方车辆)确定下一时刻位置)
#                    
#                elif 1 == frontCar.state and nowCar priority is highest now:    # 若车辆过路口但不处于当前最高优先级则进行下一轮调度
#                    nowCar run to the next position
#                    update nowCar state
#                else:
#                    continue
                        
    def JudgeJam(self, beforeTable, waitTable):                     # 判断当前交通情况是否存在卡死
        if beforeTable and waitTable and beforeTable == waitTable:
            print("The road is locked!")
            return True
        else:
            return False
                    
                    
                    
