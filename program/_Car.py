# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 15:49:41 2019

@author: V.J.
"""
class _Car(object):                                      #配置车辆属性和方法
    def __init__(self, ID, start, end, maxSpeed, startTime):
        self.ID = ID                             # 车辆ID
        self.start = start                       # 起始点
        self.end = end                           # 终点
        self.maxSpeed = maxSpeed                 # 最高车速
        self.currentSpeed = currentSpeed         # 当前车速
        self.startTime = startTime               # 出发时间
        self.isCross = 0                         # 判断车辆是否能过路口, (0):不能过  (1):能过
        self.roadDistance = 0                    # 当前道路行驶距离(距离出发端)
        self.state = 1                           # 车辆状态: 终止(1)/等待(0) 
        self.direction = None                    # 车辆行驶方向， 若车辆未出发则为None。  左转: 'L'   直走: 'S'      右转: 'R'
        self.path = []                           # 车辆行驶的路径列表
        
        

    def Run(self, currentSpeed, thisCar, frontCar, nextRoad):               # 经过一次行驶时间，更新车辆状态
        
        if car is blocked:                                            # 判断车辆是否被阻挡：1）行驶后可出路口
                                                                      #                   2）行驶后仍在车道内
            if 0 == frontCar.state:
                thisCar.state = 0
            else:
                car achieve the farest position
                thisCar.state = 1
        
        else:
            car run to the next position
            
            car.state = 1
            
            update the start position
            
