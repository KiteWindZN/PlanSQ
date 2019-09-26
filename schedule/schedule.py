# -*- coding:utf-8 -*-
"""
此文件为车辆的调度过程
"""
from process import geneticAlgm
from entity import entity
from process import createEntity
from process import skyLine
import sys
from reinforcement_learning import  r_learning
import random

#使用强化学习的装箱算法的调度，station_list1，station_list2，station_list3分别为小站，中站和大站的列表
#返回结果为使用的车辆信息
def schedule_mst_r_learning(stations,vehicles,station_list1,station_list2,station_list3,mst,T):
    res_vehicle_list=[]

    r_learning.label_stations(stations)
    for i in range(len(station_list1)):
        if (i+1) % 10==0:
            print i
        if station_list1[i]==u"S032":
            print station_list1[i]
        s_id = station_list1[i]

        choose_station=stations[s_id]
        if choose_station.isEmpty==True:
            continue
        choose_vehicle_num=choose_vehicle_index(vehicles,choose_station)
        choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
        if choose_vehicle.id == u"V709":
            print choose_vehicle.id
        #choose_vehicle.path.append(s_id)
        choose_vehicle.usedTime = choose_vehicle.usedTime + choose_station.loading_time
        vehicles[choose_vehicle_num].is_available = False

        max_height=r_learning.bin_packing_function(choose_vehicle,choose_station)
        r_learning.label_station(choose_station)
        #res_vehicle_list.append(choose_vehicle)
        createEntity.cal_station_area_weight(choose_station)

        while choose_station.weight!=0:
            if len(choose_vehicle.path)>1:
                max_height, choose_vehicle = r_learning.merge_packing(choose_vehicle, stations)
            res_vehicle_list.append(choose_vehicle)
            choose_vehicle_num = choose_vehicle_index(vehicles, choose_station)
            choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
            if choose_vehicle.id == u"V709":
                print choose_vehicle.id

            choose_vehicle.usedTime = choose_vehicle.usedTime + choose_station.loading_time
            vehicles[choose_vehicle_num].is_available = False
            #skyLine.make_new_binList(choose_station,0.7)
            max_height=r_learning.bin_packing_function(choose_vehicle, choose_station)
            r_learning.label_station(choose_station)
            #stations[choose_station.id] = choose_station
            createEntity.cal_station_area_weight(choose_station)
            used_rate = cal_used_rate(choose_vehicle)


            s_id = choose_station.id
            while max_height < choose_vehicle.length*0.9 and choose_vehicle.used_weight < choose_vehicle.weight*0.9:
            #while used_rate < 0.85 and choose_vehicle.used_weight < choose_vehicle.weight * 0.9:
                next_s_id, tmp_dis = next_station(choose_vehicle, s_id, stations, mst, T)
                if next_s_id == u"S044":
                    print "fffffffff"

                if next_s_id != "-1" and next_s_id != s_id and tmp_dis * choose_vehicle.perPrice < choose_vehicle.startPrice:
                    add_bin2waste(choose_vehicle,stations[next_s_id])
                    max_height=r_learning.bin_packing_function(choose_vehicle, stations[next_s_id])
                    #r_learning.label_station(stations[next_s_id])
                    tmp_weight=stations[next_s_id].weight
                    createEntity.cal_station_area_weight(stations[next_s_id])
                    if tmp_weight == stations[next_s_id].weight:
                        break
                    s_id=next_s_id
                else:
                    break

                used_rate = cal_used_rate(choose_vehicle)
                if used_rate > 1:
                    print("zzzzz")

        if choose_station.weight == 0:

            used_rate = cal_used_rate(choose_vehicle)
            s_id = choose_vehicle.path[-1]
            while max_height < choose_vehicle.length*0.9 and choose_vehicle.used_weight < choose_vehicle.weight*0.9:
            #while used_rate < 0.85 and choose_vehicle.used_weight < choose_vehicle.weight * 0.9:
                next_s_id, tmp_dis = next_station(choose_vehicle, s_id, stations, mst, T)
                if next_s_id == u"S044":
                    print "fffffffff"
                dis_cost = tmp_dis * choose_vehicle.perPrice
                if next_s_id != "-1" and next_s_id!= s_id and dis_cost < choose_vehicle.startPrice:
                    add_bin2waste(choose_vehicle, stations[next_s_id])
                    max_height=r_learning.bin_packing_function(choose_vehicle, stations[next_s_id])
                    r_learning.label_station(stations[next_s_id])
                    tmp_weight = stations[next_s_id].weight
                    createEntity.cal_station_area_weight(stations[next_s_id])
                    if tmp_weight == stations[next_s_id].weight:
                        break
                    s_id=next_s_id
                else:
                    break
                used_rate = cal_used_rate(choose_vehicle)
            if len(choose_vehicle.path)>1:
                max_height, choose_vehicle = r_learning.merge_packing(choose_vehicle, stations)
            res_vehicle_list.append(choose_vehicle)


    for i in range(len(station_list2)):
        if (i+1) % 10==0:
            print i
        s_id  = station_list2[i]
        if station_list2[i]==u"S021":
            print station_list2[i]
        choose_station=stations[s_id]
        if choose_station.isEmpty==True:
            continue
        choose_vehicle_num=choose_vehicle_index(vehicles,choose_station)
        choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
        if choose_vehicle.id == u"V709":
            print ("aaaaaa")
        #choose_vehicle.path.append(s_id)
        vehicles[choose_vehicle_num].is_available = False

        max_height=r_learning.bin_packing_function(choose_vehicle, choose_station)
        r_learning.label_station(choose_station)
        createEntity.cal_station_area_weight(choose_station)
        while choose_station.weight!=0:
            if len(choose_vehicle.path)>1:
                max_height, choose_vehicle = r_learning.merge_packing(choose_vehicle, stations)
            res_vehicle_list.append(choose_vehicle)
            choose_vehicle_num = choose_vehicle_index(vehicles, choose_station)
            choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
            if choose_vehicle.id == u"V206":
                print ("aaaaaa")
            #choose_vehicle.path.append(s_id)
            vehicles[choose_vehicle_num].is_available = False

            max_height=r_learning.bin_packing_function(choose_vehicle, choose_station)
            r_learning.label_station(choose_station)

            createEntity.cal_station_area_weight(choose_station)
            used_rate = cal_used_rate(choose_vehicle)

            s_id = choose_station.id
            while max_height < choose_vehicle.length*0.9 and choose_vehicle.used_weight < choose_vehicle.weight*0.9:
            #while used_rate < 0.85 and choose_vehicle.used_weight < choose_vehicle.weight * 0.9:

                next_s_id, tmp_dis = next_station(choose_vehicle, s_id, stations, mst, T)
                if next_s_id == u"S044":
                    print "fffffffff"
                if next_s_id != "-1" and next_s_id != s_id and tmp_dis * choose_vehicle.perPrice < choose_vehicle.startPrice:
                    add_bin2waste(choose_vehicle, stations[next_s_id])
                    max_height=r_learning.bin_packing_function(choose_vehicle,stations[next_s_id])
                    r_learning.label_station(stations[next_s_id])
                    tmp_weight = stations[next_s_id].weight
                    createEntity.cal_station_area_weight(stations[next_s_id])
                    if tmp_weight == stations[next_s_id].weight:
                        break
                    s_id=next_s_id
                else:
                    break
                used_rate = cal_used_rate(choose_vehicle)


        if choose_station.weight == 0:
            s_id = choose_vehicle.path[-1]
            while max_height < choose_vehicle.length*0.9 and choose_vehicle.used_weight < choose_vehicle.weight*0.9:
                next_s_id, tmp_dis = next_station(choose_vehicle, s_id, stations, mst, T)
                if next_s_id == u"S044":
                    print "fffffffff"
                if next_s_id != "-1" and tmp_dis * choose_vehicle.perPrice < choose_vehicle.startPrice:
                    add_bin2waste(choose_vehicle, stations[next_s_id])
                    max_height=r_learning.bin_packing_function(choose_vehicle,stations[next_s_id])
                    r_learning.label_station(stations[next_s_id])
                    tmp_weight = stations[next_s_id].weight
                    createEntity.cal_station_area_weight(stations[next_s_id])
                    if tmp_weight == stations[next_s_id].weight:
                        break
                    s_id=next_s_id
                else:
                    break
            if len(choose_vehicle.path)>1:
                max_height, choose_vehicle = r_learning.merge_packing(choose_vehicle, stations)
            res_vehicle_list.append(choose_vehicle)



    for i in range(len(station_list3)):
        if (i+1) % 10==0:
            print i
        if station_list3[i]==u"S204":
            print station_list3[i]
        s_id = station_list3[i]

        choose_station=stations[s_id]
        if choose_station.isEmpty==True:
            continue

        choose_vehicle_num = choose_vehicle_index(vehicles, choose_station)
        choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
        if choose_vehicle.id == u"V696":
            print choose_vehicle.id
        vehicles[choose_vehicle_num].is_available = False
        #skyLine.make_new_binList(choose_station, 0.7)
        max_height=r_learning.bin_packing_function(choose_vehicle,choose_station)
        r_learning.label_station(choose_station)
        #stations[choose_station.id] = choose_station
        createEntity.cal_station_area_weight(choose_station)
        while choose_station.weight!=0:
            if len(choose_vehicle.path)>1:
                max_height, choose_vehicle = r_learning.merge_packing(choose_vehicle, stations)
            res_vehicle_list.append(choose_vehicle)
            choose_vehicle_num = choose_vehicle_index(vehicles, choose_station)
            choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
            #res_vehicle_list.append(choose_vehicle)
            vehicles[choose_vehicle_num].is_available = False
            if choose_vehicle.id == u"V696":
                print choose_vehicle.id
            max_height=r_learning.bin_packing_function(choose_vehicle,choose_station)
            createEntity.cal_station_area_weight(choose_station)

            s_id=choose_station.id
            while max_height < choose_vehicle.length*0.92 and choose_vehicle.used_weight < choose_vehicle.weight*0.9:
                next_s_id, tmp_dis = next_station(choose_vehicle, s_id, stations, mst, T)
                if next_s_id == u"S123":
                    print "fffffffff"
                if next_s_id != "-1" and tmp_dis * choose_vehicle.perPrice < choose_vehicle.startPrice:
                    add_bin2waste(choose_vehicle, stations[next_s_id])

                    max_height=r_learning.bin_packing_function(choose_vehicle,stations[next_s_id])
                    r_learning.label_station(stations[next_s_id])

                    choose_vehicle.usedTime += T[s_id][next_s_id] + stations[next_s_id].loading_time
                    tmp_weight = stations[next_s_id].weight
                    createEntity.cal_station_area_weight(stations[next_s_id])
                    if tmp_weight == stations[next_s_id].weight:
                        break
                    s_id=next_s_id
                else:
                    break

        max_height = choose_vehicle.max_height
        if choose_station.weight == 0:

            avg_h=avg_height(choose_vehicle.lines)
            s_id=choose_vehicle.path[-1]
            while max_height < choose_vehicle.length*0.9 and choose_vehicle.used_weight < choose_vehicle.weight*0.9:
                next_s_id, tmp_dis = next_station(choose_vehicle, s_id, stations, mst, T)
                if next_s_id == u"S123":
                    print "fffffffff"
                if next_s_id != "-1" and tmp_dis * choose_vehicle.perPrice < choose_vehicle.startPrice:
                    add_bin2waste(choose_vehicle, stations[next_s_id])
                    createEntity.cal_station_area_weight(choose_station)
                    if stations[next_s_id].weight ==0:
                        stations[next_s_id].isEmpty=True

                    max_height=r_learning.bin_packing_function(choose_vehicle,stations[next_s_id])
                    r_learning.label_station(stations[next_s_id])
                    choose_vehicle.usedTime += T[s_id][next_s_id] + stations[next_s_id].loading_time
                    tmp_weight = stations[next_s_id].weight
                    createEntity.cal_station_area_weight(stations[next_s_id])
                    if tmp_weight == stations[next_s_id].weight:
                        break
                    s_id=next_s_id
                else:
                    break
                avg_h = avg_height(choose_vehicle.lines)
            if len(choose_vehicle.path)>1:
                max_height, choose_vehicle = r_learning.merge_packing(choose_vehicle, stations)
            res_vehicle_list.append(choose_vehicle)


    return res_vehicle_list


