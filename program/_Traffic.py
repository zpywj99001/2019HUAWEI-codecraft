# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 09:25:19 2019

@author: V.J.
"""
class _Traffic(object):
    def __init__(self):
        self.isJam = 0                        # 当前时刻是否存在卡死 (1):存在   (0):不存在
        
    def CrossControl(self, road, map1):                                     # 路口调度                                                 
        for cross.ID from small to big:                                     # 路口从小到大遍历
            while there is car.state == 0 on road:                          # 若道路存在等待状态车辆则实行调度
                nowRoad = road.ID from small to big                         # 道路ID从小到大遍历
                nowChannel = ID of nowRoad.channelList from small to big    # 车道从小到大遍历
                nowCar = nowChannel.carList.pop(0)                          # 车辆以车辆队列顺序遍历
                if nowCar.state == 1:                                       # 若车辆状态终止则进行下一轮调度
                    continue
                elif 0 == nowCar.isCross and (1 == frontCar.state or no frontCar):    # 若车辆不过路口且无前方车辆或
                                                                                      # 前方车辆为终止状态则行驶至下一位置后更新车辆信息
                    nowCar run to the next position
                    update nowCar state
                    continue
                elif 0 == nowCar.isCross and 0 == frontCar.state:   # 若车辆不过路口且前方车辆为等待状态则进行下一轮调度              
                    continue
                elif 1 == nowCar.isCross and nowCar priority is highest now:    # 若车辆过路口且处于当前最高优先级则行驶至下一位置后更新车辆与车道信息
                    update nowCar state                           # (注：这里可能出现两种情况：1.车辆由于前方车辆阻挡无法过路口；
                    update nowChannel state                                   # 2.车辆可以过路口，但需要根据前方道路情况(有无前方车辆)确定下一时刻位置)
                    
                elif 1 == frontCar.state and nowCar priority is highest now:    # 若车辆过路口但不处于当前最高优先级则进行下一轮调度
                    nowCar run to the next position
                    update nowCar state
                else:
                    continue
                        
    def JudgeJam(self):                     # 判断当前交通情况是否存在卡死
        if there is traffic jam:
            self.isJam = 1
        else:
            self.isJam = 0
                    
                    
                    