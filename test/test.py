import matplotlib.pyplot as plt
import random
import json
from entity import entity
from process import geneticAlgm
from process import createEntity

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

colors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple']
fig = plt.figure()
ax = fig.add_subplot(111)
plt.xlim(0, 4)
plt.ylim(0, 5)
color_index=random.randint(1,100)
plt.gca().add_patch(plt.Rectangle((0.1, 0.1), 1,2,facecolor=colors[color_index%7]))
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

        for p in path:
            bin_list=info[p]
            #print (v_info,len(bin_list))
            i += len(bin_list)
            for b in bin_list:
                b_id=b

                if b_id not in bin_map:
                    bin_map[b_id]=1
                else:
                    bin_map[b_id] += 1
    for b in bins:
        b_id = b.id
        if b_id not in bin_map:
            print b_id,b.local_station
    cost,rate=geneticAlgm.cal_final_result(vehicle_list,map)
    print(cost, rate)
    print(len(bin_map),i)



path = "../dataset/month4/"

print("enter")
map, time = createEntity.createMap(path + "matrix.json")

stations, maxLimit = createEntity.createStation(path + "station.json")
#station_total=stations["S001"]

bins = createEntity.createBin(path + "bin.json", stations)
resolveBinJson("../result/913993.22866_2019-09-06-10:30:16-result.json",map,bins)
