from process import geneticAlgm
from entity import entity
from process import createEntity
from process import skyLine
from createJson import createResult
import sys
from process import multipul_skyline
import random
def choose_vehicle_index(vehicle_list,station):
    weight=station.weight
    area=station.area
    res=-1
    #for i in range(len(vehicle_list)):
    #    vehicle_area = vehicle_list[i].length * vehicle_list[i].width
    #    if vehicle_list[i].length <= station.vehicle_limit and vehicle_list[i].is_available == True and vehicle_list[i].weight*0.8 >= weight and vehicle_area *0.8 >= area:
    #        res=i
    #        break
    #if res!=-1:
    #    return res
    i = len(vehicle_list) - 1
    while i>0:
        if vehicle_list[i].length <= station.vehicle_limit and vehicle_list[i].is_available == True:
            res=i
            break
        i = i-1
    return  res

def schedule_mst(stations,vehicles,station_list1,station_list2,station_list3,mst,T):
    res_vehicle_list=[]
    for s_id in station_list1:
        choose_station=stations[s_id]
        if choose_station.isEmpty==True:
            continue
        choose_vehicle_num=choose_vehicle_index(vehicles,choose_station)
        choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
        res_vehicle_list.append(choose_vehicle)
        #choose_vehicle.path.append(s_id)
        choose_vehicle.usedTime = choose_vehicle.usedTime + choose_station.loading_time
        vehicles[choose_vehicle_num].is_available = False

        max_height = skyLine.skyline(choose_vehicle,choose_station)
        createEntity.cal_station_area_weight(choose_station)
        if choose_station.id == u"S051":
            print "aaa"
        while choose_station.weight!=0:

            choose_vehicle_num = choose_vehicle_index(vehicles, choose_station)
            choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
            res_vehicle_list.append(choose_vehicle)
            #choose_vehicle.path.append(s_id)
            choose_vehicle.usedTime = choose_vehicle.usedTime + choose_station.loading_time
            vehicles[choose_vehicle_num].is_available = False

            max_height = skyLine.skyline(choose_vehicle, choose_station)


            createEntity.cal_station_area_weight(choose_station)

            while max_height < choose_vehicle.length*0.9 and choose_vehicle.used_weight < choose_vehicle.weight*0.9:

                nobor_list = mst[s_id]
                tmp_dis = sys.maxsize
                next_s_id = "-1"
                for n_s in nobor_list:
                    if mst[s_id][n_s] < tmp_dis and stations[n_s].isEmpty == False and n_s != s_id and stations[n_s].vehicle_limit >= choose_vehicle.length:
                        tmp_dis = mst[s_id][n_s]
                        next_s_id = n_s
                if next_s_id != "-1" and next_s_id != s_id and tmp_dis * choose_vehicle.perPrice < choose_vehicle.startPrice:
                    max_height=skyLine.skyline(choose_vehicle, stations[next_s_id])
                    s_id=next_s_id
                else:
                    break

        if choose_station.weight == 0:

            nobor_list = mst[s_id]
            tmp_dis = sys.maxsize
            next_s_id = "-1"
            for n_s in nobor_list:
                if mst[s_id][n_s] < tmp_dis and stations[n_s].isEmpty == False and n_s != s_id:
                    tmp_dis = mst[s_id][n_s]
                    next_s_id = n_s
            dis_cost = tmp_dis * choose_vehicle.perPrice

            if next_s_id == "-1" or dis_cost > choose_vehicle.startPrice:
                continue

            while max_height < choose_vehicle.length*0.9 and choose_vehicle.used_weight < choose_vehicle.weight*0.9:

                nobor_list = mst[s_id]
                tmp_dis = sys.maxsize
                next_s_id = "-1"
                for n_s in nobor_list:
                    if mst[s_id][n_s] < tmp_dis and stations[n_s].isEmpty == False and n_s != s_id and stations[n_s].vehicle_limit >= choose_vehicle.length:
                        tmp_dis = mst[s_id][n_s]
                        next_s_id = n_s
                dis_cost = tmp_dis * choose_vehicle.perPrice
                if next_s_id != "-1" and next_s_id!= s_id and dis_cost < choose_vehicle.startPrice:
                    max_height=skyLine.skyline(choose_vehicle, stations[next_s_id])
                    # choose_vehicle.path.append(next_s_id)
                    s_id=next_s_id
                else:
                    break

            '''
            tmp_area = 0.0
            choose_vehicle_area = choose_vehicle.length * choose_vehicle.width
            for b in choose_vehicle.bin_list:
                tmp_area = round(tmp_area + b.length * b.width, 5)
            if tmp_area / (choose_vehicle_area) < 0.8:
                for b in choose_vehicle.bin_list:
                    b.pointList = []
                    stations[b.local_station].binList.append(b)

                station_list=[]
                for s in choose_vehicle.path:
                    ss=stations[s]
                    station_list.append(ss)
                    ss.isEmpty = False
                    createEntity.cal_station_area_weight(ss)
                choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
                max_height=multipul_skyline.multi_skyline(choose_vehicle,station_list,stations)

            s_id = choose_vehicle.path[-1]
            while max_height < choose_vehicle.length*0.9:

                nobor_list = mst[s_id]
                tmp_dis = sys.maxsize
                next_s_id = "-1"
                for n_s in nobor_list:
                    if mst[s_id][n_s] < tmp_dis and stations[n_s].isEmpty == False and n_s != s_id:
                        tmp_dis = mst[s_id][n_s]
                        next_s_id = n_s
                dis_cost = tmp_dis * choose_vehicle.perPrice
                if next_s_id != "-1" and next_s_id!= s_id and dis_cost < choose_vehicle.startPrice:
                    max_height=skyLine.skyline(choose_vehicle, stations[next_s_id])
                    # choose_vehicle.path.append(next_s_id)
                    s_id=next_s_id
            '''

    for s_id in station_list2:
        choose_station=stations[s_id]
        if choose_station.isEmpty==True:
            continue
        choose_vehicle_num=choose_vehicle_index(vehicles,choose_station)
        choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
        res_vehicle_list.append(choose_vehicle)
        #choose_vehicle.path.append(s_id)
        vehicles[choose_vehicle_num].is_available = False

        max_height = skyLine.skyline(choose_vehicle,choose_station)
        createEntity.cal_station_area_weight(choose_station)
        while choose_station.weight!=0:

            choose_vehicle_num = choose_vehicle_index(vehicles, choose_station)
            choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
            res_vehicle_list.append(choose_vehicle)
            #choose_vehicle.path.append(s_id)
            vehicles[choose_vehicle_num].is_available = False

            max_height = skyLine.skyline(choose_vehicle, choose_station)
            createEntity.cal_station_area_weight(choose_station)

            while max_height < choose_vehicle.length*0.9 and choose_vehicle.used_weight < choose_vehicle.weight*0.9:
                next_s_id, tmp_dis = next_station(choose_vehicle, s_id, stations, mst, T)

                if next_s_id != "-1" and next_s_id != s_id and tmp_dis * choose_vehicle.perPrice < choose_vehicle.startPrice:
                    max_height=skyLine.skyline(choose_vehicle, stations[next_s_id])
                    s_id=next_s_id
                else:
                    break

        if choose_station.weight == 0:

            nobor_list = mst[s_id]
            tmp_dis = sys.maxsize
            next_s_id = "-1"
            for n_s in nobor_list:
                if mst[s_id][n_s] < tmp_dis and stations[n_s].isEmpty == False and n_s != s_id and stations[n_s].vehicle_limit >= choose_vehicle.length:
                    tmp_dis = mst[s_id][n_s]
                    next_s_id = n_s
            dis_cost = tmp_dis * choose_vehicle.perPrice

            if next_s_id == "-1" or dis_cost > choose_vehicle.startPrice:
                continue

            while max_height < choose_vehicle.length*0.9 and choose_vehicle.used_weight < choose_vehicle.weight*0.9:
                next_s_id, tmp_dis = next_station(choose_vehicle, s_id, stations, mst, T)
                if next_s_id != "-1" and tmp_dis * choose_vehicle.perPrice < choose_vehicle.startPrice:
                    max_height=skyLine.skyline(choose_vehicle, stations[next_s_id])
                    s_id=next_s_id
                else:
                    break
            '''
            tmp_area = 0.0
            choose_vehicle_area = choose_vehicle.length * choose_vehicle.width
            for b in choose_vehicle.bin_list:
                tmp_area = round(tmp_area + b.length * b.width, 5)
            if tmp_area / (choose_vehicle_area) < 0.8:
                for b in choose_vehicle.bin_list:
                    b.pointList = []
                    stations[b.local_station].binList.append(b)

                station_list = []
                for s in choose_vehicle.path:
                    ss = stations[s]
                    station_list.append(ss)
                    ss.isEmpty = False
                    createEntity.cal_station_area_weight(ss)
                choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
                max_height = multipul_skyline.multi_skyline(choose_vehicle, station_list, stations)

            s_id = choose_vehicle.path[-1]
            while max_height < choose_vehicle.length * 0.9:

                nobor_list = mst[s_id]
                tmp_dis = sys.maxsize
                next_s_id = "-1"
                for n_s in nobor_list:
                    if mst[s_id][n_s] < tmp_dis and stations[n_s].isEmpty == False and n_s != s_id and stations[n_s].vehicle_limit >= choose_vehicle.length:
                        tmp_dis = mst[s_id][n_s]
                        next_s_id = n_s
                dis_cost = tmp_dis * choose_vehicle.perPrice
                if next_s_id != "-1" and next_s_id != s_id and dis_cost < choose_vehicle.startPrice:
                    max_height = skyLine.skyline(choose_vehicle, stations[next_s_id])
                    # choose_vehicle.path.append(next_s_id)
                    s_id = next_s_id
            '''
    for s_id in station_list3:
        choose_station=stations[s_id]
        if choose_station.isEmpty==True:
            continue
        choose_vehicle_num=choose_vehicle_index(vehicles,choose_station)
        choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
        res_vehicle_list.append(choose_vehicle)
        vehicles[choose_vehicle_num].is_available = False

        max_height = skyLine.skyline(choose_vehicle,choose_station)
        createEntity.cal_station_area_weight(choose_station)
        while choose_station.weight!=0:

            choose_vehicle_num = choose_vehicle_index(vehicles, choose_station)
            choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
            res_vehicle_list.append(choose_vehicle)
            vehicles[choose_vehicle_num].is_available = False

            max_height = skyLine.skyline(choose_vehicle, choose_station)
            createEntity.cal_station_area_weight(choose_station)

            while max_height < choose_vehicle.length*0.9 and choose_vehicle.used_weight < choose_vehicle.weight*0.9:
                next_s_id, tmp_dis = next_station(choose_vehicle, s_id, stations, mst, T)

                if next_s_id != "-1" and tmp_dis * choose_vehicle.perPrice < choose_vehicle.startPrice:
                    max_height=skyLine.skyline(choose_vehicle, stations[next_s_id])
                    choose_vehicle.usedTime += T[s_id][next_s_id] + stations[next_s_id].loading_time
                    s_id=next_s_id
                else:
                    break

        max_height = choose_vehicle.max_height
        if choose_station.weight == 0:

            avg_h=avg_height(choose_vehicle.lines)
            while max_height < choose_vehicle.length*0.9 and choose_vehicle.used_weight < choose_vehicle.weight*0.9:
                next_s_id, tmp_dis = next_station(choose_vehicle, s_id, stations, mst, T)

                if next_s_id != "-1" and tmp_dis * choose_vehicle.perPrice < choose_vehicle.startPrice:
                    max_height=skyLine.skyline(choose_vehicle, stations[next_s_id])
                    choose_vehicle.usedTime += T[s_id][next_s_id] + stations[next_s_id].loading_time
                    s_id=next_s_id
                else:
                    break
                avg_h = avg_height(choose_vehicle.lines)
            '''
            tmp_area = 0.0
            choose_vehicle_area = choose_vehicle.length * choose_vehicle.width
            for b in choose_vehicle.bin_list:
                tmp_area = round(tmp_area + b.length * b.width, 5)
            if tmp_area / (choose_vehicle_area) < 0.85:
                for b in choose_vehicle.bin_list:
                    b.pointList = []
                    stations[b.local_station].binList.append(b)

                station_list = []
                path=[]
                for p in choose_vehicle.path:
                    path.append(p)

                for s in choose_vehicle.path:
                    ss = stations[s]
                    station_list.append(ss)
                    ss.isEmpty = False
                    createEntity.cal_station_area_weight(ss)
                choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
                max_height = multipul_skyline.multi_skyline(choose_vehicle, station_list, stations)
                print("dddd")
                choose_vehicle.path=[]
                choose_vehicle.path=path
            s_id = choose_vehicle.path[-1]
            while max_height < choose_vehicle.length * 0.9:
                next_s_id,tmp_dis=next_station(choose_vehicle, s_id, stations, mst,T)
                dis_cost = tmp_dis * choose_vehicle.perPrice
                if next_s_id != "-1" and dis_cost < choose_vehicle.startPrice:
                    max_height = skyLine.skyline(choose_vehicle, stations[next_s_id])
                    s_id = next_s_id
                else:
                    break
            '''
    return res_vehicle_list


