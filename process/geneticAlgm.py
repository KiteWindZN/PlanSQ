# -*- coding:utf-8 -*-
"""
此文件为最初设计的用启发式算法去调度车辆，现在除了一些基本的功能性的函数，其余基本弃用
"""
from entity import entity
import createEntity
import skyLine
import sys
import random
from createJson import createResult

#遗传算法
def genetic(vehicles,stations,map,time,gene_num):
    print("genetic Algm")

    final_cost=sys.maxsize
    final_rate = 0
    final_gene=[]

    gene_list=[]
    for i in range(gene_num):
        res=create_gene_station(stations)
        gene_list.append(res)

    N = 100

    for i in range(N):
        res_gene=[]
        res_cost=[]
        res_rate=[]
        for j in range(len(gene_list)):
            vehicle_list = schedule_gene(gene_list[j],vehicles,stations,map,time)
            check_vehicle_list(vehicle_list)
            cost,rate = cal_final_result(vehicle_list,map)
            res_cost.append(cost)
            res_rate.append(rate)
            if final_cost > cost:
                final_cost = cost
                final_rate = rate
                final_gene = copy_gene(gene_list[j])
        print(i," : ",final_cost,final_rate," , ",final_gene)
        #return final_gene, final_cost, final_rate
        #choose 200 gene
        for h in range(200):
            min_cost = sys.maxsize
            for k in range(10):
                choose_index=0
                index= random.randint(0,len(gene_list)-1)
                if res_cost[index]< min_cost:
                    choose_index = index
                    min_cost = res_cost[index]
            res_gene.append(gene_list[choose_index])
        #cross

        #cross_rate = 1
        #mutation_rate = 0.6

        for h in range(len(res_gene)):
            index1 = random.randint(0, len(res_gene) - 1)
            index2 = random.randint(0, len(res_gene) - 1)
            for nn in range(len(res_gene)/4):
                gene_mutation(res_gene[index1])
                gene_cross(res_gene[index1], res_gene[index2])


        gene_list = res_gene
        res_cost=[]
        res_rate=[]
        res_gene=[]

    return final_gene,final_cost,final_rate


def copy_gene(gene):
    res_gene=[]
    for g in gene:
        res_gene.append(g)
    return res_gene

#注意消除冲突的问题
def gene_cross(gene1,gene2):
    gene_len=len(gene1)

    # 消除冲突
    list1 = {}
    list2 = {}
    change1 = []
    change2 = []

    for i in gene1:
        list1[i] = 0
        list2[i] = 0

    cross_start=random.randint(0,gene_len-1)
    i=cross_start
    while i< (gene_len-1):
        tmp=gene1[i]
        gene1[i]=gene2[i]
        gene2[i]=tmp
        i=i+1

    for i in range(gene_len):
        list1[gene1[i]] = list1[gene1[i]]+1
        if list1[gene1[i]] == 2:
            change1.append(i)

        list2[gene2[i]] = list2[gene2[i]]+1
        if list2[gene2[i]] == 2:
            change2.append(i)
    for i in range(len(change1)):
        tmp = gene1[change1[i]]
        gene1[change1[i]]=gene2[change2[i]]
        gene2[change2[i]]=tmp


#变异过程
def gene_mutation(gene):
    gene_len=len(gene)
    first = random.randint(0,gene_len-1)
    second = random.randint(0,gene_len-1)
    while second == first:
        second = random.randint(0,gene_len-1)
    tmp=gene[first]
    gene[first]=gene[second]
    gene[second]=tmp


#产生gene过程
def create_gene_bin(bin_list):
    bin_len = len(bin_list)
    bin_index_list = []
    res = []
    for i in range(bin_len):
        bin_index_list.append(i)

    while bin_len>0:
        index=random.randint(0,bin_len-1)
        gene=bin_index_list[index]
        res.append(gene)
        bin_index_list.remove(gene)
        bin_len=bin_len-1

    return res

#模拟退火算法
def simulated_annealing(bins,vehicle):
    T=10000
    a=0.9

#产生station的基因序列
def create_gene_station(stations):
    station_id_list=[]

    res=[]
    for s in stations:
        station_id_list.append(s)
    station_len = len(station_id_list)
    while station_len > 0:
        index=random.randint(0,station_len-1)
        gene = station_id_list[index]
        res.append(gene)
        station_id_list.remove(gene)
        station_len = len(station_id_list)
    return res


