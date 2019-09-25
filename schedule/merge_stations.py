# -*- coding:utf-8 -*-
"""
此文件为各种类型的站点聚类的操作，包括距离近的站点的合并和label之和为0的站点的聚类操作
"""
from process import geneticAlgm
from process import createEntity
import sys
from reinforcement_learning import  r_learning
import schedule

#距离很近，且vehicle_limit相同的站点的聚类
def process_merged_station(stations,merged_station_list,vehicles,map,T):
    res_vehicle_list=[]
    for station in merged_station_list:
        if len(station.binList)==0:
            continue
        merge_list_id = []
        merge_list_id.append(station.binList[0].local_station)
        merge_list_id.append(station.binList[-1].local_station)
        choose_vehicle_num = schedule.choose_vehicle_index(vehicles, station)
        choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
        vehicles[choose_vehicle_num].is_available = False
        if choose_vehicle.id == u"V709":
            print choose_vehicle.id,8
        max_height=r_learning.bin_packing_function(choose_vehicle,station)
        r_learning.delete_packedbins(choose_vehicle,stations)
        while r_learning.is_one_empty(merge_list_id,stations)==False:
            res_vehicle_list.append(choose_vehicle)
            choose_vehicle_num = schedule.choose_vehicle_index(vehicles, station)
            choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
            vehicles[choose_vehicle_num].is_available = False
            if choose_vehicle.id == u"V709":
                print choose_vehicle.id, 9
            max_height = r_learning.bin_packing_function(choose_vehicle, station)
            r_learning.delete_packedbins(choose_vehicle, stations)
            s_id=choose_vehicle.path[-1]
            while max_height < choose_vehicle.length*0.9 and choose_vehicle.used_weight < choose_vehicle.weight*0.9:
                next_s_id, tmp_dis = schedule.next_station(choose_vehicle, s_id, stations, map, T)
                if next_s_id == u"S044":
                    print "fffffffff"
                if next_s_id != "-1" and tmp_dis * choose_vehicle.perPrice < choose_vehicle.startPrice:
                    schedule.add_bin2waste(choose_vehicle, stations[next_s_id])
                    max_height=r_learning.bin_packing_function(choose_vehicle,stations[next_s_id])
                    r_learning.label_station(stations[next_s_id])
                    if stations[next_s_id].is_merged == 1:
                        r_learning.delete_from_merged_station(merged_station_list, stations[next_s_id], choose_vehicle)
                    tmp_weight = stations[next_s_id].weight
                    createEntity.cal_station_area_weight(stations[next_s_id])
                    if tmp_weight == stations[next_s_id].weight:
                        break
                    s_id=next_s_id
                else:
                    break
        if r_learning.is_one_empty(merge_list_id,stations)==True:
            #if len(choose_vehicle.path)>1:
            #    max_height, choose_vehicle = r_learning.merge_packing(choose_vehicle, stations)
            res_vehicle_list.append(choose_vehicle)

    if stations[u"S114"].isEmpty==True:
        print "Empty++++++++"
    return res_vehicle_list

#距离很近，vehicle_limit不同的站点的聚类
def merge_diff_size_stations(vehicles, stations, map, T):
    res_vehicle_list = []
    for s in stations:
        stations[s].is_merged = 0
    for s_1 in map:
        tmp_dis = sys.maxsize
        choose_s = "-1"
        if stations[s_1].isEmpty == True:
            continue
        for s_2 in map[s_1]:
            if s_1 == s_2:
                continue
            if tmp_dis > map[s_1][s_2] and map[s_1][s_2] <= 1000 and stations[s_2].isEmpty == False:# and stations[s_2].label+stations[s_1].label == 0:
                tmp_dis = map[s_1][s_2]
                choose_s = s_2
        if choose_s == "-1":
            continue
        print s_1,choose_s, map[s_1][choose_s]
        merge_station = r_learning.merge_two_station(stations[s_1], stations[choose_s])
        r_learning.label_station(merge_station)

        small_bin = r_learning.cal_small_bin(merge_station)
        large_bin = r_learning.cal_large_bin(merge_station)
        while small_bin > 10 and large_bin > 20:
            choose_vehicle_num = schedule.choose_vehicle_index(vehicles, merge_station)
            choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
            vehicles[choose_vehicle_num].is_available = False
            max_height = r_learning.bin_packing_function(choose_vehicle, merge_station)
            r_learning.delete_packedbins(choose_vehicle, stations)
            choose_vehicle=continue_process(choose_vehicle, stations, merge_station, map, T, max_height)

            res_vehicle_list.append(choose_vehicle)
            small_bin = r_learning.cal_small_bin(merge_station)
            large_bin = r_learning.cal_large_bin(merge_station)

    return res_vehicle_list

