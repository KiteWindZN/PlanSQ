from process import geneticAlgm
from process import createEntity
from createJson import createResult
from reinforcement_learning import r_learning
from schedule import merge_stations
from schedule import schedule
from schedule import final_process
import random


def random_list(list):
    res_list=[]
    while len(list)>0:
        i=random.randint(0,len(list)-1)
        res_list.append(list[i])
        list.remove(list[i])
    return res_list


def my_test(vehicles,stations,map,time,res_vehicle_list):

    station_list1,station_list2,station_list3=createEntity.divide_stations(stations)
    station_list3=random_list(station_list3)
    station_list1 = random_list(station_list1)
    station_list2 = random_list(station_list2)

    '''
    station_list1=[u'S122', u'S033', u'S190', u'S051', u'S069', u'S078', u'S103', u'S021', u'S036', u'S002', u'S028', u'S059', u'S108', u'S175', u'S127', u'S208', u'S057', u'S178', u'S072', u'S100', u'S094', u'S012', u'S160', u'S215', u'S129', u'S176']
    station_list2=[u'S044',u'S034', u'S037', u'S031', u'S032', u'S040', u'S043', u'S042',  u'S135', u'S134', u'S136', u'S133', u'S019', u'S014', u'S015', u'S091', u'S096', u'S095', u'S143', u'S144', u'S148', u'S149', u'S087', u'S086', u'S081', u'S152', u'S159', u'S158', u'S003', u'S166', u'S167', u'S164', u'S165', u'S161', u'S105', u'S107', u'S186', u'S187', u'S188', u'S070', u'S074', u'S076', u'S173', u'S177', u'S204', u'S119', u'S118', u'S115', u'S112', u'S195', u'S191', u'S210', u'S198', u'S063', u'S067', u'S068', u'S123', u'S125', u'S055', u'S052', u'S053']
    station_list3=[u'S008',u'S058', u'S102', u'S097', u'S206', u'S065', u'S113', u'S207', u'S039', u'S189', u'S128', u'S027', u'S170', u'S050', u'S005', u'S174', u'S017', u'S046', u'S209', u'S138', u'S183', u'S041', u'S184', u'S016', u'S205', u'S106', u'S201', u'S061', u'S172', u'S010', u'S075', u'S156', u'S079', u'S080', u'S151', u'S035', u'S192',  u'S109', u'S098', u'S085', u'S121', u'S194', u'S132', u'S162', u'S126', u'S089', u'S142', u'S131', u'S199', u'S157', u'S146', u'S203', u'S200', u'S193', u'S214', u'S116', u'S001', u'S213', u'S024', u'S062', u'S026', u'S084', u'S150', u'S147', u'S130', u'S038', u'S077', u'S163', u'S029', u'S009', u'S139', u'S047', u'S197', u'S004', u'S110', u'S101', u'S082', u'S049', u'S018', u'S141', u'S137', u'S020', u'S071', u'S154', u'S169', u'S013', u'S007', u'S006', u'S212', u'S022', u'S179', u'S171', u'S185', u'S099', u'S011', u'S114', u'S030', u'S025', u'S056', u'S093', u'S153', u'S111', u'S120', u'S155', u'S196', u'S092', u'S023', u'S182', u'S140', u'S088', u'S181', u'S083', u'S104', u'S211', u'S064', u'S117', u'S045', u'S060', u'S124', u'S066', u'S180', u'S073', u'S168', u'S054', u'S145', u'S090', u'S048', u'S202']
    
    station_list1=[u'S108', u'S190', u'S178', u'S100', u'S059', u'S175', u'S069', u'S129', u'S028', u'S122', u'S002', u'S072',
     u'S094', u'S176', u'S215', u'S160', u'S051', u'S057', u'S078', u'S012', u'S103', u'S127', u'S036', u'S021',
     u'S208', u'S033']
    station_list2=[u'S134', u'S034', u'S037', u'S031', u'S032', u'S040', u'S043', u'S042', u'S044', u'S135', u'S136', u'S133',
     u'S019', u'S014', u'S015', u'S091', u'S096', u'S095', u'S143', u'S144', u'S148', u'S149', u'S087', u'S086',
     u'S081', u'S152', u'S159', u'S158', u'S003', u'S166', u'S167', u'S164', u'S165', u'S161', u'S105', u'S107',
     u'S186', u'S187', u'S188', u'S070', u'S074', u'S076', u'S173', u'S177', u'S204', u'S119', u'S118', u'S115',
     u'S112', u'S195', u'S191', u'S210', u'S198', u'S063', u'S067', u'S068', u'S123', u'S125', u'S055', u'S052',
     u'S053']
    station_list3=[u'S018', u'S080', u'S104', u'S075', u'S180', u'S131', u'S064', u'S097', u'S168', u'S150', u'S013', u'S098', u'S083', u'S128', u'S213',
     u'S169', u'S110', u'S039', u'S066', u'S182', u'S060', u'S016', u'S126', u'S181', u'S163', u'S170', u'S124',
     u'S035', u'S179', u'S089', u'S141', u'S117', u'S077', u'S073', u'S194', u'S162', u'S047', u'S010',
     u'S203', u'S154', u'S056', u'S027', u'S048', u'S061', u'S214', u'S157', u'S025', u'S102', u'S142', u'S007',
     u'S109', u'S185', u'S140', u'S038', u'S116', u'S189', u'S120', u'S205', u'S201', u'S113', u'S200', u'S156',
     u'S207', u'S184', u'S092', u'S058', u'S022', u'S106', u'S054', u'S202', u'S041', u'S093', u'S088', u'S146',
     u'S101', u'S049', u'S084', u'S155', u'S147', u'S199', u'S132', u'S139', u'S046', u'S006', u'S145',
     u'S197', u'S029', u'S024', u'S121', u'S045', u'S111', u'S020', u'S193', u'S004', u'S192', u'S071',
     u'S009', u'S114', u'S005', u'S023', u'S065', u'S090', u'S137', u'S099', u'S011', u'S138', u'S151', u'S212',
     u'S017', u'S008', u'S130', u'S209', u'S085', u'S001', u'S211', u'S174', u'S206', u'S082', u'S172', u'S030',
     u'S183', u'S062', u'S079', u'S153', u'S171', u'S050', u'S026', u'S196']
    '''
    station_list1=[u'S033', u'S122', u'S190', u'S127', u'S176', u'S100', u'S036', u'S103', u'S178', u'S078', u'S057', u'S215',
     u'S129', u'S028', u'S069', u'S175', u'S002', u'S208', u'S012', u'S160', u'S021', u'S072', u'S059', u'S094',
     u'S051', u'S108']
    station_list2=[u'S081', u'S143', u'S014', u'S164', u'S186', u'S167', u'S087', u'S134', u'S042', u'S086', u'S204', u'S074',
     u'S063', u'S161', u'S198', u'S076', u'S015', u'S165', u'S187', u'S149', u'S148', u'S043', u'S044', u'S158',
     u'S173', u'S144', u'S112', u'S019', u'S135', u'S166', u'S118', u'S188', u'S125', u'S105', u'S191', u'S053',
     u'S037', u'S040', u'S119', u'S107', u'S052', u'S055', u'S003', u'S152', u'S159', u'S091', u'S096', u'S195',
     u'S133', u'S034', u'S067', u'S032', u'S177', u'S210', u'S123', u'S136', u'S115', u'S068', u'S095', u'S070',
     u'S031']
    station_list3=[u'S101', u'S120', u'S048', u'S006', u'S207', u'S162', u'S197', u'S010', u'S075', u'S102', u'S047', u'S017',
     u'S060', u'S099', u'S184', u'S180', u'S079', u'S024', u'S035', u'S205', u'S121', u'S181', u'S013', u'S168',
     u'S139', u'S199', u'S058', u'S156', u'S061', u'S132', u'S214', u'S111', u'S020', u'S054', u'S147', u'S018',
     u'S029', u'S005', u'S194', u'S093', u'S097', u'S130', u'S140', u'S026', u'S150', u'S193', u'S049', u'S170',
     u'S183', u'S092', u'S073', u'S212', u'S155', u'S089', u'S206', u'S045', u'S083', u'S114', u'S200', u'S084',
     u'S041', u'S116', u'S066', u'S009', u'S169', u'S104', u'S157', u'S117', u'S179', u'S022', u'S064', u'S213',
     u'S211', u'S174', u'S065', u'S185', u'S154', u'S050', u'S090', u'S085', u'S172', u'S142', u'S171', u'S138',
     u'S038', u'S196', u'S151', u'S128', u'S077', u'S203', u'S046', u'S124', u'S163', u'S182', u'S209', u'S141',
     u'S027', u'S110', u'S008', u'S023', u'S109', u'S080', u'S016', u'S007', u'S098', u'S126', u'S137', u'S062',
     u'S189', u'S001', u'S113', u'S071', u'S056', u'S131', u'S025', u'S145', u'S201', u'S030', u'S082', u'S153',
     u'S106', u'S039', u'S192', u'S146', u'S004', u'S088', u'S011', u'S202']

    print (station_list1)
    print (station_list2)
    print (station_list3)

    len_1 = 0  # len(bins)
    for s in station_list1:
        ll = len(stations[s].binList)
        len_1 += ll
    for s in station_list2:
        ll = len(stations[s].binList)
        len_1 += ll
    for s in station_list3:
        ll = len(stations[s].binList)
        len_1 += ll

    vehicle_list1 = []
    vehicle_list1 = schedule.schedule_mst_r_learning(stations, vehicles, station_list1, station_list2, station_list3, map, time)

    sum_1=0
    for v in vehicle_list1:
        sum_1+=len(v.bin_list)
    print sum_1,"++++++"
    for v in res_vehicle_list:
        vehicle_list1.append(v)
        sum_1 += len(v.bin_list)
    print sum_1,"--------"

    final_process.pick_bins(vehicle_list1,stations,map,time)
    final_process.change_vehicle(vehicle_list1, vehicles)
    geneticAlgm.check_vehicle_list(vehicle_list1)
    final_process.pick_bins(vehicle_list1, stations, map, time)
    r_learning.cal_vehicle_list_path(vehicle_list1,map)

    total_cost, total_rate = geneticAlgm.cal_final_result(vehicle_list1, map)
    print(total_cost, total_rate)

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
        if tmp_area/(v.length*v.width) < 0.75:

            print(v.id," ",tmp_area," ",round(v.length*v.width,5))

            #createEntity.draw_rect(v,tmp_area)