def create_gene_station1(stations):
    station_id_list1,station_id_list2,station_id_list3=createEntity.divide_stations(stations)
    station_len = len(station_id_list1)

    res=[]

    while station_len > 0:
        index=random.randint(0,station_len-1)
        gene = station_id_list1[index]
        res.append(gene)
        station_id_list1.remove(gene)
        station_len = len(station_id_list1)

    station_len = len(station_id_list2)
    while station_len > 0:
        index=random.randint(0,station_len-1)
        gene = station_id_list2[index]
        res.append(gene)
        station_id_list2.remove(gene)
        station_len = len(station_id_list2)

    station_len = len(station_id_list3)
    while station_len > 0:
        index=random.randint(0,station_len-1)
        gene = station_id_list3[index]
        res.append(gene)
        station_id_list3.remove(gene)
        station_len = len(station_id_list3)
    return res



#模拟退火算法
def simulated_annealing(bins,vehicle):
    T=10000
    a=0.9



#检查是否所有的站点的货物均已经装完
def is_finashed(stations):
    for s in stations:
        if stations[s].isEmpty==False:
            return False
    return True

def find_min_width(bins,vehicle):
    min_width=bins[0].width
    res=0

    for i in range(len(bins)):
        if min_width>bins[i].width and (bins[i].weight + vehicle.used_weight) <= vehicle.weight:
            min_width=bins[i].width
            res=i
        if min_width>bins[i].length and (bins[i].weight + vehicle.used_weight) <= vehicle.weight:
            min_width=bins[i].length
            res=i
            bins[i].rotate_bin()
    return res

def schedule_gene(gene,vehicles,stations,map,T):
    res_vehicle_list=[]
    vehicles_not_full=[]
    flag = 0
    list = [664]
    index=0
    for vehicle in vehicles:
        vehicle.is_available = True
    for i in range(len(gene)):
        g=gene[i]
        #print(i , g)
        choose_station = stations[g]
        if choose_station.isEmpty == True:
            continue
        if flag == 0:
            weight = choose_station.weight
            choose_vehicle_num = choose_vehicle_index(vehicles,choose_station,stations,gene,i)

            choose_vehicle = create_new_vehicle(vehicles[choose_vehicle_num])

            vehicles[choose_vehicle_num].is_available=False
            res_vehicle_list.append(choose_vehicle)
        choose_vehicle.usedTime = choose_vehicle.usedTime + choose_station.loading_time

        while choose_station.weight != 0:
            #print "aaa"
            max_height = skyLine.skyline(choose_vehicle,choose_station)
            createEntity.cal_station_area_weight(choose_station)
            if choose_station.weight == 0:
                choose_station.isEmpty = True
                if max_height < choose_vehicle.length * 0.8:
                    if i < len(gene)-1:
                        if map[str(g)][str(gene[i+1])] * choose_vehicle.perPrice >= choose_vehicle.startPrice :

                            next_index = find_next_ok_station(choose_vehicle, stations, gene, i, choose_station,map, T)
                            if next_index != -1:

                                skyLine.skyline(choose_vehicle, stations[gene[next_index]])
                                createEntity.cal_station_area_weight(stations[gene[next_index]])

                            flag = 0
                            continue
                        if choose_vehicle.usedTime + T[str(g)][str(gene[i+1])] + stations[str(gene[i+1])].loading_time <= 600 \
                            and choose_vehicle.length <= stations[str(gene[i+1])].vehicle_limit:

                            choose_vehicle.usedTime = choose_vehicle.usedTime + T[g][gene[i+1]]
                            flag=1
                        else:
                            flag=0
                            if max_height < choose_vehicle.length:
                                next_index=find_next_ok_station(choose_vehicle, stations, gene, i, choose_station,map, T)
                                if next_index != -1:
                                    skyLine.skyline(choose_vehicle,stations[gene[next_index]])
                                    createEntity.cal_station_area_weight(stations[gene[next_index]])
                else:
                    flag=0
            else:
                #weight = choose_station.weight
                choose_vehicle_num = choose_vehicle_index(vehicles, choose_station,stations,gene,i)

                choose_vehicle = create_new_vehicle(vehicles[choose_vehicle_num])
                vehicles[choose_vehicle_num].is_available = False
                res_vehicle_list.append(choose_vehicle)
                choose_vehicle.usedTime = choose_vehicle.usedTime + choose_station.loading_time
                flag=1
    path="../dataset/month3/"
    createEntity.createBin(path + "bin.json", stations) #add bins to stations again
    return res_vehicle_list


