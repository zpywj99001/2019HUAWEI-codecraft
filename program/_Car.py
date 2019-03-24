# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 15:49:41 2019

@author: V.J.
"""
def RelativeRoad(startCross, endCross):                # 获取当前道路ID
    for road in startCross.roadList:
        if road != -1 and (road.endID == endCross.ID or road.startID == endCross.ID):
            nowRoad = road
            return nowRoad.ID


class _Car(object):                                      #配置车辆属性和方法
    def __init__(self, ID, start, end, maxSpeed, startTime):
        self.ID = ID                             # 车辆ID
        self.start = start                       # 起始点
        self.end = end                           # 终点
        self.maxSpeed = maxSpeed                 # 最高车速
        self.currentSpeed = 0         # 当前车速
        self.startTime = startTime               # 出发时间
        self.isCross = 0                         # 判断车辆是否能过路口, (0):不能过  (1):能过
        self.nowPosition = 0                    # 当前道路行驶距离(距离出发端)
        self.state = 1                           # 车辆状态: 终止(1)/等待(0) 
        self.direction = None                    # 车辆行驶方向， 若车辆未出发则为None。  左转: 'L'   直走: 'S'      右转: 'R'
        self.path = []                           # 车辆行驶的路径列表
        self.hasGone = 0                         # 车辆已经行驶的距离
        self.nowChannel = None                   # 车辆所在车道
        

    def Run(self, roadDict):               # 经过一次行驶时间，更新车辆状态
#        while 0 == self.state:
        block = True                            # 标志前方是否有阻挡车辆
        nowRoad = RelativeRoad(self.path[0], self.path[1])         # 获取当前道路的ID
        nowRoad = roadDict[nowRoad] 
  
        if self.maxSpeed > nowRoad.limitSpeed:               # 判断车辆当前行驶速度
                    self.currentSpeed = nowRoad.limitSpeed
        else:
            self.currentSpeed = self.maxSpeed              
        needToGo = self.currentSpeed - self.hasGone         # 车辆在下条道路的行驶距离
#        if needToGo < 0:
#            needToGo = 0
        
        channel = nowRoad.channelList[self.nowChannel - 1]          # 车辆当前行驶的车道
        nowOrder = channel.carList.index(self.ID)                   # 车辆在车道中的位置
        if nowOrder != 0:                                           # 若车辆不处于该车道最前面，则判断与前车的位置关系
            frontCar = channel.carList[nowOrder-1]           
            if self.nowPosition + needToGo < frontCar.nowPosition:  # 若所需行驶距离小于前车位置即可以正常行驶，否则会被前车阻挡
                block = False
#            else:
#                if 0 == frontCar.state:                           # 若有车阻挡且前车为等待状态，则本车也为等待状态，等待前车先行
#                    self.state = 0
        elif 0 == nowOrder:                                       # 当车辆位于车道首位则判断是否出路口
            if self.nowPosition + needToGo > nowRoad.length:
                self.isCross = 1
                self.state = 0
                self.hasGone = nowRoad.length - self.nowPosition
            else:
                self.isCross = 0
            block = False
            
        if block and 0 == frontCar.state:                              # 若车辆过路口，或有车阻挡且前车为等待状态，则本车也为等待状态
            self.state = 0
#            break
        
        elif 0 == self.isCross and (not block or 1 == frontCar.state): # 若车辆不过路口且无前车或前车为终止状态，则行驶至下一位置 
            if block:
                self.nowPosition += min(needToGo, frontCar.nowPosition - 1)    # 行驶到达下一个位置
            else:
                self.nowPosition += needToGo
            self.state = 1
            self.hasGone = 0
#            self.isCross = 0
            if nowOrder + 1 == len(channel.carList):                    # 根据该车道排在末尾的一辆车计算车道剩余容量
                channel.remainCapacity = self.nowPosition - 1
                
        elif 1 == self.isCross:
            nextRoad = RelativeRoad(self.path[1], self.path[2])
            nextRoad = roadDict[nextRoad]
            if self.maxSpeed > nextRoad.limitSpeed:               # 判断车辆当前行驶速度
                self.currentSpeed = nextRoad.limitSpeed
            else:
                self.currentSpeed = self.maxSpeed              
            needToGo = self.currentSpeed - self.hasGone         # 车辆在下条道路的行驶距离
            if needToGo <= 0:                                   # 若车辆在下条道路行驶距离为零以下，则在当前道路终点处且为终止状态
#                needToGo = 0
                self.state = 1
                self.hasGone = 0
                self.isCross = 0
                self.nowPosition = nowRoad.length
                if nowOrder + 1 == len(channel.carList):
                    channel.remainCapacity = self.nowPosition - 1
             
#                if needToGo > 0:                                # 判断道路能否进入下条道路行驶
#                    for cl in nextRoad.channelList:             # 若下条道路有位置，则车辆从路口进入下一条道路，否则继续等待
#                        if cl.remainCapacity > 0:
#                            frontCar = cl.carList[-1]
#                            if 1 == frontCar.state:
#                                cl.carList.append(self.ID)
#                                self.path.pop(0)
#                                channel.carList.pop(0)
#                                self.nowChannel = cl.ID
#                                self.nowPosition = 0
#                                self.isCross = 0
#                            break
                
