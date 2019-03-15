# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 15:49:41 2019

@author: V.J.
"""
class _Car:                                      #配置车辆属性和方法
    def __init__(self, ID, start, end, maxSpeed, currentSpeed, startTime, state):
        self.ID = ID                             # 车辆ID
        self.start = start                       # 起始点
        self.end = end                           # 终点
        self.maxSpeed = maxSpeed                 # 最高车速
        self.currentSpeed = currentSpeed         # 当前车速
        self.startTime = startTime               # 出发时间
        self.nextRoad = None                     # 行驶的下一条道路
        self.roadDistance = 0                    # 当前道路行驶距离(距离出发端)
        self.state = 1                           # 车辆状态: 终止(1)/等待(0) 
        
        

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
            
