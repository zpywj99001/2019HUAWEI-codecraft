# -*- coding: utf-8 -*-
import srcdata_process as dp

crossDict, crossIdOrder = dp.Readtxt("1-map-training-1", "cross")
roadDict, roadIdOrder = dp.Readtxt("1-map-training-1", "road")
carDict, carIdOrder = dp.Readtxt("1-map-training-1", "car")

for Id in crossIdOrder:
    print(Id)
for Id in crossIdOrder:
    print(crossDict[Id])
for Id in roadIdOrder:
    print(Id)
for Id in roadIdOrder:
    print(roadDict[Id])
for Id in carIdOrder:
    print(Id)
for Id in carIdOrder:
    print(carDict[Id])