#为站点选择合适的vehicle
def choose_vehicle_index(vehicle_list,station):
    res=-1
    i = len(vehicle_list) - 1
    while i>0:
        if vehicle_list[i].length <= station.vehicle_limit and vehicle_list[i].is_available == True:
            res=i
            break
        i = i-1
    return res


# a-greedy,与label之和为0相结合
def next_station(vehicle,s_id,stations,map,time):
    label=0
    bin_list=vehicle.bin_list
    tmp_area=0
    for b in bin_list:
        tmp_area = round(b.length*b.width+tmp_area,5)
    if tmp_area/(vehicle.width * vehicle.max_height) <0.85:
        label=-1

    nobor_list = map[s_id]
    tmp_dis = sys.maxsize
    next_s_id = "-1"
    next_list = []
    next_dis = []
    for n_s in nobor_list:
        if map[s_id][n_s] < tmp_dis and n_s != s_id and stations[n_s].isEmpty == False and stations[n_s].vehicle_limit >= vehicle.length\
                and vehicle.usedTime+time[s_id][n_s] + stations[n_s].loading_time <= 600 and n_s not in vehicle.path:
            tmp_dis = map[s_id][n_s]
            next_s_id = n_s
            next_list.append(n_s)
            next_dis.append(tmp_dis)
    min_dis=tmp_dis
    if label == 0:
        return next_s_id, tmp_dis
    if next_s_id == "-1" or random.random() < 0.9 or len(next_dis) < 3:
        return next_s_id,tmp_dis
    data = [(dis, id) for dis, id in zip(next_dis,next_list)]
    data.sort()
    data.reverse()
    next_list = [id for dis, id in data]
    next_dis = [dis for dis, id in data]
    #index= random.randint(0,2)
    index=-1

    tmp_dis=sys.maxsize
    for i in range(len(next_list)):
        s = next_list[i]
        if label + stations[s].label == 0 and next_dis[i]<20000 and tmp_dis<next_dis[i]:
            index = i
            tmp_dis = next_dis[i]
    if index!=-1:
        return next_list[index],next_dis[index]
    return next_s_id,min_dis


