# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 19:18:41 2019

@author: V.J.
"""
import sys

class _Road(object):                         # 配置道路属性
    def __init__(self):
        self.ID = None                       # 道路ID
        self.length = None                   # 道路长度
        self.limitSpeed = None               # 最高速度
        self.channelNum = None               # 车道数目
        self.startID = None                  # 起始点id
        self.endID = None                    # 终点id
        self.isTwoWay = None                 # 是否双向  双向(1)/单向(0)
        self.channelListF = []               # 道路的正向车道列表(startID -> endID)
        self.channelListB = []               # 道路的反向车道列表(endID -> startID)
        
        
class _Channel(object):                      # 配置各车道属性
    def __init__(self):
        self.ID = None                       # 车道ID
        self.carList = []                    # 车道内车辆列表
        self.remainCapacity = None           # 车道剩余容量
        

class _Cross(object):                        # 配置路口属性
    def __init__(self):
        self.ID = None                       # 节点id
        self.roadList = []                   # 与该路口相接的道路id     (-1表示该道路不存在)
    

class _Map(object):                                # 配置地图属性和方法
    def __init__(self):
        self.crossList = []                        # 路口列表
        self.roadList = []                         # 道路列表
        
    def getCross(self, cross):                     # 添加路口列表
        self.crossList.append(cross)
        
    def getRoad(self, road):                       # 添加道路列表
        self.roadList.append(road)


class _Path(object):                               # 配置路径属性
    def __init__(self):
        self.currentCrossID = None                 
        self.isProcessed = False                   # 运行处理标志位
        self.length = sys.maxsize                  # 将初始权值(路长)设为最大值
        self.channelNum = 0.0000001            # 初始车道容量设为最小值
        self.pathCrossList = []                    # 存放经过的路口ID列表
        self.limitSpeed = 0.000001                 # 车道限速
        
        
class _FindShortPath(object):     # 寻找最优路径类                
    def __init__(self):
        self.pathDic = {}                          # 路径_Path类字典 {path.currentCrossID:path}
        
    def InitEachPath(self, map1, startCrossID):    # 初始化当前起始点路口至各路口的状态（路径, 路长）
        originCross = _Cross()           
        
        for cross in map1.crossList:
            if cross.ID == startCrossID:
                originCross.ID = cross.ID
                originCross.roadList.extend(cross.roadList)
            else:
                path = _Path()
                path.currentCrossID = cross.ID
                self.pathDic[path.currentCrossID] = path           
        
        for road in originCross.roadList:          # 和起始路口直接相连的路口，则修改相应路长，并记录下路径
            if road != -1:
                path = _Path()
                if road.endID == startCrossID and 0 == road.isTwoWay:   # 判断当前道路方向是否可以通行
                    continue
                elif road.endID == startCrossID and 1 == road.isTwoWay:
                    road.endID, road.startID = road.startID, road.endID 
                path.currentCrossID = road.endID
                path.length = road.length
                path.channelNum = road.channelNum            
                path.limitSpeed = road.limitSpeed
                path.pathCrossList.append(road.startID)
                self.pathDic[path.currentCrossID] = path
            
    def FindNextCross(self, map1, carSpeed):                 # 找出下一个最近的路口
        nextCross = _Cross()
        tmpDic = {}
        for k,v in self.pathDic.items():                   # 找出未处理的路口
            if not v.isProcessed:
                tmpDic[k] = v
        
        tempMin = sys.maxsize                      # 找出路径最短的路口并返回
        tmpK = None
        for k, v in tmpDic.items():
            nowSpeed = min(v.limitSpeed, carSpeed)
            weight = v.length/nowSpeed/v.channelNum
            if weight < tempMin:
                tempMin = weight
                tmpK = k
                tmpV = v               
        if tmpK:
            for cross in map1.crossList:
                if tmpV.currentCrossID == cross.ID:
                    nextCross = cross
        return nextCross
            
    def FindShortPath(self, map1, carSpeed):                 # 找出起始点至终点的最短路径
        nextCross = self.FindNextCross(map1, carSpeed)
#        print('nextCross.ID:',nextCross.ID)
        while nextCross.ID:                                      # 若该路口能使路径长度变小，则将该路口存进路口ID列表，直到所有路口都处理完毕
            currentPath = self.pathDic[nextCross.ID]
            
            for road in nextCross.roadList:
                if road != -1:
                    if road.endID == nextCross.ID and 0 == road.isTwoWay:    # 判断当前道路方向是否可以通行
                        continue
                    elif road.endID == nextCross.ID and 1 == road.isTwoWay:
                        road.endID, road.startID = road.startID, road.endID
                    if road.endID in currentPath.pathCrossList:
                        continue
                    targetPath = self.pathDic[road.endID]
                    tempLength = currentPath.length + road.length
#                    print('targetPath.length:', targetPath.length)
#                    print('tempLength:', tempLength)
                    if tempLength < targetPath.length:
                        targetPath.length = tempLength
                        targetPath.pathCrossList = []
                        
                        for i in range(len(currentPath.pathCrossList)):
                            targetPath.pathCrossList.append(currentPath.pathCrossList[i])
                        
                        targetPath.pathCrossList.append(nextCross.ID)
                    
            self.pathDic[nextCross.ID].isProcessed = True    # 标记为已处理          
            nextCross = self.FindNextCross(map1, carSpeed)          # 继续寻找下一个路口
#            print('nextCross.ID:',nextCross.ID)
                
        

        
