# -*- coding: utf-8 -*-
import srcdata_processs as dp

cross_dict, crossId_order = dp.readtxt("config","cross")
road_dict, roadId_order = dp.readtxt("config","road")
car_dict, carId_order = dp.readtxt("config","car")

for Id in crossId_order:
    print(Id)
for Id in crossId_order:
    print(cross_dict[Id])
for Id in roadId_order:
    print(Id)
for Id in roadId_order:
    print(road_dict[Id])
for Id in carId_order:
    print(Id)
for Id in carId_order:
    print(car_dict[Id])