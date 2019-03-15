# -*- coding: utf-8 -*-
import srcdata_process as dp

carIdOrder, answer = dp.Readtxt("1-map-training-1", "answer")[0]
for Id in carIdOrder:
    print(answer[Id])
# while True:
# 	set_state_car_number=0
# 	road_list = []	#所有道路的列表 list of all roads
# 	road_car = []	#道路上汽车的分布distribution of cars on roads
# 	while set_state_car_number<current_car_number:
# 		for road in road_list:
# 			for road in road_car[road].forward:
# 				pass

# =============================================================================
# def driveCartoroad():
#     pass
# =============================================================================