def avg_height(lines):
    avg_h=0
    for l in lines:
        avg_h += l.height
    avg_h = avg_h / len(lines)

    return avg_h

#车辆被调度到一个新站点时，对于浪费空间进行塞缝处理
def add_bin2waste(vehicle,station):
    s_id=station.id
    if s_id not in vehicle.station_bin:
        vehicle.station_bin[s_id]=[]
    waste_rect = vehicle.waste_area
    i=0
    N=len(waste_rect)
    while i < N:
        rect  = waste_rect[i]
        res=choose_for_waste(rect,station.binList)
        if res == -1:
            i=i+1
            continue
        else:
            width=res.width
            length=res.length

            res.pointList.append(entity.Point(rect.start.x,rect.start.y))
            res.pointList.append(entity.Point(rect.start.x+width, rect.start.y))
            res.pointList.append(entity.Point(rect.start.x + width, rect.start.y+length))
            res.pointList.append(entity.Point(rect.start.x, rect.start.y+length))

            vehicle.bin_list.append(res)
            vehicle.station_bin[s_id].append(res)
            skyLine.delete_bin(station.binList,res)
            vehicle.waste_area.remove(rect)
            i = i-1
        i=i+1
        N = len(waste_rect)

#为浪费空间选择可以装入的面积最大的货物
def choose_for_waste(rect,bins):
    bin_list=[]
    width=rect.end.x-rect.start.x
    length=rect.left_height

    for b in bins:
        if b.width <= width and b.length<=length:
            bin_list.append(b)
        elif b.length<=width and b.width<=length:
            b.rotate_bin()
            bin_list.append(b)
    tmp_area=0
    index=-1
    for i in range(len(bin_list)):
        b=bin_list[i]
        if b.width*b.length>tmp_area:
            index=i
            tmp_area=b.width*b.length
    if index == -1:
        return index
    return bin_list[index]

