while True:
	set_state_car_number=0	
	road_list = []	#所有道路的列表 list of all roads
	road_car = []	#道路上汽车的分布distribution of cars on roads
	while set_state_car_number<current_car_number:
		for road in road_list:
			for road in road_car[road].forward:
				pass