#当一个站点的大货数目大于20，小货数目大于10时，先直接派车装货
def process_station(stations,vehicles,map,T):
    res_vehicle_list=[]

    for s in stations:
        choose_station=stations[s]

        small_bin = r_learning.cal_small_bin(choose_station)
        large_bin = r_learning.cal_large_bin(choose_station)
        while small_bin > 10 and large_bin > 20:
            choose_vehicle_num = schedule.choose_vehicle_index(vehicles, choose_station)
            choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
            vehicles[choose_vehicle_num].is_available = False
            max_height = r_learning.bin_packing_function(choose_vehicle, choose_station)
            choose_vehicle=continue_process(choose_vehicle, stations, choose_station, map, T, max_height)

            res_vehicle_list.append(choose_vehicle)
            small_bin = r_learning.cal_small_bin(choose_station)
            large_bin = r_learning.cal_large_bin(choose_station)

    return res_vehicle_list

#label之和为0的站点的合并
def process_merge_by_label_stations(vehicles,stations,map,T,vehicle_limit):
    res_vehicle_list=[]
    small_bin_list=r_learning.get_small_station_id_list(stations,vehicle_limit)
    large_bin_list=r_learning.get_large_station_id_list(stations,vehicle_limit)
    #small_bin_list = random_list(small_bin_list)
    #large_bin_list = random_list(large_bin_list)
    print large_bin_list
    print small_bin_list
    for s_id in large_bin_list:
        choose_station=stations[s_id]
        if choose_station.vehicle_limit >= 9.6:
            large_bin = r_learning.cal_large_bin(choose_station)
            small_bin = r_learning.cal_small_bin(choose_station)
            while small_bin > 10 and large_bin>20:
                choose_vehicle_num = schedule.choose_vehicle_index(vehicles, choose_station)
                choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
                if choose_vehicle.id == u"V709":
                    print "V890",1
                vehicles[choose_vehicle_num].is_available = False
                max_height = r_learning.bin_packing_function(choose_vehicle, choose_station)
                choose_vehicle=continue_process(choose_vehicle, stations, choose_station, map, T, max_height)

                res_vehicle_list.append(choose_vehicle)

                large_bin = r_learning.cal_large_bin(choose_station)
                small_bin = r_learning.cal_small_bin(choose_station)
                if choose_vehicle.id == u"V598":
                    print ("aaaaaa")

    for s_id in small_bin_list:
        choose_station=stations[s_id]

        large_bin = r_learning.cal_large_bin(choose_station)
        small_bin = r_learning.cal_small_bin(choose_station)
        while large_bin > 20 and small_bin>10:
            choose_vehicle_num = schedule.choose_vehicle_index(vehicles, choose_station)
            choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
            if choose_vehicle.id == u"V709":
                print "V890",2,s_id
            vehicles[choose_vehicle_num].is_available = False
            max_height = r_learning.bin_packing_function(choose_vehicle, choose_station)
            choose_vehicle=continue_process(choose_vehicle, stations, choose_station, map, T, max_height)

            res_vehicle_list.append(choose_vehicle)

            large_bin = r_learning.cal_large_bin(choose_station)
            small_bin = r_learning.cal_small_bin(choose_station)
            if choose_vehicle.id == u"V709":
                print choose_vehicle.path

    small_bin_list = r_learning.get_small_station_id_list(stations, vehicle_limit)
    large_bin_list = r_learning.get_large_station_id_list(stations, vehicle_limit)

    for s_id in small_bin_list:
        tmp_dis=sys.maxsize
        choose_id="-1"
        if s_id == u"S045":
            print s_id
        for s_id_2 in large_bin_list:
            if s_id_2 not in map[s_id]:
                continue
            if map[s_id][s_id_2] < tmp_dis:
                tmp_dis=map[s_id][s_id_2]
                choose_id=s_id_2
        if tmp_dis<25000:
            print s_id,choose_id,map[s_id][choose_id]

            merge_station = r_learning.merge_two_station(stations[s_id], stations[choose_id])
            r_learning.label_station(merge_station)
            label=merge_station.label
            choose_station = merge_station

            large_bin = r_learning.cal_large_bin(choose_station)
            small_bin = r_learning.cal_small_bin(choose_station)
            while large_bin > 10 and small_bin > 10:
                choose_vehicle_num = schedule.choose_vehicle_index(vehicles, choose_station)
                choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
                if choose_vehicle.id == u"V890":
                    print "V890", 4
                vehicles[choose_vehicle_num].is_available = False
                max_height = r_learning.bin_packing_function(choose_vehicle, choose_station)
                r_learning.delete_packedbins(choose_vehicle, stations)
                choose_vehicle=continue_process(choose_vehicle, stations, choose_station, map, T, max_height)

                res_vehicle_list.append(choose_vehicle)
                large_bin = r_learning.cal_large_bin(choose_station)
                small_bin = r_learning.cal_small_bin(choose_station)
                if choose_vehicle.id == u"V598":
                    print ("aaaaaa")

    return res_vehicle_list