#计算车辆的装载率
def cal_used_rate(v):
    tmp_area=0
    for b in v.bin_list:
        tmp_area = round(tmp_area + b.length * b.width, 5)
    return tmp_area / (v.length * v.width)

#随机化序列
def random_list(list):
    res_list=[]
    while len(list)>0:
        i=random.randint(0,len(list)-1)
        res_list.append(list[i])
        list.remove(list[i])
    return res_list


#弃用
def pour_bins(vehicle,stations):
    for b in vehicle.bin_list:
        b.pointList = []
        stations[b.local_station].binList.append(b)

    merge_station=entity.Station(vehicle.path[0],stations[vehicle.path[0]].vehicle_limit,stations[vehicle.path[0]].loading_time)
    for p in vehicle.path:
        tmp_bin_list=stations[p].binList
        for b in tmp_bin_list:
            tmp_b=geneticAlgm.create_new_bin(b)
            merge_station.binList.append(tmp_b)
            merge_station.isEmpty=False

    for s in vehicle.path:
        ss = stations[s]
        ss.isEmpty = False
        createEntity.cal_station_area_weight(ss)
    #choose_station = stations[vehicle.path[0]]
    choose_station=merge_station
    choose_vehicle = geneticAlgm.create_new_vehicle(vehicle)
    tmp_line=entity.Line(entity.Point(0,0),entity.Point(choose_vehicle.width,0),choose_vehicle.length,choose_vehicle.length)
    choose_vehicle.lines.append(tmp_line)
    #choose_vehicle.path.append(choose_station.id)
    choose_vehicle.max_height = 0
    #skyLine.compose_skyline(choose_vehicle,choose_station)
    max_height=r_learning.bin_packing_function(choose_vehicle,choose_station)
    choose_vehicle.path=vehicle.path
    vehicle=choose_vehicle

    for b in vehicle.bin_list:
        local_station=b.local_station
        skyLine.delete_bin(stations[local_station].binList,b)

    for p in vehicle.path:
        createEntity.cal_station_area_weight(stations[p])

    return max_height,vehicle