if __name__ == '__main__':
    path = "../dataset/month4/"
    print("enter")
    map, time = createEntity.createMap(path + "matrix.json")
    stations, maxLimit = createEntity.createStation(path + "station.json")

    bins = createEntity.createBin(path + "bin.json", stations)
    r_learning.label_stations(stations)

    vehicles = createEntity.createVehicle(path + "vehicle.json")
    res_vehicle_list = []
    res_vehicle_list = merge_stations.many_merge(vehicles, stations, map, time)

    for v in res_vehicle_list:
        if v.id==u'V696':
            print v.id, v.path

    sum = 0
    for v in res_vehicle_list:
        sum += len(v.bin_list)

    print sum

    for i in range(200):
        avaibalbe_vehicle_list = []
        for i in range(len(vehicles)):
            v = vehicles[i]
            avaibalbe_vehicle_list.append(geneticAlgm.create_new_vehicle(v))
            avaibalbe_vehicle_list[-1].is_available = v.is_available

        station_dict = {}
        for s in stations:
            ss = stations[s]
            station_dict[s] = geneticAlgm.create_new_station(ss)
            createEntity.cal_station_area_weight(station_dict[s])

        r_learning.label_stations(station_dict)
        my_test(avaibalbe_vehicle_list, station_dict, map, time, res_vehicle_list)