def next_station(vehicle,s_id,stations,map,time):
    nobor_list = map[s_id]
    tmp_dis = sys.maxsize
    next_s_id = "-1"
    for n_s in nobor_list:
        if map[s_id][n_s] < tmp_dis and n_s != s_id and stations[n_s].isEmpty == False and stations[n_s].vehicle_limit >= vehicle.length\
                and vehicle.usedTime+time[s_id][n_s] + stations[n_s].loading_time <= 600:
            tmp_dis = map[s_id][n_s]
            next_s_id = n_s
    return next_s_id,tmp_dis


def schedule(stations,vehicles,map,time):
    vehicle_list=[]
    for s in stations:
        choose_station = stations[s]
        if choose_station.isEmpty == True:
            continue
        choose_vehicle_num=choose_vehicle_index(vehicles,choose_station)
        choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
        max_height = skyLine.skyline(choose_vehicle,choose_station)
        createEntity.cal_station_area_weight(choose_station)
        while choose_station.weight!=0:
            vehicles[choose_vehicle_num].is_available = False
            vehicle_list.append(choose_vehicle)
            choose_vehicle_num = choose_vehicle_index(vehicles, choose_station)
            choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
            max_height = skyLine.skyline(choose_vehicle, choose_station)
            createEntity.cal_station_area_weight(choose_station)

            tmp_area = 0.0
            choose_vehicle_area = choose_vehicle.length * choose_vehicle.width
            for b in choose_vehicle.bin_list:
                tmp_area = round(tmp_area + b.length * b.width, 5)
            if tmp_area / (choose_vehicle_area) < 0.8:
                #    print(choose_vehicle.id, " ", tmp_area, " ", round(choose_vehicle_area, 5))
                # if max_height<choose_vehicle.length*0.85:
                for b in choose_vehicle.bin_list:
                    b.pointList = []
                    choose_station.binList.append(b)
                choose_vehicle.bin_list=[]
                #choose_vehicle.lines=[]
                choose_station.isEmpty = False
                createEntity.cal_station_area_weight(choose_station)
                break

            '''
            tmp_area = 0.0
            choose_vehicle_area = choose_vehicle.length * choose_vehicle.width
            for b in choose_vehicle.bin_list:
                tmp_area = round(tmp_area + b.length * b.width, 5)
            #if tmp_area / (choose_vehicle_area) < 0.7:
            if max_height < choose_vehicle.length *0.8:

                for b in choose_vehicle.bin_list:
                    b.pointList = []
                    choose_station.binList.append(b)
                choose_station.isEmpty=False
                createEntity.cal_station_area_weight(choose_station)
               
                choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
                station_list=[]
                station_list.append(choose_station)
                s_id=s
                nobor_list = map[s_id]
                tmp_dis = sys.maxsize
                next_s_id = "-1"
                for n_s in nobor_list:
                    if map[s_id][n_s] < tmp_dis and s_id != n_s and stations[n_s].isEmpty == False:
                        tmp_dis = map[s_id][n_s]
                        next_s_id = n_s
                if next_s_id != "-1" and next_s_id != s_id and tmp_dis * choose_vehicle.perPrice < choose_vehicle.startPrice and choose_vehicle.usedTime + \
                        time[s_id][next_s_id] + stations[next_s_id].loading_time <= 600:

                    station_list.append(stations[next_s_id])

                    max_height = multipul_skyline.multi_skyline(choose_vehicle, station_list, stations)

                    #max_height = skyLine.skyline(choose_vehicle, stations[next_s_id])
                
            else:
                createEntity.cal_station_area_weight(choose_station)
                if choose_station.isEmpty == True:
                    break
                choose_vehicle_num = choose_vehicle_index(vehicles, choose_station)
                choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
                max_height = skyLine.skyline(choose_vehicle, choose_station)
            '''


        tmp_area = 0.0
        choose_vehicle_area=choose_vehicle.length * choose_vehicle.width
        for b in choose_vehicle.bin_list:
            tmp_area = round(tmp_area + b.length * b.width, 5)
        if tmp_area / (choose_vehicle_area) <0.8:
        #    print(choose_vehicle.id, " ", tmp_area, " ", round(choose_vehicle_area, 5))
        #if max_height<choose_vehicle.length*0.85:
            for b in choose_vehicle.bin_list:
                b.pointList=[]
                choose_station.binList.append(b)

            choose_station.isEmpty=False
            createEntity.cal_station_area_weight(choose_station)

        else:
            vehicles[choose_vehicle_num].is_available = False
            #createEntity.cal_station_area_weight(choose_station)
            vehicle_list.append(choose_vehicle)
    return vehicle_list