def find_next_ok_station(vehicle,stations,gene,i,start_station,map,T):
    if i+1 == len(gene):
        return -1
    res = -1
    tmp_dis=sys.maxsize
    while i+1 < len(gene):
        i=i+1
        limit=stations[gene[i]].vehicle_limit
        if stations[gene[i]].isEmpty == False and T[start_station.id][gene[i]] + vehicle.usedTime <= 600 and limit >= vehicle.length and map[start_station.id][gene[i]] * vehicle.perPrice < vehicle.startPrice:
            if tmp_dis > map[start_station.id][gene[i]]:
                res = i
                tmp_dis = map[start_station.id][gene[i]]
    return res



def check_vehicle(vehicle):
    path= vehicle.path
    if vehicle.id == "V656":
        print ("gggggg")
    station_bin = vehicle.station_bin
    for s in path:
        if s not in station_bin:
            print vehicle.id
            print("aaa")
        if len(station_bin[s])==0:
            path.remove(s)
            station_bin.pop(s)

def check_vehicle_weight(vehicle):
    bin_list=vehicle.bin_list
    sum_weight=0
    for bin in bin_list:
        sum_weight= round(sum_weight+bin.weight,5)
    if sum_weight > vehicle.weight:
        print vehicle.id ,"over weight"

def check_vehicle_list(vehicle_list):
    for vehicle in vehicle_list:
        check_vehicle(vehicle)
        check_vehicle_weight(vehicle)

def check_vehicle_limit(vehicle_list,stations):
    for vehicle in vehicle_list:
        vehicle_length = vehicle.length
        path = vehicle.path
        for s in path:
            station_limit = stations[s].vehicle_limit
            if station_limit < vehicle_length:
                print(station_limit, vehicle_length)



#前向搜索树算法
def forward_tree(bins,vehicle):
    print()

def createBlock(bins):
    length=len(bins)
    min_rate=0.9
    new_bins=[]
    for i in range(length):
        cal_rate = 0
        choose=-1
        b=entity.Bin("",0,0,0)
        for j in range(length):
            if i==j:
                continue
            bin,rate=gen_block(bins[i],bins[j],min_rate)
            if rate==0:
                continue
            if cal_rate<rate:
                cal_rate=rate
                choose=j
                b=bin
        if choose != -1:
            new_bins.append(b)
            bins.remove(bins[i])
            bins.remove(bins[j])
            length=len(bins)


#先分配70%的车辆去拉货，然后更新站点数据，再派出30%的车，然后更新数据，再根据货物
#分配车辆时三种类型的车先按照1：1：1的比例分配，
# 分配到具体站点的时候，按如下规则分配：
# 1.随机选择站点，检测站点的货物重量，和货物需要的总的面积信息，根据此信息分配车辆
# 2.初始分配站点时，一些作为交通枢纽的站点被选中的可能性更大

#车辆的调度执行如下规则：
#1.如果一辆车的使用率达到了90%以上，则不再调度它，
#   或者检测该车辆到达邻居站点需要的time，cost，以及可以装上的货物，是否可以更大的提高使用率，并且消耗不大时，才可以继续调度
#2.初始的选择点是随机的可能会因为初始点的不同而导致结果有较大的变化
#   根据随机性原理，多跑几遍数据，选择最优的结果
#3.尽量结合遗传算法和模拟退火算法，跑出合理的车辆调度路径


def not_empty_stations(stations):
    res_stations=[]
    for s in stations:
        if stations[s].isEmpty ==  False:
            res_stations.append(s)
    return res_stations

def create_new_vehicle(vehicle):
    id=vehicle.id
    length=vehicle.length
    width=vehicle.width
    weight=vehicle.weight
    sp=vehicle.startPrice
    pp=vehicle.perPrice
    v=entity.Vehicle(id,length,width,weight,sp,pp)
    return v


