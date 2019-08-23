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


def resolveBinJson(path,map):
    file=open(path,"r")
    fileJson=json.load(file)
    #print(fileJson)

    vehicles_info = fileJson
    vehicle_list=[]

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
    cost,rate=geneticAlgm.cal_final_result(vehicle_list,map)
    print(cost, rate)


path = "../dataset/month3/"

print("enter")
map, time = createEntity.createMap(path + "matrix.json")
resolveBinJson("../result/new2.json",map)