#聚类label之和为0的中站，大货多的中站也可以和小货多的大战合并
def process_merge_mid_stations(vehicles,stations,map,T):
    res_vehicle_list = []
    vehicle_limit=10
    small_bin_list = r_learning.get_small_station_id_list(stations, vehicle_limit)
    large_bin_list = r_learning.get_large_station_id_list(stations, vehicle_limit)
    #大货多的中站也可以和小货多的大战合并
    small_bin_list_1 = r_learning.get_small_station_id_list(stations, 18)
    #large_bin_list_1 = r_learning.get_large_station_id_list(stations, 18)
    for s in small_bin_list_1:
        small_bin_list.append(s)

    '''
    small_bin_list=[]
    large_bin_list=[]
    small_bin_list.append(u"S114")
    large_bin_list.append(u"S040")
    '''

    #for s in large_bin_list_1:
    #    large_bin_list.append(s)
    print "mid station merge"
    print large_bin_list
    print small_bin_list

    for s_id in large_bin_list:
        choose_station=stations[s_id]
        if choose_station.vehicle_limit >= 9.6:
            large_bin = r_learning.cal_large_bin(choose_station)
            small_bin = r_learning.cal_small_bin(choose_station)
            while small_bin > 10 and large_bin>20:
                choose_vehicle_num = schedule.choose_vehicle_index(vehicles, choose_station)
                choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
                if choose_vehicle.id == u"V709":
                    print "V890",1
                vehicles[choose_vehicle_num].is_available = False
                max_height = r_learning.bin_packing_function(choose_vehicle, choose_station)
                choose_vehicle=continue_process(choose_vehicle, stations, choose_station, map, T, max_height)

                res_vehicle_list.append(choose_vehicle)

                large_bin = r_learning.cal_large_bin(choose_station)
                small_bin = r_learning.cal_small_bin(choose_station)
                if choose_vehicle.id == u"V598":
                    print ("aaaaaa")

    for s_id in small_bin_list:
        choose_station=stations[s_id]

        large_bin = r_learning.cal_large_bin(choose_station)
        small_bin = r_learning.cal_small_bin(choose_station)
        while large_bin > 20 and small_bin>10:
            choose_vehicle_num = schedule.choose_vehicle_index(vehicles, choose_station)
            choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
            if choose_vehicle.id == u"V709":
                print "V890",2,s_id
            vehicles[choose_vehicle_num].is_available = False
            max_height = r_learning.bin_packing_function(choose_vehicle, choose_station)
            choose_vehicle=continue_process(choose_vehicle, stations, choose_station, map, T, max_height)

            res_vehicle_list.append(choose_vehicle)

            large_bin = r_learning.cal_large_bin(choose_station)
            small_bin = r_learning.cal_small_bin(choose_station)
            if choose_vehicle.id == u"V709":
                print choose_vehicle.path

    for s_id in small_bin_list:
        tmp_dis=sys.maxsize
        choose_id="-1"
        if s_id == u"S045":
            print s_id
        for s_id_2 in large_bin_list:
            if s_id_2 not in map[s_id]:
                continue
            if map[s_id][s_id_2] < tmp_dis:
                tmp_dis=map[s_id][s_id_2]
                choose_id=s_id_2
        if tmp_dis<10000:
            print s_id,choose_id,map[s_id][choose_id],"mid"

            merge_station = r_learning.merge_two_station(stations[choose_id], stations[s_id])
            r_learning.label_station(merge_station)
            label=merge_station.label
            choose_station = merge_station

            large_bin = r_learning.cal_large_bin(choose_station)
            small_bin = r_learning.cal_small_bin(choose_station)
            while large_bin > 20 and small_bin > 10:

                choose_vehicle_num = schedule.choose_vehicle_index(vehicles, choose_station)
                choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
                if choose_vehicle.id == u"V890":
                    print "V890", 4
                vehicles[choose_vehicle_num].is_available = False
                max_height = r_learning.bin_packing_function(choose_vehicle, choose_station)
                r_learning.delete_packedbins(choose_vehicle, stations)
                choose_vehicle=continue_process(choose_vehicle, stations, choose_station, map, T, max_height)

                res_vehicle_list.append(choose_vehicle)
                large_bin = r_learning.cal_large_bin(choose_station)
                small_bin = r_learning.cal_small_bin(choose_station)
                if choose_vehicle.id == u"V598":
                    print ("aaaaaa")

    return res_vehicle_list