def avg_height(lines):
    avg_h=0
    for l in lines:
        avg_h += l.height
    avg_h = avg_h / len(lines)

    return avg_h


def pick_bins(vehicle_list,stations,map,time):
    for v in vehicle_list:
        if v.max_height < v.length * 0.4:
            for v1 in vehicle_list:
                if v1.id == v.id:
                    continue
                #if v1.max_height > v1.length *0.9:
                #    continue
                s_id = v1.path[-1]
                if v1.usedTime + time[s_id][v.path[0]] +stations[v.path[0]].loading_time <= 600 and map[s_id][v.path[0]] * v1.perPrice < v.startPrice and v1.length <= stations[v.path[0]].vehicle_limit:
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
                        tmp_bin.pointList.append(b.pointList[0])
                        tmp_bin.pointList.append(b.pointList[1])
                        tmp_bin.pointList.append(b.pointList[2])
                        tmp_bin.pointList.append(b.pointList[3])
                        tmp_vehicle.bin_list.append(tmp_bin)
                        tmp_vehicle.station_bin[b.local_station].append(tmp_bin)
                    for l in v1.lines:
                        #tmp_line = entity.Line(entity.Point(l.start.x,l.start.y),entity.Point(l.end.x, l.end.y),l.left_height,l.right_height)
                        tmp_vehicle.lines.append(entity.Line(entity.Point(l.start.x,l.start.y),entity.Point(l.end.x, l.end.y),l.left_height,l.right_height))
                    skyLine.skyline(tmp_vehicle,tmp_station)
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
        if v.length == 17.5 and v.max_height<= 9.6:
            for v2 in vehicles:
                v1=geneticAlgm.create_new_vehicle(v2)
                if v2.is_available == True:
                    tmp_station = entity.Station(v.path[0], v1.length, 0)
                    for b in v.bin_list:
                        tmp_bin=entity.Bin(b.id,b.length,b.width,b.weight,b.local_station)
                        tmp_station.binList.append(tmp_bin)
                        tmp_station.isEmpty=False
                    skyLine.skyline(v1,tmp_station)
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
                    skyLine.skyline(v1,tmp_station)
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

