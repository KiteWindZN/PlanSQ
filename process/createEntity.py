# -*- coding:utf-8 -*-
from process import ReadJson
from entity import entity
import sys
import datetime
import matplotlib.pyplot as plt
import random
import matplotlib.patches as patches
#plt.use('Qt5Agg')

#根据json构建全联接地图,经过研究数据发现map是非对称的
def createMap(path):
    map={}
    T={}
    departure_station_id, arrival_station_id, distance, time = ReadJson.resolveMatrixJson(path)
    for id in departure_station_id:
        map[id]={}
        T[id]={}
    for i in range(len(departure_station_id)):
        start=departure_station_id[i]
        end=arrival_station_id[i]
        dis=distance[i]
        t=time[i]
        #if t >= 600:
        #    #两个站点之间的行驶时间超过10小时(600分钟)，路径无效
        #    print(start+" , ",end," , ",t)
        #    continue
        #if start == end:
        #    continue
        map[start][end]=dis
        T[start][end]=t


    #Sprint(departure_station_id)
    return map,T
#根据json构建vehicle的list
def createVehicle(path):
    Vehicles=[]
    vehicle_id, vehicle_length, vehicle_width, vehicle_weight, flag_down_fare, distance_fare=ReadJson.resolveVehicleJson(path)

    for i in range(len(vehicle_id)):
        id=vehicle_id[i]
        length=vehicle_length[i]
        width=vehicle_width[i]
        weight=vehicle_weight[i]
        startFare=flag_down_fare[i]
        disFare=distance_fare[i]
        v=entity.Vehicle(id,length,width,weight,startFare,disFare)
        Vehicles.append(v)

    return Vehicles
#将bin插入station的binList时，按照面积从大到小排序
def binInsert(station,bin):
    area = bin.length*bin.width
    binList = station.binList
    flag=0
    for i in range(len(binList)):
        tmpArea = binList[i].length*binList[i].width
        if area > tmpArea:
            binList.insert(i,bin)
            flag=1
            #print('insert')
            break
    if flag == 0:
        binList.append(bin)

    return binList

#根据json创建Bin的List，并将bin添加到所在的station
def createBin(path,stations):
    Bins=[]
    bin_id, bin_length, bin_width, bin_weight, station=ReadJson.resolveBinJson(path)

    for i in range(len(bin_id)):
        id=bin_id[i]
        length=bin_length[i]
        width=bin_width[i]
        weight=bin_weight[i]
        s=station[i]
        b=entity.Bin(id,length,width,weight)
        Bins.append(b)
        #stations[s].binList.append(b)
        stations[s].binList=binInsert(stations[s],b)
        stations[s].area = round( stations[s].area + b.length*b.width,5)
        stations[s].weight = round(stations[s].weight + b.weight,5)

        #stations[s].binList.append(b)
        stations[s].isEmpty=False

    #stations['S002'].binList.append(b)
    return Bins
#根据json创建station的字典存储结构
def createStation(path):
    Stations={}
    station_id, vehicle_limit, loading_time = ReadJson.resolveStationJson(path)
    maxLimit=0
    for i in range(len(station_id)):
        id = station_id[i]
        limit = vehicle_limit[i]
        if maxLimit<limit:
            maxLimit=limit
        t = loading_time[i]
        station=entity.Station(id,limit,t)
        Stations[id]=station

    return Stations,maxLimit
#打印一个station的信息
def printStation(s):
    print(s.id,len(s.binList),s.vehicle_limit,s.loading_time,s.area,s.weight)

#打印一个bin的信息
def printBin(b):
    print(b.id,b.length,b.width,b.weight)

#计算总的货物的area，weight，作为分配车辆的参考
def calBin(Bins):
    resArea=0.0;
    resWeight=0.0;

    for b in Bins:
        resArea=resArea+b.length*b.width

        resWeight=resWeight+b.weight
    return resArea,resWeight

#构建最小生成树
def createMST(map,T):
    newStations=[]
    lastStations=[]
    resMap={}
    resT={}
    for s in map:
        lastStations.append(s)
    newStations.append(lastStations[0])
    resMap[lastStations[0]]={}
    resT[lastStations[0]]={}
    lastStations.remove(lastStations[0])

    N=len(lastStations)
    for i in range(N-1):
        minDis = sys.maxsize
        choooseS = ""
        startS = ""
        for s in newStations:
            for lstS in lastStations:
                if lstS not in map[s]:
                    continue
                if minDis > map[s][lstS] :
                    minDis = map[s][lstS]
                    choooseS = lstS
                    startS = s
        if choooseS is '':
            startS=lastStations[0]
            newStations.append(startS)
            lastStations.remove(startS)
            resMap[startS]={}
            resT[startS]={}
            continue

        newStations.append(choooseS)
        lastStations.remove(choooseS)
        resMap[choooseS] = {}
        resT[choooseS]={}
        resMap[startS][choooseS] = minDis
        resMap[choooseS][startS] = map[choooseS][startS]
        resT[startS][choooseS] = T[startS][choooseS]
        resT[choooseS][startS] = T[choooseS][startS]

    return resMap,resT