#车辆装货的最大高度小于车辆高度的90%，继续调度车辆
def continue_process(choose_vehicle,stations,choose_station,map,T,max_height):
    r_learning.get_real_path(choose_vehicle)
    #s_id = choose_station.id
    s_id=choose_vehicle.path[-1]
    flag=0
    while max_height < choose_vehicle.length * 0.9 and choose_vehicle.used_weight < choose_vehicle.weight * 0.9:
        next_s_id, tmp_dis = schedule.next_station(choose_vehicle, s_id, stations, map, T)
        if next_s_id == u"S123":
            print "fffffffff"
        if next_s_id != "-1" and tmp_dis * choose_vehicle.perPrice < choose_vehicle.startPrice:
            flag=1
            schedule.add_bin2waste(choose_vehicle, stations[next_s_id])
            createEntity.cal_station_area_weight(choose_station)
            if stations[next_s_id].weight == 0:
                stations[next_s_id].isEmpty = True

            max_height = r_learning.bin_packing_function(choose_vehicle, stations[next_s_id])
            r_learning.label_station(stations[next_s_id])
            choose_vehicle.usedTime += T[s_id][next_s_id] + stations[next_s_id].loading_time
            tmp_weight = stations[next_s_id].weight
            createEntity.cal_station_area_weight(stations[next_s_id])
            if tmp_weight == stations[next_s_id].weight:
                break
            s_id = next_s_id
        else:
            break
    if flag==1:
        max_height, choose_vehicle = r_learning.merge_packing(choose_vehicle, stations)
    return choose_vehicle

#弃用
def go_to_nearest_station(choose_vehicle,stations,choose_station,map,T):
    s_id=choose_station.id
    next_s_id, tmp_dis = schedule.next_station(choose_vehicle, s_id, stations, map, T)
    if next_s_id == u"S123":
        print "fffffffff"
    if next_s_id != "-1" and tmp_dis * choose_vehicle.perPrice < choose_vehicle.startPrice:
        flag = 1
        schedule.add_bin2waste(choose_vehicle, stations[next_s_id])
        createEntity.cal_station_area_weight(choose_station)
        if stations[next_s_id].weight == 0:
            stations[next_s_id].isEmpty = True

        max_height = r_learning.bin_packing_function(choose_vehicle, stations[next_s_id])
        r_learning.label_station(stations[next_s_id])
        choose_vehicle.usedTime += T[s_id][next_s_id] + stations[next_s_id].loading_time
        tmp_weight = stations[next_s_id].weight
        createEntity.cal_station_area_weight(stations[next_s_id])

    if flag==1:
        max_height, choose_vehicle = r_learning.merge_packing(choose_vehicle, stations)
    return choose_vehicle

#站点聚类的汇总操作，返回结果为使用的车辆信息
def many_merge(vehicles,stations,mst,T):
    res_vehicle_list = []

    # res_vehicle_list1 = process_merge_mid_stations(vehicles, stations, mst, T)
    res_vehicle_list1 = process_merge_by_label_stations(vehicles, stations, mst, T, 18)
    for v in res_vehicle_list1:
        res_vehicle_list.append(v)

    print "Again"
    r_learning.label_stations(stations)
    res_vehicle_list1 = process_merge_by_label_stations(vehicles, stations, mst, T, 18)
    for v in res_vehicle_list1:
        res_vehicle_list.append(v)

    r_learning.label_stations(stations)
    res_vehicle_list1 = process_merge_mid_stations(vehicles, stations, mst, T)
    for v in res_vehicle_list1:
        res_vehicle_list.append(v)

    r_learning.label_stations(stations)
    res_vehicle_list1 = process_merge_mid_stations(vehicles, stations, mst, T)
    for v in res_vehicle_list1:
        res_vehicle_list.append(v)

    print "BEGIN NEAREST+++++++++++++"
    merge_station_list = r_learning.merge_nearest_stations(stations, mst)
    res_vehicle_list1 = process_merged_station(stations, merge_station_list, vehicles, mst, T)
    for v in res_vehicle_list1:
        if v.id == u"V709":
            print "V709", 5
        res_vehicle_list.append(v)

    print "NEAREST -------------"
    merge_station_list = r_learning.merge_nearest_stations(stations, mst)
    res_vehicle_list1 = process_merged_station(stations, merge_station_list, vehicles, mst, T)
    for v in res_vehicle_list1:
        if v.id == u"V709":
            print "V709", 6
        res_vehicle_list.append(v)
    # res_vehicle_list=process_station(stations,vehicles)

    print "QUZHENG ++++++++++"
    r_learning.label_stations(stations)
    res_vehicle_list1 = process_station(stations, vehicles, mst, T)
    for v in res_vehicle_list1:
        res_vehicle_list.append(v)

    print "DIFF SIZE+++++++++="
    r_learning.label_stations(stations)
    res_vehicle_list1 = merge_diff_size_stations(vehicles, stations, mst, T)
    for v in res_vehicle_list1:
        res_vehicle_list.append(v)

    return res_vehicle_list
