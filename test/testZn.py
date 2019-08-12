from process import geneticAlgm
from entity import entity
from process import createEntity
from process import skyLine
from createJson import createResult
import  sys

def choose_vehicle_index(vehicle_list,station):

    i = len(vehicle_list) - 1
    while i>0:
        if vehicle_list[i].length <= station.vehicle_limit and vehicle_list[i].is_available == True:
            return i
        i = i-1

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
        while choose_station.weight!=0:
            choose_vehicle_num = choose_vehicle_index(vehicles, choose_station)
            choose_vehicle = geneticAlgm.create_new_vehicle(vehicles[choose_vehicle_num])
            res_vehicle_list.append(choose_vehicle)
            #choose_vehicle.path.append(s_id)
            choose_vehicle.usedTime = choose_vehicle.usedTime + choose_station.loading_time
            vehicles[choose_vehicle_num].is_available = False

            max_height = skyLine.skyline(choose_vehicle, choose_station)
            createEntity.cal_station_area_weight(choose_station)

        if choose_station.weight == 0:
            if max_height < choose_vehicle.length:
                nobor_list=mst[s_id]
                tmp_dis=sys.maxsize
                next_s_id ="-1"
                for n_s in nobor_list:
                    if mst[s_id][n_s] < tmp_dis and stations[n_s].isEmpty == False and n_s != s_id and choose_vehicle.usedTime+T[s_id][n_s]<=600:
                        tmp_dis = mst[s_id][n_s]
                        next_s_id = n_s
                if next_s_id != "-1" and tmp_dis * choose_vehicle.perPrice < choose_vehicle.startPrice:
                    skyLine.skyline(choose_vehicle,stations[next_s_id])
                    #choose_vehicle.path.append(next_s_id)
                    choose_vehicle.usedTime = choose_vehicle.usedTime + T[s_id][n_s] + choose_station.loading_time

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

        if choose_station.weight == 0:
            if max_height < choose_vehicle.length:
                nobor_list=mst[s_id]
                tmp_dis=sys.maxsize
                next_s_id ="-1"
                for n_s in nobor_list:
                    if mst[s_id][n_s] < tmp_dis and stations[n_s].isEmpty == False:
                        tmp_dis = mst[s_id][n_s]
                        next_s_id = n_s
                if next_s_id != "-1" and n_s != s_id and tmp_dis * choose_vehicle.perPrice < choose_vehicle.startPrice:
                    skyLine.skyline(choose_vehicle,stations[next_s_id])
                    #choose_vehicle.path.append(next_s_id)

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

        if choose_station.weight == 0:
            if max_height < choose_vehicle.length:
                nobor_list=mst[s_id]
                tmp_dis=sys.maxsize
                next_s_id ="-1"
                for n_s in nobor_list:
                    if mst[s_id][n_s] < tmp_dis and stations[n_s].isEmpty == False:
                        tmp_dis = mst[s_id][n_s]
                        next_s_id = n_s
                if next_s_id != "-1" and n_s != s_id and tmp_dis * choose_vehicle.perPrice < choose_vehicle.startPrice:
                    skyLine.skyline(choose_vehicle,stations[next_s_id])
                    #choose_vehicle.path.append(next_s_id)
    return res_vehicle_list


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

    print(len(mst))
    print(len(vehicles[2].bin_list))
    print()
    print(len(stations["S012"].binList))

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
    vehicle_list = schedule_mst(stations,vehicles,station_list1,station_list2,station_list3,mst,T)
    # gene,cost,rate = genetic(vehicles,stations,map,time,200)
    #vehicle_list = geneticAlgm.schedule_gene(gene, vehicles, stations, map, time)
    total_cost, total_rate = geneticAlgm.cal_final_result(vehicle_list, map)
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
    for v in vehicle_list:
        len_2 = len_2 + len(v.bin_list)

    print("len_1 : ", len_1, "len_2 : ", len_2)

    createResult.createJson(path, vehicle_list)

    # tmp_area=0.0
    # for b in vehicles[2].bin_list:
    #    tmp_area = round(tmp_area+b.length*b.width,5)
    # print(tmp_area," ",round(vehicles[2].length*vehicles[2].width,5))

# createEntity.draw_rect(vehicles[2],tmp_area)

myTest()