#弃用
def schedule_mst(stations,vehicles,station_list1,station_list2,station_list3,mst,T):
    res_vehicle_list=[]
    for i in range(len(station_list1)):
        if (i+1) % 100==0:
            print i
        s_id = station_list1[i]

        choose_station=stations[s_id]
        if choose_station.isEmpty==True:
            continue
        choose_vehicle_num=choose_vehicle_index(vehicles,choose_station)
        choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
        if choose_vehicle.id == u'V645':
            print ("znzn")

        #choose_vehicle.path.append(s_id)
        choose_vehicle.usedTime = choose_vehicle.usedTime + choose_station.loading_time
        vehicles[choose_vehicle_num].is_available = False

        max_height,choose_vehicle,choose_station = skyLine.process_skyline(choose_vehicle,choose_station)
        stations[choose_station.id] = choose_station
        #res_vehicle_list.append(choose_vehicle)
        used_rate = cal_used_rate(choose_vehicle)
        if used_rate < 0.8:
            max_height,choose_vehicle=pour_bins(choose_vehicle,stations)
        createEntity.cal_station_area_weight(choose_station)
        if choose_station.id == u"S196":
            print "aaa"

        while choose_station.weight!=0:
            res_vehicle_list.append(choose_vehicle)
            choose_vehicle_num = choose_vehicle_index(vehicles, choose_station)
            choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
            if choose_vehicle.id == u'V645':
                print ("znzn")

            choose_vehicle.usedTime = choose_vehicle.usedTime + choose_station.loading_time
            vehicles[choose_vehicle_num].is_available = False
            #skyLine.make_new_binList(choose_station,0.7)
            max_height,choose_vehicle,choose_station = skyLine.process_skyline(choose_vehicle, choose_station)
            stations[choose_station.id] = choose_station
            createEntity.cal_station_area_weight(choose_station)
            used_rate = cal_used_rate(choose_vehicle)
            if used_rate < 0.8:
                max_height, choose_vehicle = pour_bins(choose_vehicle, stations)
                createEntity.cal_station_area_weight(choose_station)
            s_id = choose_station.id
            while max_height < choose_vehicle.length*0.9 and choose_vehicle.used_weight < choose_vehicle.weight*0.9:
            #while used_rate < 0.85 and choose_vehicle.used_weight < choose_vehicle.weight * 0.9:
                next_s_id, tmp_dis = next_station(choose_vehicle, s_id, stations, mst, T)
                if choose_vehicle.id == u'V645':
                    print ("znzn")

                if next_s_id != "-1" and next_s_id != s_id and tmp_dis * choose_vehicle.perPrice < choose_vehicle.startPrice:
                    add_bin2waste(choose_vehicle,stations[next_s_id])
                    max_height,choose_vehicle,stations[next_s_id]=skyLine.process_skyline(choose_vehicle, stations[next_s_id])
                    tmp_weight=stations[next_s_id].weight
                    createEntity.cal_station_area_weight(stations[next_s_id])
                    if tmp_weight == stations[next_s_id].weight:
                        break
                    s_id=next_s_id
                else:
                    break

                used_rate = cal_used_rate(choose_vehicle)
                if used_rate > 1:
                    print("zzzzz")
            used_rate = cal_used_rate(choose_vehicle)
            if used_rate < 0.8:
                max_height, choose_vehicle = pour_bins(choose_vehicle, stations)
                createEntity.cal_station_area_weight(choose_station)


        if choose_station.weight == 0:

            used_rate = cal_used_rate(choose_vehicle)
            while max_height < choose_vehicle.length*0.9 and choose_vehicle.used_weight < choose_vehicle.weight*0.9:
            #while used_rate < 0.85 and choose_vehicle.used_weight < choose_vehicle.weight * 0.9:
                next_s_id, tmp_dis = next_station(choose_vehicle, s_id, stations, mst, T)

                dis_cost = tmp_dis * choose_vehicle.perPrice
                if next_s_id != "-1" and next_s_id!= s_id and dis_cost < choose_vehicle.startPrice:
                    add_bin2waste(choose_vehicle, stations[next_s_id])
                    max_height,choose_vehicle,stations[next_s_id]=skyLine.process_skyline(choose_vehicle, stations[next_s_id])
                    tmp_weight = stations[next_s_id].weight
                    createEntity.cal_station_area_weight(stations[next_s_id])
                    if tmp_weight == stations[next_s_id].weight:
                        break
                    s_id=next_s_id
                else:
                    break
                used_rate = cal_used_rate(choose_vehicle)

            res_vehicle_list.append(choose_vehicle)


    for i in range(len(station_list2)):
        if (i+1) % 100==0:
            print i
        s_id  = station_list2[i]

        choose_station=stations[s_id]
        createEntity.cal_station_area_weight(choose_station)
        if choose_station.isEmpty==True:
            continue
        choose_vehicle_num=choose_vehicle_index(vehicles,choose_station)
        choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
        if choose_vehicle.id == u'V399':
            print ("znzn")
        #choose_vehicle.path.append(s_id)
        vehicles[choose_vehicle_num].is_available = False
        #skyLine.make_new_binList(choose_station, 0.7)
        max_height, choose_vehicle, choose_station = skyLine.process_skyline(choose_vehicle, choose_station)
        stations[choose_station.id] = choose_station
        used_rate = cal_used_rate(choose_vehicle)
        if used_rate < 0.8:
            max_height, choose_vehicle = pour_bins(choose_vehicle, stations)
        createEntity.cal_station_area_weight(choose_station)

        while choose_station.weight!=0:
            res_vehicle_list.append(choose_vehicle)
            choose_vehicle_num = choose_vehicle_index(vehicles, choose_station)
            choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
            if choose_vehicle.id == u'V399':
                print ("znzn")
            #choose_vehicle.path.append(s_id)
            vehicles[choose_vehicle_num].is_available = False

            max_height, choose_vehicle, choose_station = skyLine.process_skyline(choose_vehicle,
                                                                                      choose_station)

            stations[choose_station.id] = choose_station

            used_rate = cal_used_rate(choose_vehicle)
            if used_rate < 0.8:
                max_height, choose_vehicle = pour_bins(choose_vehicle, stations)
                createEntity.cal_station_area_weight(choose_station)

            createEntity.cal_station_area_weight(choose_station)
            used_rate = cal_used_rate(choose_vehicle)
            s_id = choose_station.id
            while max_height < choose_vehicle.length*0.9 and choose_vehicle.used_weight < choose_vehicle.weight*0.9:
            #while used_rate < 0.85 and choose_vehicle.used_weight < choose_vehicle.weight * 0.9:

                next_s_id, tmp_dis = next_station(choose_vehicle, s_id, stations, mst, T)

                if next_s_id != "-1" and next_s_id != s_id and tmp_dis * choose_vehicle.perPrice < choose_vehicle.startPrice:
                    add_bin2waste(choose_vehicle, stations[next_s_id])
                    max_height, choose_vehicle, stations[next_s_id] = skyLine.process_skyline(choose_vehicle,
                                                                                              stations[next_s_id])
                    tmp_weight = stations[next_s_id].weight
                    createEntity.cal_station_area_weight(stations[next_s_id])
                    if tmp_weight == stations[next_s_id].weight:
                        break
                    s_id=next_s_id
                else:
                    break
                used_rate = cal_used_rate(choose_vehicle)
            used_rate = cal_used_rate(choose_vehicle)
            if used_rate < 0.8:
                max_height, choose_vehicle = pour_bins(choose_vehicle, stations)
                createEntity.cal_station_area_weight(choose_station)


        if choose_station.weight == 0:

            while max_height < choose_vehicle.length*0.9 and choose_vehicle.used_weight < choose_vehicle.weight*0.9:
                next_s_id, tmp_dis = next_station(choose_vehicle, s_id, stations, mst, T)
                if next_s_id != "-1" and tmp_dis * choose_vehicle.perPrice < choose_vehicle.startPrice:
                    add_bin2waste(choose_vehicle, stations[next_s_id])
                    max_height, choose_vehicle, stations[next_s_id] = skyLine.process_skyline(choose_vehicle,
                                                                                              stations[next_s_id])
                    tmp_weight = stations[next_s_id].weight
                    createEntity.cal_station_area_weight(stations[next_s_id])
                    if tmp_weight == stations[next_s_id].weight:
                        break
                    s_id=next_s_id
                else:
                    break
            used_rate = cal_used_rate(choose_vehicle)
            if used_rate < 0.8:
                max_height, choose_vehicle = pour_bins(choose_vehicle, stations)
            res_vehicle_list.append(choose_vehicle)

    for i in range(len(station_list3)):
        if (i+1) % 100==0:
            print i
        if station_list3[i]==u'S041':
            print "S041"
        s_id  = station_list3[i]

        choose_station=stations[s_id]
        if choose_station.isEmpty==True:
            continue
        choose_vehicle_num=choose_vehicle_index(vehicles,choose_station)
        choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
        if choose_vehicle.id == u'V653':
            print ("znzn")
        vehicles[choose_vehicle_num].is_available = False
        #skyLine.make_new_binList(choose_station, 0.7)
        max_height, choose_vehicle, choose_station = skyLine.process_skyline(choose_vehicle,
                                                                                  choose_station)
        stations[choose_station.id] = choose_station
        used_rate = cal_used_rate(choose_vehicle)
        if used_rate < 0.8:
            max_height, choose_vehicle = pour_bins(choose_vehicle, stations)
            createEntity.cal_station_area_weight(choose_station)

        createEntity.cal_station_area_weight(choose_station)

        if choose_station.id == u'S204':
            print choose_station.id

        while choose_station.weight!=0:
            res_vehicle_list.append(choose_vehicle)
            choose_vehicle_num = choose_vehicle_index(vehicles, choose_station)
            choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
            if choose_vehicle.id == u'V653':
                print ("znzn")
            #res_vehicle_list.append(choose_vehicle)
            vehicles[choose_vehicle_num].is_available = False

            max_height, choose_vehicle, choose_station = skyLine.process_skyline(choose_vehicle,
                                                                                      choose_station)
            stations[choose_station.id] = choose_station
            used_rate = cal_used_rate(choose_vehicle)
            if used_rate < 0.8:
                max_height, choose_vehicle = pour_bins(choose_vehicle, stations)
                createEntity.cal_station_area_weight(choose_station)

            createEntity.cal_station_area_weight(choose_station)
            s_id = choose_station.id
            while max_height < choose_vehicle.length*0.9 and choose_vehicle.used_weight < choose_vehicle.weight*0.9:
                next_s_id, tmp_dis = next_station(choose_vehicle, s_id, stations, mst, T)

                if next_s_id != "-1" and tmp_dis * choose_vehicle.perPrice < choose_vehicle.startPrice:
                    add_bin2waste(choose_vehicle, stations[next_s_id])

                    max_height, choose_vehicle, stations[next_s_id] = skyLine.process_skyline(choose_vehicle,
                                                                                              stations[next_s_id])
                    choose_vehicle.usedTime += T[s_id][next_s_id] + stations[next_s_id].loading_time
                    tmp_weight = stations[next_s_id].weight
                    createEntity.cal_station_area_weight(stations[next_s_id])
                    if tmp_weight == stations[next_s_id].weight:
                        break
                    s_id=next_s_id
                else:
                    break
            used_rate = cal_used_rate(choose_vehicle)
            if used_rate < 0.8:
                max_height, choose_vehicle = pour_bins(choose_vehicle, stations)
                createEntity.cal_station_area_weight(choose_station)

        max_height = choose_vehicle.max_height
        if choose_station.weight == 0:
            if choose_station.id == u'S204':
                print choose_station.id

            avg_h=avg_height(choose_vehicle.lines)
            while max_height < choose_vehicle.length*0.9 and choose_vehicle.used_weight < choose_vehicle.weight*0.9:
                next_s_id, tmp_dis = next_station(choose_vehicle, s_id, stations, mst, T)

                if next_s_id != "-1" and tmp_dis * choose_vehicle.perPrice < choose_vehicle.startPrice:
                    add_bin2waste(choose_vehicle, stations[next_s_id])
                    createEntity.cal_station_area_weight(choose_station)
                    if stations[next_s_id].weight ==0:
                        stations[next_s_id].isEmpty=True

                    max_height, choose_vehicle, stations[next_s_id] = skyLine.process_skyline(choose_vehicle,
                                                                                              stations[next_s_id])
                    choose_vehicle.usedTime += T[s_id][next_s_id] + stations[next_s_id].loading_time
                    tmp_weight = stations[next_s_id].weight
                    createEntity.cal_station_area_weight(stations[next_s_id])
                    if tmp_weight == stations[next_s_id].weight:
                        break
                    s_id=next_s_id
                else:
                    break
                avg_h = avg_height(choose_vehicle.lines)
            used_rate = cal_used_rate(choose_vehicle)
            if used_rate < 0.8:
                max_height, choose_vehicle = pour_bins(choose_vehicle, stations)
                createEntity.cal_station_area_weight(choose_station)

            res_vehicle_list.append(choose_vehicle)

    return res_vehicle_list