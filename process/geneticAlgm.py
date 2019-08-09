# -*- coding:utf-8 -*-
from entity import entity
from process import createEntity
from process import skyLine
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

    res_cost=[]
    res_rate=[]
    res_gene=[]

    for i in range(N):
        for j in range(len(gene_list)):
            vehicle_list = schedule_gene(gene_list[j],vehicles,stations,time)
            cost,rate = cal_final_result(vehicle_list,map)
            res_cost.append(cost)
            res_rate.append(rate)
            if final_cost > cost:
                final_cost = cost
                final_rate = rate
                final_gene = copy_gene(gene_list[j])

        #choose 200 gene
        for h in range(100):
            min_cost = sys.maxsize
            for k in range(10):
                choose_index=0
                index= random.randint(0,gene_num-1)
                if res_cost[index]< min_cost:
                    choose_index = index
                    min_cost = res_cost[index]
            res_gene.append(gene_list[choose_index])
        #cross
        cross_rate = 0.5
        mutation_rate = 0.2

        for h in range(len(res_gene)):
            index1 = random.randint(0,len(res_gene))
            rate1=random.random()
            if rate1<= mutation_rate:
                gene_mutation(res_gene[index1])
            rate1=random.random()
            if rate1 <= cross_rate:
                index2=random.randint(0,len(res_gene))
                gene_cross(res_gene[index1],res_gene[index2])

        gene_list = res_gene

    return final_gene,final_cost,final_rate


def copy_gene(gene):
    res_gene=[]
    for g in gene:
        res_gene.append(g)
    return res_gene

#注意消除冲突的问题
def gene_cross(gene1,gene2):
    gene_len=len(gene1)
    cross_start=random.randint(0,gene_len-1)
    i=cross_start
    while i< (gene_len-1):
        tmp=gene1[i]
        gene1[i]=gene2[i]
        gene2[i]=tmp
        i=i+1
    #消除冲突
    list1=[]
    list2=[]
    change1=[]
    change2=[]

    for i in gene1:
        list1.append(0)
        list2.append(0)
    for i in range(gene_len):
        list1[gene1[i]] = list1[gene1[i]]+1
        if list1[gene1[i]] == 2:
            change1.append(gene1[i])

        list2[gene2[i]] = list2[gene2[i]]+1
        if list2[gene2[i]] == 2:
            change2.append(gene2[i])
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


def create_gene_station(stations):
    station_len = len(stations)
    station_list=[]
    res=[]
    for s in stations:
        station_list.append(s)

    while station_len > 0:
        index=random.randint(0,station_len-1)
        gene = station_list[index]
        res.append(gene)
        station_list.remove(gene)
        station_len = len(station_list)
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


def schedule_gene(gene,vehicles,stations,T):
    res_vehicle_list=[]
    flag = 0
    list = [664]
    index=0
    for vehicle in vehicles:
        vehicle.is_available = True
    for i in range(len(gene)):
        g=gene[i]
        #print(i , g)
        choose_station = stations[g]
        if flag == 0:
            weight = choose_station.weight
            choose_vehicle_num = choose_vehicle_index(weight, vehicles,choose_station)
            #choose_vehicle_num=list[index]
            #index= index+1
            choose_vehicle = create_new_vehicle(vehicles[choose_vehicle_num])
            #vehicles.remove(vehicles[choose_vehicle_num])
            vehicles[choose_vehicle_num].is_available=False
            res_vehicle_list.append(choose_vehicle)
        choose_vehicle.usedTime = choose_vehicle.usedTime + choose_station.loading_time

        while choose_station.weight != 0:
            #print "aaa"
            max_height = skyLine.skyline(choose_vehicle,choose_station)
            createEntity.cal_station_area_weight(choose_station)
            if choose_station.weight == 0:
                choose_station.isEmpty = True
                if max_height < choose_vehicle.length:
                    if i < len(gene)-1 and choose_vehicle.usedTime + T[str(g)][str(gene[i+1])] + stations[str(gene[i+1])].loading_time <= 600 \
                            and choose_vehicle.length <= stations[str(gene[i+1])].vehicle_limit:
                        if choose_vehicle.length > stations[str(gene[i+1])].vehicle_limit:
                            print("aaaaaa")
                        choose_vehicle.usedTime = choose_vehicle.usedTime + T[g][gene[i+1]]
                        flag=1
                    else:
                        flag=0
                else:
                    flag=0
            else:
                weight = choose_station.weight
                choose_vehicle_num = choose_vehicle_index(weight, vehicles, choose_station)
                #choose_vehicle_num = list[index]
                #index = index + 1
                choose_vehicle = create_new_vehicle(vehicles[choose_vehicle_num])
                #vehicles.remove(vehicles[choose_vehicle_num])
                vehicles[choose_vehicle_num].is_available = False
                res_vehicle_list.append(choose_vehicle)
                choose_vehicle.usedTime = choose_vehicle.usedTime + choose_station.loading_time
                flag=0

    return res_vehicle_list