def create_new_station(station):
    id=station.id
    vehicle_limit=station.vehicle_limit
    loading_time=station.loading_time
    s=entity.Station(id,vehicle_limit,loading_time)

    binList = station.binList
    if len(binList)>0:
        s.isEmpty=False

    for b in binList:
        new_b=create_new_bin(b)
        s.binList.append(new_b)
    return s

def create_new_bin(bin):
    id=bin.id
    length=bin.length
    width=bin.width
    weight=bin.weight
    s=bin.local_station
    b=entity.Bin(id, length, width, weight, s)
    #point_list=bin.pointList
    #for p in point_list:
    #    b.pointList.append(entity.Point(p.x,p.y))
    return b

def choose_vehicle_index(vehicle_list,station,stations,gene,gene_index):

    #if station.id == "S194":
    #    print("bbbb")
    flag=1
    if gene_index+1 == len(gene):
        flag=1

    i=gene_index+1
    while i<len(gene):
        tmp_s=stations[gene[i]]
        if tmp_s.vehicle_limit >= station.vehicle_limit:
            flag = 0
            break
        i=i+1

    weight=station.weight
    area=station.area

    if flag==1:
        for i in range(len(vehicle_list)):
            vehicle_area = vehicle_list[i].length * vehicle_list[i].width
            if vehicle_list[i].length <= station.vehicle_limit and vehicle_list[i].is_available == True and weight < vehicle_list[i].weight*0.8 and area < vehicle_area*0.8:
                return i


    i = len(vehicle_list) - 1
    while i>0:
        if vehicle_list[i].length <= station.vehicle_limit and vehicle_list[i].is_available == True:
            return i
        i = i-1


def find_max_vehicle(vehicle_list):
    max=vehicle_list[0]
    res=0
    for i in range(len(vehicle_list)):
        if max < vehicle_list[i]:
            res=i
    return res


def gen_block(b1,b2,min_rate):
    l = 0.0
    w = 0.0
    bin=entity.Bin(b1.id+"_"+b2.id,l,w,0)
    s1=b1.length*b1.width
    s2=b2.length*b2.width
    rate=0

    for i in range(2):
        l = max(b1.length, b2.length)
        w = max(b1.width, b2.width)
        if i == 0:
            w = b1.width + b2.width
        if i==1:
            l=b1.length+b2.length

        r = (s1+s2)/(l*w)
        if r > min_rate:
            if rate < r:
                rate=r
                bin.length=l
                bin.width=w
                bin.weight=b1.weight+b2.weight


        return bin,rate



def cal_cost_and_rate(vehicle,map):
    cost=0.0
    bin_list=vehicle.bin_list
    total_area=vehicle.length * vehicle.width
    used_area=0.0
    if vehicle.id==u"V890":
        print vehicle.path
    path=vehicle.path

    cost=cost + vehicle.startPrice
    distance=0.0
    for i in range(len(path)):
        if i ==0:
            start= path[i]
            continue
        cur=path[i]
        if cur not in map[start]:
            print("nonono")
            print i,start,cur,vehicle.id,path
        distance = distance + map[start][cur]
        start=cur
    cost = cost +distance * vehicle.perPrice
    for bin in bin_list:
        used_area = used_area + bin.length * bin.width

    rate=used_area / total_area
    return cost, rate


def cal_final_result(vehicle_list,mst):
    total_cost=0.0
    total_rate=0.0

    for vehicle in vehicle_list:
        cost,rate=cal_cost_and_rate(vehicle,mst)
        total_cost= total_cost+cost
        total_rate=total_rate + rate

    total_rate = total_rate / len(vehicle_list)

    return total_cost, total_rate

def cal_used_rate(v):
    tmp_area=0
    for b in v.bin_list:
        tmp_area = round(tmp_area + b.length * b.width, 5)
    return tmp_area / (v.length * v.width)


