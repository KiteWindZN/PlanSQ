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
            if max_height == 5.6:
                print ("aaaa")
            while max_height < choose_vehicle.length*0.85:

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

            while max_height < choose_vehicle.length*0.85:

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

            while max_height < choose_vehicle.length*0.9:

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
                if mst[s_id][n_s] < tmp_dis and stations[n_s].isEmpty == False and n_s != s_id and stations[n_s].vehicle_limit >= choose_vehicle.length:
                    tmp_dis = mst[s_id][n_s]
                    next_s_id = n_s
            dis_cost = tmp_dis * choose_vehicle.perPrice

            if next_s_id == "-1" or dis_cost > choose_vehicle.startPrice:
                continue

            while max_height < choose_vehicle.length*0.9:

                nobor_list = mst[s_id]
                tmp_dis = sys.maxsize
                next_s_id = "-1"
                for n_s in nobor_list:
                    if mst[s_id][n_s] < tmp_dis and stations[n_s].isEmpty == False and stations[n_s].vehicle_limit >= choose_vehicle.length:
                        tmp_dis = mst[s_id][n_s]
                        next_s_id = n_s
                if next_s_id != "-1" and next_s_id != s_id and tmp_dis * choose_vehicle.perPrice < choose_vehicle.startPrice:
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
                    if mst[s_id][n_s] < tmp_dis and stations[n_s].isEmpty == False and n_s != s_id:
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

            while max_height < choose_vehicle.length*0.9:

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
                if mst[s_id][n_s] < tmp_dis and stations[n_s].isEmpty == False and n_s != s_id and stations[n_s].vehicle_limit >= choose_vehicle.length:
                    tmp_dis = mst[s_id][n_s]
                    next_s_id = n_s
            dis_cost = tmp_dis * choose_vehicle.perPrice

            if next_s_id == "-1" or dis_cost > choose_vehicle.startPrice:
                continue
            avg_h=avg_height(choose_vehicle.lines)
            while avg_h < choose_vehicle.length*0.9:
                nobor_list = mst[s_id]
                tmp_dis = sys.maxsize
                next_s_id = "-1"
                for n_s in nobor_list:
                    if mst[s_id][n_s] < tmp_dis and stations[n_s].isEmpty == False and stations[n_s].vehicle_limit >= choose_vehicle.length:
                        tmp_dis = mst[s_id][n_s]
                        next_s_id = n_s
                if next_s_id != "-1" and next_s_id != s_id and tmp_dis * choose_vehicle.perPrice < choose_vehicle.startPrice and choose_vehicle.usedTime + T[s_id][next_s_id] + stations[next_s_id].loading_time <= 600:
                    max_height=skyLine.skyline(choose_vehicle, stations[next_s_id])
                    s_id=next_s_id
                else:
                    break
                avg_h = avg_height(choose_vehicle.lines)
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
                    if mst[s_id][n_s] < tmp_dis and stations[n_s].isEmpty == False and n_s != s_id:
                        tmp_dis = mst[s_id][n_s]
                        next_s_id = n_s
                dis_cost = tmp_dis * choose_vehicle.perPrice
                if next_s_id != "-1" and next_s_id != s_id and dis_cost < choose_vehicle.startPrice:
                    max_height = skyLine.skyline(choose_vehicle, stations[next_s_id])
                    # choose_vehicle.path.append(next_s_id)
                    s_id = next_s_id
                else:
                    break
            '''
    return res_vehicle_list


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
    bins = createEntity.createBin(path + "bin.json", stations)
    vehicles = createEntity.createVehicle(path + "vehicle.json")
    mst, T = createEntity.createMST(map, time)
    # createEntity.deleteVehicle(vehicles, maxLimit)

    # map,time = createEntity.floyd(map,time)
    # print()
    # print(len(stations["S045"].binList))

    # max_height=skyLine.skyline(vehicles[998],stations["S045"])

    # print()
    # print(max_height)

    # print()
    # print(len(vehicles[998].bin_list))
    # print()
    # print(len(stations["S012"].binList))

    #print(len(mst))
    #print(len(vehicles[2].bin_list))
    #print()
    #print(len(stations["S012"].binList))

    path = createResult.createFileJson()


    # createResult.createJson(path, vehicle_list)
    # createEntity.update_stations(stations)

    # tmp_area=0.0
    # for b in vehicles[2].bin_list:
    #    tmp_area = round(tmp_area+b.length*b.width,5)
    # print(tmp_area," ",round(vehicles[2].length*vehicles[2].width,5))

    #  createEntity.draw_rect(vehicles[2],tmp_area)

    gene = geneticAlgm.create_gene_station(stations)
    # gene=["S171","S164", "S104","S087","S008","S200","S003","S188","S099","S167", "S038","S132","S035","S127","S066","S076","S010","S169","S027","S170","S079"]
    # gene=["S163"]

    # print len(gene)
    station_list1,station_list2,station_list3=createEntity.divide_stations(stations)
    station_list1=random_list(station_list1)
    station_list2 = random_list(station_list2)
    station_list3 = random_list(station_list3)
    #print(len(station_list1),len(station_list2),len(station_list3))
    #vehicle_list = schedule_mst(stations,vehicles,station_list1,station_list2,station_list3,map,time)
    #vehicle_list = schedule(stations,vehicles,map,time)
    #geneticAlgm.check_vehicle_list(vehicle_list)
    vehicle_list1=schedule_mst(stations,vehicles,station_list3,station_list1,station_list2,map,time)
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

    createResult.createJson(path, vehicle_list1)


    for i in range(len(vehicle_list1)):
        tmp_area = 0.0
        v=vehicle_list1[i]
        for b in v.bin_list:
            tmp_area = round(tmp_area+b.length*b.width,5)
        if tmp_area/(v.length*v.width) < 0.70:
            print(v.id," ",tmp_area," ",round(v.length*v.width,5))

            createEntity.draw_rect(v,tmp_area)

myTest()