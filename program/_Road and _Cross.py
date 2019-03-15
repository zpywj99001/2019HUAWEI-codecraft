# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 17:38:11 2019

@author: V.J.
"""

class _Road(object):                           # 配置道路属性
    def __init__(self, roadID, length, limitSpeed, channelNum, startID, endID, isTwoWay):
        self.roadID = roadID                   # 道路ID
        self.length = length                   # 道路长度
        self.limitSpeed = limitSpeed           # 最高速度
        self.channelNum = channelNum           # 车道数目
        self.startID = startID                 # 起始点id
        self.endID = endID                     # 终点id
        self.isTwoWay = isTwoWay               # 是否双向  双向(1)/单向(0)
        

class _Cross(object):                          # 配置路口属性
    def __init__(self, crossID, road1ID, road2ID, road3ID, road4ID):
        self.crossID = crossID                 # 节点id
        self.road1ID = road1ID                 # 道路1id     (-1表示该道路不存在)
        self.road2ID = road2ID                 # 道路2id
        self.road3ID = road3ID                 # 道路3id
        self.road4ID = road4ID                 # 道路4id
        
