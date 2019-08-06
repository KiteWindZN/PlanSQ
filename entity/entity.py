class Station():
    id=""
    vehicle_limit=0
    loading_time=0
    binList=[]
    isEmpty=True
    weight=0.0
    area=0.0


    def __init__(self,id,vehicle_limit,loading_time):
        self.id=id
        self.vehicle_limit=vehicle_limit
        self.loading_time=loading_time
        self.binList=[]
        self.isEmpty=True
        self.weight=0.0
        self.area=0.0


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

    def __init__(self,id,length,width,weight):
        self.id=id
        self.length=length
        self.width=width
        self.weight=weight
        self.pointList=[]

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
        self.x=x
        self.y=y


class Line:

    def __init__(self,start,end,left_height,right_height):
        self.start=start
        self.end=end
        self.width=round(end.x-start.x,5)
        self.height=start.y
        self.left_height=left_height
        self.right_height=right_height
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

        self.length=righhtDown.x -leftDown.x
        self.width=leftUp.y - leftDown.y
        self.area= self.length * self.width
        self.isEmpty=False

    def check_empty(self):
        if self.length == 0 or self.width == 0:
            self.isEmpty=True

    def can_put_in(self,b):
        if b.length <= self.length and b.width <= self.width:
            return True
        return False
