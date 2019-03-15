# -*- coding: utf-8 -*-

# =================read data from txt===============
def readtxt(folder,file):
    file_dict = {file+'Id': file+'_attr_list'}
    fileId_order = []
    txt = open(folder+"\\"+file+".txt","r")
    lines = txt.readlines()[1:]
    for line in lines:
        line = line.strip('( )\n')
        line = line.split(',')
        for i in range(len(line)):
            line[i] = int(line[i])
        file_dict[line[0]] = line[1:]
        fileId_order.append(line[0])
        fileId_order.sort()
    return file_dict, fileId_order

# ====================for test======================
if __name__ == "__main__":
    cross_dict, crossId_order = readtxt("config","cross")
    road_dict, roadId_order = readtxt("config","road")
    car_dict, carId_order = readtxt("config","car")
    
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