if __name__ == '__main__':
    path = "../dataset/month3/"

    print("enter")
    map, time = createEntity.createMap(path + "matrix.json")
    stations, maxLimit = createEntity.createStation(path + "station.json")
    bins = createEntity.createBin(path + "bin.json", stations)
    vehicles = createEntity.createVehicle(path + "vehicle.json")

    print()
    print(len(vehicles[2].bin_list))
    print()
    print(len(stations["S012"].binList))



    path = createResult.createFileJson()

    #createResult.createJson(path, vehicle_list)
    #createEntity.update_stations(stations)

    #tmp_area=0.0
    #for b in vehicles[2].bin_list:
    #    tmp_area = round(tmp_area+b.length*b.width,5)
    #print(tmp_area," ",round(vehicles[2].length*vehicles[2].width,5))

    #  createEntity.draw_rect(vehicles[2],tmp_area)


    gene,cost,rate = genetic(vehicles,stations,map,time,200)
    #gene=['S152', 'S209', 'S009', 'S144', 'S098', 'S061', 'S159', 'S163', 'S148', 'S072', 'S211', 'S024', 'S090', 'S172', 'S141', 'S118', 'S170', 'S124', 'S010', 'S044', 'S078', 'S086', 'S075', 'S197', 'S036', 'S122', 'S129', 'S045', 'S160', 'S114', 'S117', 'S115', 'S183', 'S094', 'S033', 'S027', 'S058', 'S203', 'S079', 'S029', 'S005', 'S016', 'S165', 'S088', 'S113', 'S167', 'S212', 'S187', 'S202', 'S133', 'S076', 'S089', 'S096', 'S178', 'S080', 'S207', 'S215', 'S128', 'S155', 'S099', 'S132', 'S018', 'S021', 'S180', 'S173', 'S192', 'S052', 'S151', 'S181', 'S057', 'S164', 'S034', 'S119', 'S140', 'S053', 'S071', 'S109', 'S166', 'S073', 'S006', 'S050', 'S026', 'S111', 'S110', 'S068', 'S014', 'S134', 'S136', 'S013', 'S048', 'S120', 'S116', 'S070', 'S121', 'S054', 'S175', 'S047', 'S008', 'S214', 'S138', 'S001', 'S056', 'S142', 'S156', 'S038', 'S198', 'S082', 'S103', 'S196', 'S060', 'S205', 'S150', 'S022', 'S158', 'S059', 'S064', 'S042', 'S123', 'S139', 'S145', 'S146', 'S025', 'S074', 'S104', 'S051', 'S077', 'S171', 'S101', 'S153', 'S161', 'S062', 'S177', 'S095', 'S210', 'S201', 'S066', 'S179', 'S032', 'S102', 'S204', 'S097', 'S084', 'S135', 'S125', 'S184', 'S182', 'S093', 'S092', 'S067', 'S147', 'S063', 'S168', 'S069', 'S200', 'S169', 'S043', 'S213', 'S185', 'S004', 'S162', 'S041', 'S206', 'S143', 'S188', 'S017', 'S126', 'S193', 'S105', 'S127', 'S083', 'S208', 'S028', 'S003', 'S040', 'S174', 'S130', 'S195', 'S049', 'S191', 'S065', 'S030', 'S081', 'S199', 'S015', 'S108', 'S107', 'S154', 'S011', 'S035', 'S157', 'S002', 'S176', 'S100', 'S137', 'S007', 'S019', 'S023', 'S020', 'S087', 'S046', 'S149', 'S190', 'S112', 'S091', 'S055', 'S085', 'S131', 'S037', 'S189', 'S039', 'S106', 'S194', 'S012', 'S031', 'S186']
    vehicle_list=schedule_gene(gene,vehicles,stations,map,time)
    check_vehicle_list(vehicle_list)
    total_cost,total_rate=cal_final_result(vehicle_list,map)
    print(total_cost,total_rate)
    #print (total_cost , total_rate)
    #path = createResult.createFileJson()

    #status=is_finashed(stations)
    #print(status)

    #for i in range(len(gene)):
    #    if i+1 < len(gene):
    #        print(map[str(gene[i])][str(gene[i+1])])

    len_1=len(bins)
    len_2=0
    for v in vehicle_list:
        len_2 = len_2 + len(v.bin_list)


    print( "len_1 : ", len_1, "len_2 : ",len_2)

    createResult.createJson(path, vehicle_list)


    tmp_area=0.0
    for b in vehicle_list[2].bin_list:
        tmp_area = round(tmp_area+b.length*b.width,5)
    print(tmp_area," ",round(vehicles[2].length*vehicles[2].width,5))

    createEntity.draw_rect(vehicle_list[2],tmp_area)

