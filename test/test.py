# -*-coding:utf-8-*-
import matplotlib.pyplot as plt
import random
import json
from entity import entity
from process import geneticAlgm
from process import createEntity
from process import skyLine

def draw_rect(vehicle):
  colors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple']
  fig = plt.figure()
  ax = fig.add_subplot(111)
  bin_list = vehicle.bin_list
  for bin in bin_list:
    point_list= bin.pointList
    start1=point_list[0].x
    end1=point_list[0].y
    width=point_list[1].x - point_list[0].x
    height=point_list[2].y - point_list[1].y
    color_index=random.randint(1,100)
    plt.gca().add_patch(plt.Rectangle((start1, end1), width, height,facecolor=colors[color_index%7]))
  plt.show()



def resolveBinJson(path,map,bins):
    file=open(path,"r")
    fileJson=json.load(file)
    #print(fileJson)
    i=0
    vehicles_info = fileJson
    vehicle_list=[]
    bin_map={}
    #for i in range(len(vehicles_info)):
    #    v_info = vehicles_info[i]

    for v_info in vehicles_info:
        if v_info <= "V333":
          length = 7.8
          width=2.3
          weight=10000
          sp=888
          pp=0.004
        elif v_info <="V666":
          length = 9.6
          width = 3.0
          weight=15000
          sp = 999
          pp = 0.00418
        else:
          length = 17.5
          width = 3
          weight=30000
          sp = 1199
          pp = 0.00439
        vehicle=entity.Vehicle(v_info,length,width,weight,sp,pp)
        vehicle_list.append(entity.Vehicle(v_info,length,width,weight,sp,pp))
        vehicle_list[-1].path=vehicles_info[v_info]["Route"]

        path=vehicles_info[v_info]["Route"]
        info=vehicles_info[v_info]
        point_lists={}
        for p in path:
            bin_list=info[p]
            #print (v_info,len(bin_list))
            for b_id in bin_list:
                point_lists[b_id]=bin_list[b_id]

            i += len(bin_list)
            for b in bin_list:
                b_id=b

                if b_id not in bin_map:
                    bin_map[b_id]=1
                else:
                    bin_map[b_id] += 1
                    print "hhhhhhhh",b_id,p,v_info
        #check_result(vehicle,point_lists)

        tmp_list=[]
        for p in point_lists:
            tmp_list.append(point_lists[p])
        print vehicle.id
        check_rect(tmp_list)
    for b in bins:
        b_id = b.id
        if b_id not in bin_map:
            print b_id,b.local_station,v_info
    cost,rate=geneticAlgm.cal_final_result(vehicle_list,map)
    print(cost, rate)
    print(len(bin_map),i)


def test_result():
    path = "../dataset/month4/"

    print("enter")
    map, time = createEntity.createMap(path + "matrix.json")

    stations, maxLimit = createEntity.createStation(path + "station.json")
    #station_total=stations["S001"]

    bins = createEntity.createBin(path + "bin.json", stations)
    resolveBinJson("../result/839898.44385_2019-09-22-20:44:13-result.json",map,bins)

def test_gene_score():
    line_1=entity.Line(entity.Point(0,0),entity.Point(1.275,0),1.225,7.8)
    bin_1=entity.Bin("B001",1.225,1.025,100,"S001")
    score_1=skyLine.gene_score(line_1,bin_1)
    bin_1.rotate_bin()
    score_2=skyLine.gene_score(line_1,bin_1)
    print score_1,score_2

#test_gene_score()


def check_result(vehicle,point_lists):
    print vehicle.id
    vehicle_length=vehicle.length
    vehicle_width=vehicle.width
    states= [[0] * int(vehicle_width*1000) for i in range(int(vehicle_length*1000))]


    for p in point_lists:
        p_l=point_lists[p]
        x_1=int(p_l[0][0]*1000)
        y_1=int(p_l[0][1]*1000)

        x_3=int(p_l[2][0]*1000)
        y_3=int(p_l[2][1]*1000)

        i=y_1
        while i < y_3:
            j=x_1
            while j<x_3:
                if states[i][j]==0:
                    states[i][j]=1
                else:
                    print states[i][j]
                    print "重叠"
                j+=1
            i+=1



def check_point_list(list1,list2):
    x_1=list1[0][0]
    x_2=list1[2][0]
    y_1 = list1[0][1]
    y_2 = list1[2][1]

    x_3 = list2[0][0]
    x_4 = list2[2][0]
    y_3=list2[0][1]
    y_4=list2[2][1]

    if x_1<=x_4 and x_2<=x_3 or (x_1>=x_4 and x_2 >= x_3):
        return True
    if y_1<=y_4 and y_2<=y_3 or (y_1>=y_4 and y_2 >= y_3 ):
        return True
    return False


def check_rect(point_lists):
    for i in range(len(point_lists)):
        j=i+1
        while j < len(point_lists):
            if check_point_list(point_lists[i],point_lists[j]) == False:
                print "重叠+++++"
            j+=1

if __name__=='__main__':
    test_result()