def check_vehicle(vehicle):
    path= vehicle.path
    station_bin = vehicle.station_bin
    for s in path:
        if len(station_bin[s])==0:
            path.remove(s)
            station_bin.pop(s)


def check_vehicle_list(vehicle_list):
    for vehicle in vehicle_list:
        check_vehicle(vehicle)

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


def schedule_vehicle(mst,T,vehicle_list,total_weight,stations,rate,res_vehicle_list):
    first_weight=total_weight * rate
    avg_weight=0
    for vehicle in vehicle_list:
        avg_weight = avg_weight + vehicle.weight
    avg_weight = avg_weight / len(vehicle_list)
    vehicle_first_num = first_weight / avg_weight



    for i in range(vehicle_first_num):
        choose_station_num=random.randint(1,len(stations))
        if choose_station_num<10:
            choose_station_id="S00"+choose_station_num
        elif choose_station_num<100:
            choose_station_id="S0"+choose_station_num
        else:
            choose_station_id="S"+choose_station_num
        choose_station=stations[choose_station_id]
        station_weight = choose_station.weight
        choose_vehicle_num=choose_vehicle_index(station_weight,vehicle_list)
        choose_vehicle = create_new_vehicle(vehicle_list[choose_vehicle_num])
        res_vehicle_list.append(choose_vehicle)

        #vehicle顺着树跑路
        while True:
            choose_vehicle.usedTime= choose_vehicle.usedTime + choose_station.loading_time
            choose_vehicle.path.append(choose_station_id)
            choose_vehicle.station_bin[choose_station_id]={}
            max_height=skyLine(choose_vehicle, choose_station)
            #不需要调度的情况
            if max_height == choose_vehicle.length and len(choose_station.binList)>0:
                break
            else:#随机选择下一个站点
                #使用时间范围内，可到达的station
                enable_stations = []
                next_stations = mst[choose_station]
                for s in next_stations:
                    if choose_vehicle.usedTime + T[choose_station_id][s] + stations[s].loading_time <= 600 and stations[s].isEmpty==False:
                        enable_stations.append(s)
                if len(enable_stations) == 0:#临近节点都不可用,可能需要补充继续调度节点的操作，直到vehicle的使用率达到一定的比率
                    break

                choose_station_num=random.randint(0,len(enable_stations)-1)
                j=0
                for s in enable_stations:
                    if j == choose_station_num:
                        choose_station=stations[s]
                        choose_vehicle.usedTime = choose_vehicle.usedTime + T[choose_station_id][s]
                        break
                    j = j + 1
    createEntity.update_stations(stations)

