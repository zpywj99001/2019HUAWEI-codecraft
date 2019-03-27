import logging
import sys
from _FindShortPath import _Cross, _Road, _Channel, _Path, _Map, _FindShortPath
from _Car import _Car
#-----------test-----------
#cap = 10000
#minCapRoadId = 0
factor = 0.088
#-----------test-----------
# =============================================================================
# logging.basicConfig(level=logging.DEBUG,
#                     filename='../logs/CodeCraft-2019.log',
#                     format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S',
#                     filemode='a')
# =============================================================================

def ReadCartxt(filePath,file):                                                  
    fileDict = {file+'Id': file+'_attr_list'}
    fileIdOrder = []
    with open(filePath, "r") as f:
        lines = f.readlines()[1:]
    for line in lines:
        line = line.strip('( )\n')
        line = line.split(',')
        for i in range(len(line)):
            line[i] = int(line[i])
        newCar = _Car(line[0], line[1], line[2], line[3], line[4])
        fileDict[newCar.ID] = newCar
        fileIdOrder.append(line[0])
        fileIdOrder.sort()
    return fileDict, fileIdOrder

def ReadCrosstxt(filePath, file):                                                # 读取路口信息
    fileDict = {file+'Id': file+'_attr_list'}
    fileIdOrder = []
    with open(filePath, "r") as f:
        lines = f.readlines()[1:]
    for line in lines:
        line = line.strip('( )\n')
        line = line.split(',')
        for i in range(len(line)):
            line[i] = int(line[i])
        newCross = _Cross()
        newCross.ID = line[0]
        newCross.roadList.extend(line[1:])
        fileDict[newCross.ID] = newCross
        fileIdOrder.append(line[0])
        fileIdOrder.sort()
    return fileDict, fileIdOrder

def ReadRoadtxt(filePath, file):                                                 # 读取道路信息
    fileDict = {file+'Id': file+'_attr_list'}
    fileIdOrder = []
    with open(filePath, "r") as f:
        lines = f.readlines()[1:]
    for line in lines:
        line = line.strip('( )\n')
        line = line.split(',')
        for i in range(len(line)):
            line[i] = int(line[i])
        newRoad = _Road()
        newRoad.ID = line[0]
        newRoad.length = line[1]
        newRoad.limitSpeed = line[2]
        newRoad.channelNum = line[3]
        newRoad.startID = line[4]
        newRoad.endID = line[5]
        newRoad.isTwoWay = line[6]
        newRoad.channelList = list(range(1, newRoad.channelNum+1))
        fileDict[newRoad.ID] = newRoad
        fileIdOrder.append(line[0])
        fileIdOrder.sort()
        #----------------for test----------------------
# =============================================================================
#         tempcap = line[1]*line[2]*line[3]
#         global cap
#         global minCapRoadId
#         if cap > tempcap:
#             minCapRoadId = line[0]
#             cap = tempcap
# =============================================================================
        #-------------------------------test-----------
    return fileDict, fileIdOrder

def SaveAnswerToTxt(filePath, carIdOrder, optPath, carDict):  
    global factor
    answerLine = []
    answerLine.append("#(carId, StartTime, RoadIdList)")
                      
# ===========test==================================================================
    #carDict.pop("carId")
    #carStarttimeOrder = sorted(carDict.values,key=lambda x:x.startTime)
# ===========test==================================================================
    
    for carId in carIdOrder:
        optPathStr = ", ".join(str(i) for i in optPath[carId])
        Time = carDict[carId].startTime + int(len(answerLine)*factor)
        optPathStr = "(" + str(carId)+", " + str(Time) + ", " + optPathStr + ")"
        answerLine.append(optPathStr)
    answerTxt = "\n".join(answerLine)
    with open(filePath, "w") as f:
        f.write(answerTxt)
        print("Save answer.txt successfully!\n")

def RelativeRoad(startCross, endCross):
    for road in startCross.roadList:
        if road != -1 and (road.endID == endCross.ID or road.startID == endCross.ID):
            nowRoad = road
            return nowRoad.ID

def main():
    if len(sys.argv) != 5:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

# =============================================================================
#     logging.info("car_path is %s" % (car_path))
#     logging.info("road_path is %s" % (road_path))
#     logging.info("cross_path is %s" % (cross_path))
#     logging.info("answer_path is %s" % (answer_path))
# =============================================================================
    
    crossDict, crossIdOrder = ReadCrosstxt(cross_path, "cross")
    roadDict, roadIdOrder = ReadRoadtxt(road_path, "road")
    carDict, carIdOrder = ReadCartxt(car_path, "car")

    for roadID in roadIdOrder:                                                     # 将各道路的车道列表内元素配置为_Channel类
        nowRoad = roadDict[roadID]
        for channel in range(nowRoad.channelNum):
            newChannel = _Channel()
            newChannel.ID = nowRoad.channelList[channel]
            newChannel.remainCapacity = nowRoad.length
            nowRoad.channelList[channel] = newChannel
    
    
    for crossID in crossIdOrder:                                                   # 将各道路属性配置到对应路口的道路列表中
        nowCross = crossDict[crossID]
        for road in range(len(nowCross.roadList)):
            nowRoadId = nowCross.roadList[road]
            if nowRoadId != -1:
                nowCross.roadList[road] = roadDict[nowRoadId]
        
    thisMap = _Map()
    
    for ID in crossIdOrder:
        thisMap.getCross(crossDict[ID])
    
    for ID in roadIdOrder:
        thisMap.getRoad(roadDict[ID])
    
    optPathCross = dict()                    # 存放各车辆最短路径经过的路口字典
    
    optPathRoad = dict()                   # 存放各车辆最短路径经过的道路字典
    
    for car in carIdOrder:
        
        nowCar = carDict[car]
        nowOptPath = _FindShortPath()
        nowOptPath.InitEachPath(thisMap, nowCar.start)
        print('\n')
        print('carID:',car)
        print('nowCar.start:', nowCar.start, 'nowCar.end:', nowCar.end)
        nowOptPath.FindShortPath(thisMap)
        nowOptPath = nowOptPath.pathDic[nowCar.end].pathCrossList
        nowOptPath.append(nowCar.end)
        optPathCross[car] = nowOptPath
        carDict[car].path.extend(nowOptPath)
        nowOptRoad = []
        print('nowOptPath', nowOptPath)
        for cross in range(len(nowOptPath) - 1):
            nowCross = nowOptPath[cross]
            nextCross = nowOptPath[cross + 1]
            startCross = crossDict[nowCross]
            endCross = crossDict[nextCross]
    #        print('startCross:', startCross.ID, 'endCross', endCross.ID)
            pathRoad = RelativeRoad(startCross, endCross)
            nowOptRoad.append(pathRoad)
        print('nowOptRoad', nowOptRoad)
        optPathRoad[car] = nowOptRoad
            
    SaveAnswerToTxt(answer_path, carIdOrder, optPathRoad, carDict)
# to read input file
# process
# to write output file


if __name__ == "__main__":
    main()
    
    
