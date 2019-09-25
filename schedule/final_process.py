# -*- coding:utf-8 -*-
from process import geneticAlgm
from entity import entity
from reinforcement_learning import r_learning

def pick_bins(vehicle_list,stations,map,time):
    for v in vehicle_list:
        if v.max_height < v.length * 0.6:
            for v1 in vehicle_list:
                if v1.id == v.id:
                    continue
                #if v1.max_height > v1.length *0.9:
                #    continue
                s_id = v1.path[-1]
                if v.path[0] not in time[s_id]:
                    continue
                tmp_time=v1.usedTime + time[s_id][v.path[0]] +stations[v.path[0]].loading_time
                if tmp_time <= 600 and map[s_id][v.path[0]] * v1.perPrice < v.startPrice and v1.length <= stations[v.path[0]].vehicle_limit:
                    station = stations[s_id]
                    tmp_vehicle = entity.Vehicle(v1.id, v1.length, v1.width, v1.weight, v1.startPrice, v1.perPrice)
                    tmp_station=entity.Station(v.path[0],station.vehicle_limit,station.loading_time)

                    for b in v.bin_list:
                        tmp_bin=entity.Bin(b.id,b.length,b.width,b.weight,b.local_station)
                        tmp_station.binList.append(tmp_bin)
                        tmp_vehicle.station_bin[b.local_station]=[]
                        tmp_station.isEmpty=False
                    for b in v1.bin_list:
                        tmp_vehicle.station_bin[b.local_station]=[]

                    for b in v1.bin_list:
                        tmp_bin=entity.Bin(b.id,b.length,b.width,b.weight,b.local_station)
                        if len(b.pointList)==0:
                            break
                        tmp_bin.pointList.append(b.pointList[0])
                        tmp_bin.pointList.append(b.pointList[1])
                        tmp_bin.pointList.append(b.pointList[2])
                        tmp_bin.pointList.append(b.pointList[3])
                        tmp_vehicle.bin_list.append(tmp_bin)
                        tmp_vehicle.station_bin[b.local_station].append(tmp_bin)
                    for l in v1.lines:
                        #tmp_line = entity.Line(entity.Point(l.start.x,l.start.y),entity.Point(l.end.x, l.end.y),l.left_height,l.right_height)
                        tmp_vehicle.lines.append(entity.Line(entity.Point(l.start.x,l.start.y),entity.Point(l.end.x, l.end.y),l.left_height,l.right_height))
                    #skyLine.skyline(tmp_vehicle,tmp_station)
                    r_learning.bin_packing_function(tmp_vehicle, tmp_station)
                    if tmp_station.isEmpty ==True:
                        tmp_vehicle.path=[]
                        for p in v1.path:
                            tmp_vehicle.path.append(p)
                        for p in v.path:
                            tmp_vehicle.path.append(p)
                        vehicle_list.remove(v)
                        vehicle_list.remove(v1)
                        tmp_vehicle.usedTime = v1.usedTime + time[s_id][v.path[0]] +stations[v.path[0]].loading_time
                        vehicle_list.append(tmp_vehicle)
                        print("+++++OK")
                        break

def change_vehicle(vehicle_list,vehicles):
    for i in range(len(vehicle_list)):
        v=vehicle_list[i]
        if v.id== u'V388':
            print "dddddd"
        if v.length == 17.5 and v.max_height<= 9.6:
            for v2 in vehicles:
                v1=geneticAlgm.create_new_vehicle(v2)
                if v2.is_available == True:
                    tmp_station = entity.Station(v.path[0], v1.length, 0)
                    for b in v.bin_list:
                        tmp_bin=entity.Bin(b.id,b.length,b.width,b.weight,b.local_station)
                        tmp_station.binList.append(tmp_bin)
                        tmp_station.isEmpty=False
                    #skyLine.skyline(v1,tmp_station)
                    r_learning.bin_packing_function(v1, tmp_station)
                    v1.path = v.path
                    if tmp_station.isEmpty == True:
                        v1.path=[]
                        for p in v.path:
                            v1.path.append(p)
                        vehicle_list.remove(v)
                        vehicle_list.append(v1)
                        v2.is_available = False
                        i = i-1
                        print("+++++++++")
                        break
        elif v.length == 9.6 and v.max_height<= 7.8:
            for v2 in vehicles:
                v1=geneticAlgm.create_new_vehicle(v2)
                if v2.is_available == True:
                    tmp_station = entity.Station(v.path[0], v1.length, 0)
                    for b in v.bin_list:
                        tmp_bin=entity.Bin(b.id,b.length,b.width,b.weight,b.local_station)
                        tmp_station.binList.append(tmp_bin)
                        tmp_station.isEmpty=False
                    #skyLine.skyline(v1,tmp_station)
                    r_learning.bin_packing_function(v1,tmp_station)
                    v1.path=v.path
                    if tmp_station.isEmpty == True:

                        v1.path = []
                        for p in v.path:
                            v1.path.append(p)
                        vehicle_list.remove(v)
                        vehicle_list.append(v1)
                        v2.is_available = False
                        i=i-1
                        print("--------")
                        break