#打印一个vehicle的信息
def printVehicle(v):
    print(v.id,v.length,v.width,v.weight,v.startPrice,v.perPrice)

#删除重复的vehicle和长，宽，载重参数一样但是价格更贵的vehicle
def deleteVehicle(vehicles,maxLimit):
    i = 1
    while i < len(vehicles):
        if i == 0:
            continue
        v1=vehicles[i]
        if v1.length>maxLimit:
            vehicles.remove(v1)
            continue

        for j in range(i):
            v2 = vehicles[j]
            if v1.length == v2.length and v1.width == v2.width and v1.weight == v2.weight:
                # delete v1
                if v1.startPrice == v2.startPrice and v1.perPrice == v2.perPrice:
                    vehicles.remove(v1)
                    i = i-1
                    break
                if v1.startPrice == v2.startPrice and v1.perPrice > v2.perPrice:
                    vehicles.remove(v1)
                    i = i - 1
                    break
                if v1.startPrice > v2.startPrice and v1.perPrice == v2.perPrice:
                    vehicles.remove(v1)
                    i = i - 1
                    break
                if v1.startPrice > v2.startPrice and v1.perPrice > v2.perPrice:
                    vehicles.remove(v1)
                    i = i - 1
                    break
                #delete v2
                if v1.startPrice == v2.startPrice and v1.perPrice < v2.perPrice:
                    vehicles.remove(v2)
                    i = i - 1
                    break
                if v1.startPrice < v2.startPrice and v1.perPrice == v2.perPrice:
                    vehicles.remove(v2)
                    i = i - 1
                    break
                if v1.startPrice < v2.startPrice and v1.perPrice < v2.perPrice:
                    vehicles.remove(v2)
                    i = i - 1
                    break

            #delete some expensive vehicles

        i = i+1


def floyd(mat,T):
    N=len(mat)

    for k in range(N):
        id_k=get_station_id(k)
        for i in range(N):
            id_i=get_station_id(i)
            for j in range(N):
                id_j=get_station_id(j)
                if mat[id_i][id_j] > mat[id_i][id_k] + mat[id_k][id_j]:
                    mat[id_i][id_j] = mat[id_i][id_k] + mat[id_k][id_j]
                    T[id_i][id_j] = T[id_i][id_k] + T[id_k][id_j]
    return mat,T

def get_station_id(num):
    station_id="S"
    if num < 10:
        station_id = station_id + "00" +num
    elif num < 100:
        station_id = station_id + "0" +num
    else:
        station_id = station_id + num
    return station_id

def cal_station_area_weight(station):
    station.area=0
    station.weight=0

    bin_list=station.binList
    for b in bin_list:
        station.area = round(station.area + b.length*b.width,5)
        station.weight = round(station.weight + b.weight,5)


def update_stations(stations):
    for s in stations:
        cal_station_area_weight(stations[s])
        if stations[s].weight == 0:
            stations[s].isEmpty = True

def draw_rect(vehicle,used_area):
    colors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple']
    fig = plt.figure()
    ax = fig.add_subplot(111)
    bin_list = vehicle.bin_list
    plt.xlim(0, round(vehicle.width+0.1,5))
    plt.ylim(0, round(vehicle.length+0.1,5))

    for bin in bin_list:
        point_list= bin.pointList
        start1=point_list[0].x
        end1=point_list[0].y
        width=round(point_list[1].x - point_list[0].x,5)
        height=round(point_list[2].y - point_list[1].y,5)
        print (start1,end1, width,height)
        color_index=random.randint(1,100)
        plt.gca().add_patch(plt.Rectangle((start1, end1), width, height,facecolor=colors[color_index%7]))
    used_rate = round(used_area/(vehicle.length* vehicle.width),5)
    plt.suptitle("used_rate: "+str(used_rate))
    date = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    pic_name = '../pic/rect_' + str(date) + '.png'
    plt.savefig(pic_name)
    plt.show()


    #fig.savefig("rect1.png", dpi=90, bbox_inches='tight')



if __name__ == '__main__':

    path="../dataset/month3/"

    print("enter")
    map,time=createMap(path+"matrix.json")
    stations,maxLimit=createStation(path+"station.json")
    bins=createBin(path+"bin.json",stations)
    vehicles=createVehicle(path+"vehicle.json")

    for s in stations:
        printStation(stations[s])
    #print(stations)
    print("\n")
    #print(map)
    #print(time)
    #for s in map:
    #   print(map[s])

    mts,T=createMST(map,time)
    #print(len(mts))
    #for s in mts:
    #   print(s," : ",mts[s])

    binList=stations['S001'].binList
    for i in range(len(binList)):
        #area=binList[i].length * binList[i].width
        printBin(binList[i])

    print(len(binList))
    print("\n")
    #print(len(vehicles))
    deleteVehicle(vehicles,maxLimit)
    #print(len(vehicles))

    for i in range(len(vehicles)):
       printVehicle(vehicles[i])
    print("\n")
    totalArea,totalWeight = calBin(bins)

    print(totalArea," , ",totalWeight)

    #print(maxLimit)

    #print(len(mts))