def random_list(list):
    res_list=[]
    while len(list)>0:
        i=random.randint(0,len(list)-1)
        res_list.append(list[i])
        list.remove(list[i])
    return res_list

def myTest():
    path = "../dataset/month3/"

    print("enter")
    map, time = createEntity.createMap(path + "matrix.json")
    stations, maxLimit = createEntity.createStation(path + "station.json")
    #station_total=stations["S001"]

    bins = createEntity.createBin(path + "bin.json", stations)
    #station_total.binList=bins
    station_dic={}
    #station_dic["S001"]=station_total
    vehicles = createEntity.createVehicle(path + "vehicle.json")
    mst, T = createEntity.createMST(map, time)
    # createEntity.deleteVehicle(vehicles, maxLimit)

    # map,time = createEntity.floyd(map,time)



    #gene = geneticAlgm.create_gene_station(stations)

    # print len(gene)
    station_list1,station_list2,station_list3=createEntity.divide_stations(stations)
    #station_list1=random_list(station_list1)
    station_list2 = random_list(station_list2)


    print (station_list1)
    print (station_list2)
    print (station_list3)
    #print(len(station_list1),len(station_list2),len(station_list3))
    #vehicle_list = schedule_mst(stations,vehicles,station_list1,station_list2,station_list3,map,time)
    #vehicle_list = schedule(stations,vehicles,map,time)
    #geneticAlgm.check_vehicle_list(vehicle_list)
    vehicle_list1=schedule_mst(stations,vehicles,station_list3,station_list1,station_list2,map,time)

    pick_bins(vehicle_list1,stations,map,time)
    change_vehicle(vehicle_list1, vehicles)
    geneticAlgm.check_vehicle_list(vehicle_list1)
    #gene,cost,rate = genetic(vehicles,stations,map,time,200)
    #vehicle_list = geneticAlgm.schedule_gene(gene, vehicles, stations, map, time)
    #total_cost, total_rate = geneticAlgm.cal_final_result(vehicle_list, map)
    #print(total_cost, total_rate)
    total_cost, total_rate = geneticAlgm.cal_final_result(vehicle_list1, map)
    print(total_cost, total_rate)
    # print (total_cost , total_rate)
    # path = createResult.createFileJson()

    # status=is_finashed(stations)
    # print(status)

    # for i in range(len(gene)):
    #    if i+1 < len(gene):
    #        print(map[str(gene[i])][str(gene[i+1])])

    len_1 = len(bins)
    len_2 = 0
    for v in vehicle_list1:
        len_2 = len_2 + len(v.bin_list)

    print("len_1 : ", len_1, "len_2 : ", len_2)
    path = createResult.createFileJson(total_cost)
    createResult.createJson(path, vehicle_list1)


    for i in range(len(vehicle_list1)):
        tmp_area = 0.0
        v=vehicle_list1[i]
        for b in v.bin_list:
            tmp_area = round(tmp_area+b.length*b.width,5)
        if tmp_area/(v.length*v.width) < 0.7:
            print(v.id," ",tmp_area," ",round(v.length*v.width,5))

            #createEntity.draw_rect(v,tmp_area)

for i in range(20):
    myTest()