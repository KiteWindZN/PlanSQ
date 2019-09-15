# -*- coding:utf-8 -*-
class Station():
    id=""
    vehicle_limit=0
    loading_time=0
    binList=[]
    isEmpty=True
    weight=0.0
    area=0.0
    label=0


    def __init__(self,id,vehicle_limit,loading_time):
        self.id=id
        self.vehicle_limit=vehicle_limit
        self.loading_time=loading_time
        self.binList=[]
        self.isEmpty=True
        self.weight=0.0
        self.area=0.0
        self.label=0


class Vehicle:
    id=0
    length=0.0
    width=0.0
    weight = 0.0
    startPrice=0.0
    perPrice=0.0
    usedTime=0.0 #已使用时间
    path=[]
    bin_list=[]
    lines=[]
    max_height=0.0
    used_weight=0.0
    station_bin={}
    is_available=True
    waste_area=[]

    def __init__(self,id,length,width,weight,sp,pp):
        self.id=id
        self.length=length
        self.width=width
        self.weight=weight
        self.startPrice=sp
        self.perPrice=pp
        self.usedTime=0.0
        self.path=[]
        self.bin_list=[]
        self.lines=[]
        self.max_height=0.0
        self.used_weight=0.0
        self.station_bin={}
        self.is_available = True
        self.waste_area=[]
        #self.init_lines()

    def add_path(self,station):
        self.path.append(station)

    def init_lines(self):
        s=Point(0,0)
        e=Point(self.width,0)
        left_height=self.length
        right_height=self.length
        line=Line(s,e,left_height,right_height)
        self.lines.append(line)

class Bin:
    id=0
    length=0.0
    width=0.0
    weight=0.0
    pointList=[]
    local_station=""

    def __init__(self,id,length,width,weight,s):
        self.id=id
        self.length=length
        self.width=width
        self.weight=weight
        self.pointList=[]
        self.local_station = s

    def set_pointList(self,leftDown,righhtDown,rightUp,leftUp):
        self.pointList.append(leftDown)
        self.pointList.append(righhtDown)
        self.pointList.append(rightUp)
        self.pointList.append(leftUp)

    def rotate_bin(self):
        tmp=self.width
        self.width=self.length
        self.length=tmp


class Point:
    x = 0.0
    y = 0.0

    def __init__(self,x,y):
        self.x=round(x,5)
        self.y=round(y,5)


class Line:

    def __init__(self,start,end,left_height,right_height):
        self.start=start
        self.end=end
        self.width=round(end.x-start.x,5)
        self.height=round(start.y,5)
        self.left_height=round(left_height,5)
        self.right_height=round(right_height,5)
        self.is_able=True


class Area:
    pointList=[]
    width=0.0
    length=0.0
    area=0.0
    isEmpty=False

    def __init__(self,leftDown,righhtDown,rightUp,leftUp):
        self.pointList.append(leftDown)
        self.pointList.append(righhtDown)
        self.pointList.append(rightUp)
        self.pointList.append(leftUp)

        self.length=round(righhtDown.x -leftDown.x,5)
        self.width=round(leftUp.y - leftDown.y,5)
        self.area= round(self.length * self.width,5)
        self.isEmpty=False

    def check_empty(self):
        if self.length == 0 or self.width == 0:
            self.isEmpty=True

    def can_put_in(self,b):
        if b.length <= self.length and b.width <= self.width:
            return True
        return False