#最后一次调度车辆，根据第二次的结果，计算当前节点的状态，一辆一辆的分配车辆，直到全部收集完所有的货物
def schedule_vehicle_final(mst,T,vehicle_list,stations,res_vehicle_list):
    for s in stations:
        if stations[s].isEmpty == False:
            continue

        choose_station=stations[s]
        weight=choose_station.weight
        choose_vehicle_num=choose_vehicle_index(weight,vehicle_list)
        choose_vehicle=create_new_vehicle(vehicle_list[choose_vehicle_num])
        res_vehicle_list.append(choose_vehicle)

        max_height=0
        while True:
            choose_vehicle.usedTime = choose_vehicle.usedTime + choose_station.loading_time
            choose_vehicle.path.append(s)
            choose_vehicle.station_bin[s] = {}
            max_height=skyLine(choose_vehicle, choose_station)
            if max_height == choose_vehicle.length and len(choose_station.binList) > 0:
                if is_finashed(stations) == True:
                    break
                continue
            else:#随机选择下一个站点
                #使用时间范围内，可到达的station
                enable_stations = []
                next_stations = mst[choose_station]
                for n_s in next_stations:
                    if choose_vehicle.usedTime + T[s][n_s] <= 600 and stations[s].isEmpty is False:
                        enable_stations.append(s)
                if len(enable_stations) == 0:#临近节点都不可用,可能需要补充继续调度节点的操作，直到vehicle的使用率达到一定的比率
                    break

                choose_station_num=random.randint(0,len(enable_stations)-1)
                j=0
                for s in enable_stations:
                    if j== choose_station_num:
                        choose_station=stations[s]
                        choose_vehicle.usedTime = choose_vehicle.usedTime + T[s][n]
                        break
            createEntity.update_stations(stations)
            if is_finashed(stations) == True:
                break


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

def choose_vehicle_index(weight,vehicle_list,station):
    i=len(vehicle_list)-1
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
    path=vehicle.path

    cost=cost + vehicle.startPrice
    distance=0.0
    for i in range(len(path)):
        if i ==0:
            start= path[i]
            continue
        cur=path[i]
        distance = distance + map[start][cur]
        start=cur
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



if __name__ == '__main__':
    path = "../dataset/month3/"

    print("enter")
    map, time = createEntity.createMap(path + "matrix.json")
    stations, maxLimit = createEntity.createStation(path + "station.json")
    bins = createEntity.createBin(path + "bin.json", stations)
    vehicles = createEntity.createVehicle(path + "vehicle.json")
    #mts, T = createEntity.createMST(map, time)
    #createEntity.deleteVehicle(vehicles, maxLimit)

    #print()
    #print(len(stations["S045"].binList))

    #max_height=skyLine.skyline(vehicles[998],stations["S045"])


    #print()
    #print(max_height)

    #print()
    #print(len(vehicles[998].bin_list))
    #print()
    #print(len(stations["S012"].binList))

    #vehicle_list=[]
    #vehicle_list.append(vehicles[998])

    path = createResult.createFileJson()

    #createResult.createJson(path, vehicle_list)
    #createEntity.update_stations(stations)

    #tmp_area=0.0
    #for b in vehicles[2].bin_list:
    #    tmp_area = round(tmp_area+b.length*b.width,5)
    #print(tmp_area," ",round(vehicles[2].length*vehicles[2].width,5))

    #  createEntity.draw_rect(vehicles[2],tmp_area)

    #gene=create_gene_station(stations)
    #gene=["S171","S164", "S104","S087","S008","S200","S003","S188","S099","S167", "S038","S132","S035","S127","S066","S076","S010","S169","S027","S170","S079"]
    #gene=["S163"]
    #print gene
    #print len(gene)

    gene = genetic(vehicles,stations,map,time,200)
    vehicle_list=schedule_gene(gene,vehicles,stations,time)
    #total_cost,total_rate=cal_final_result(vehicle_list,map)

    #print (total_cost , total_rate)
    #path = createResult.createFileJson()

    status=is_finashed(stations)
    print(status)

    #for i in range(len(gene)):
    #    if i+1 < len(gene):
    #        print(time[str(gene[i])][str(gene[i+1])])

    len_1=len(bins)
    len_2=0
    for v in vehicle_list:
        len_2 = len_2 + len(v.bin_list)


    print( "len_1 : ", len_1, "len_2 : ",len_2)

    createResult.createJson(path, vehicle_list)

    check_vehicle_limit(vehicle_list,stations)