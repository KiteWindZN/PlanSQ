from entity import entity
from process import createEntity
import sys
import random
#遗传算法
def genetic(bin_list,gene_num):
    print("genetic Algm")
    bin_len=len(bin_list)
    bin_index_list=[]
    gene_list=[]
    for i in range(gene_num):
        res=create_gene(bin_list)
        gene_list.append(res)


#注意消除冲突的问题
def cross_gene(gene1,gene2):
    gene_len=len(gene1)
    cross_start=random.randint(0,gene_len-1)
    i=cross_start
    while i< (gene_len-1):
        tmp=gene1[i]
        gene1[i]=gene2[i]
        gene2[i]=tmp
    #消除冲突
    list1=[]
    list2=[]
    change1=[]
    change2=[]

    for i in range(gene_len):
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
def create_gene(bin_list):
    bin_len = len(bin_list)
    bin_index_list = []
    res = []
    for i in range(bin_len):
        bin_index_list.append(i)
    i=0
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

#skyline算法，缺少组合装入和可装入的检测
def skyline(vehicle,station):
    bins=station.binList
    station_id=station.id
    vehicle.station_bin[station_id]=[]
    vehicle_length=vehicle.length
    vehicle_width=vehicle.width
    #lines中的线段按照严格的从左到右的顺序排列
    lines=vehicle.lines
    start=entity.Point(0,0)
    end=entity.Point(0,vehicle_width)
    #line=entity.Line(start,end,vehicle_length,vehicle_length)
    max_height=0
    #车辆的初始状态
    if len(lines)==0:
        choose = find_max_width(bins)
        #先放进一个宽度最大的箱子，目前没有发现有箱子的尺寸比车子还大，故此处的if语句恒为True
        if bins[choose].width <= vehicle_width and bins[choose].length <= vehicle_length:
            leftDown=entity.Point(0,0)
            rightDown=entity.Point(bins[choose].width,0)
            rightUp=entity.Point(bins[choose].width,bins[choose].length)
            leftUp=entity.Point(0,bins[choose].length)
            bins[choose].set_positionList(leftDown,rightDown,rightUp,leftUp)
            line1=entity.Line(leftUp,rightUp,vehicle_length-rightUp.y,vehicle_length-rightUp.y)
            line2=entity.Line(rightDown,end,leftUp.y,vehicle_length)
            lines.append(line1)
            lines.append(line2)
            vehicle[station_id].append(bins[choose])
            bins.remove(bins[choose])
            #vehicle.weight=vehicle.weight-bins[choose].weight
            vehicle.used_weight = vehicle.used_weight + bins[choose].weight
            max_height=bins[choose].length
            vehicle.used_weight = vehicle.used_weight+bins[choose].weight


    while max_height<vehicle_length and vehicle.used_weight < vehicle.weight and len(bins)>0:

        choose=find_lowest_line(lines)
        choose_bin=find_min_width(bins)

        while lines[choose].width < bins[choose_bin].width:
            lines[choose].is_able=False
            choose=find_lowest_line(lines)
        bin_list=[]
        for i in range(len(bins)):
            b=bin[i]
            if b.width < lines[choose].width:
                bin_list.append(b)
            elif b.length < lines[choose].width:
                bin_list.append(b)
        score=0
        final_bin=0
        for i in range(len(bin_list)):
            tmp_score1=gene_score(lines[choose],bin_list[i])
            tmp_score2=gene_score(lines[choose],bin_list[i].rotate())
            if tmp_score1 > tmp_score2: #再旋转回来
                bin_list.retate()
            tmp_score=max(tmp_score1,tmp_score2)
            if score<tmp_score:
                score = tmp_score
                final_bin=i
        #更新 max_height
        line=lines[choose]
        if bin_list[final_bin].length + line.height > max_height:
            max_height = bin_list[final_bin].length + line.height

        if score == 0:
            # 选择下一个line
            line.is_able = False
        # 把bin装入，计算四个点的坐标
        if score !=6 and score != 3 and score !=1:

            leftDown = entity.Point(lines[choose].start.x, lines[choose].start.y)
        else:
            leftDown = entity.Point(lines[choose].end.x-bin_list[final_bin].width,lines[choose].height)
        rightDown = entity.Point(leftDown.x + bin_list[final_bin].width, leftDown.y)
        rightUp = entity.Point(leftDown.x + bin_list[final_bin].width,
                               leftDown.y + bin_list[final_bin].length)
        leftUp = entity.Point(leftDown.x, leftDown.y + bin_list[final_bin].length)
        bin_list[final_bin].set_pointList(leftDown, rightDown, rightUp, leftUp)

        vehicle.bin_list.append(bin_list[final_bin])  # add to vehicle
        vehicle[station_id].append(bin_list[final_bin])
        #更新vehicle.used_weight
        vehicle.used_weight = vehicle.used_weight+bin_list[final_bin].weight
        # 因为bin可能发生旋转，所以根据id在原始的bins中查找，最终删除放入vehicle的bin
        delete_bin(bins,bin_list[final_bin])

        if score == 12:
            if lines[choose].left_height==lines[choose].right_height:
                if choose > 0 and choose+1 < len(lines):
                    lines[choose-1].end=entity.Point(lines[choose+1].end.x,lines[choose+1].end.y)
                    lines[choose-1].width = lines[choose-1].width + lines[choose].width + lines[choose+1].width
                    lines[choose-1].right_height=lines[choose+1].right_height

                    lines.remove(lines[choose])
                    lines.remove(lines[choose])
                else : #装满了整个车
                    max_height=vehicle_length

            elif choose > 0:
                lines[choose-1].end=entity.Point(line.end.x,line.height+bin_list[final_bin].length)
                if choose+1 == len(lines):
                    lines[choose + 1].left_height = lines[choose].height - lines[choose + 1].height

                lines[choose-1].height=lines[choose-1].width + lines[choose].width
                lines[choose-1].end.x=lines[choose].end.x
                lines[choose-1].width=lines[choose-1].width + lines[choose].width

                lines.remove(lines[choose])

            elif choose == 0:
                lines[choose+1].left_height=vehicle_length=lines[choose+1].height
                lines.remove(lines[choose])

        elif score == 11:
            lines[choose+1].start.x=lines[choose].start.x
            lines[choose+1].width=lines[choose].width + lines[choose+1].width
            lines[choose+1].left_height=lines[choose-1].height-lines[choose+1].height

            lines.remove(lines[choose])

        elif score == 10 or score == 9:

            lines[choose].start.y=lines[choose].start.y+bin_list[final_bin].length
            lines[choose].end.y=lines[choose].start.y
            lines[choose].height=lines[choose].start.y
            if lines[choose].height < lines[choose-1].height:
                lines[choose].height = lines[choose-1].height - lines[choose].height
            else:
                lines[choose].left_height=vehicle_length

            if lines[choose].height<lines[choose+1].height:
                lines[choose].right_height=lines[choose+1].height - lines[choose].height
            else:
                lines[choose].right_height=vehicle_length
                lines[choose+1].left_height=lines[choose]-lines[choose+1].height

        elif score == 8:

            lines[choose].start.y = lines[start].y + bin_list[final_bin].length
            lines[choose].end.y = lines[choose].start.y
            lines[choose].height = lines[choose].start.y
            lines[choose].left_height = lines[choose-1].height - lines[choose].height

        elif score == 7 :

            lines[choose].start.x = lines[choose].start.x + bin_list[final_bin].width

            lines[choose-1].end.x=lines[choose-1]+bin_list[final_bin].width
        elif score == 6:

            lines[choose].end.x = lines[choose].end.x-bin_list[final_bin].width
            lines[choose+1].start.x = lines[choose+1].start.x + bin_list[final_bin].width
        elif score == 5 or score == 4:
            lines[choose].left_height=bin_list[final_bin].length
            # 多出一条线段
            tmp_start=entity.Point(lines[choose].start.x,lines[choose].start.y+bin_list[final_bin].length)
            tmp_end=entity.Point(tmp_start.x+bin_list[final_bin].width,tmp_start.y)

            if tmp_start.y<lines[choose].height:
                tmp_left_height=lines[choose-1].height-tmp_start.y
            else:
                tmp_left_height=vehicle_length
            tmp_right_height=vehicle_length

            tmp_line=entity.Line(tmp_start,tmp_end,tmp_left_height,tmp_right_height)
            lines.index(choose,tmp_line)

        elif score == 3:
            lines[choose].end.x = lines[choose].end.x - bin_list[final_bin].width
            lines[choose].right_height = bin_list[final_bin].length

            tmp_start=entity.Point(lines[choose].end.x,lines[choose].end.y)
            tmp_end=entity.Point(tmp_start.x+bin_list[final_bin].width,tmp_start.y)

            tmp_left_height=vehicle_length
            if tmp_start.y < lines[choose+1].height:
                tmp_right_height = lines[choose+1].height - tmp_start.y
            else:
                tmp_right_height = vehicle_length
            tmp_line=entity.Line(tmp_start,tmp_end,tmp_left_height,tmp_right_height)
            lines.index(choose+1,tmp_line)

        elif score == 2:
            lines[choose-1].end.x= lines[choose-1].end.x + bin_list[final_bin].width
            lines[choose].start.x=lines[choose].start.x - bin_list[final_bin].width
        elif score == 1:
            lines[choose+1].start.x = lines[choose+1].start.x-bin_list[final_bin].width
            lines[choose].end.x = lines[choose].end.x + bin_list[final_bin].width
    #本站点的货物已经装完
    if len(bins)==0:
        station.isEmpty=True
    #如果max_height==vehicle.length则说明车厢已经装满，否则说明以下两种情况：
    # 1.站点的货物已经装载完
    # 2.车辆超重
    #这两种情况都可以通过检查车辆的状态来进一步判断，从而确定是否需要向此站点再派车辆，或者将此车辆继续调度
    return  max_height



#检查是否所有的站点的货物均已经装完
def is_finashed(stations):
    for s in stations:
        if s.isEmpty==False:
            return False
    return True

#根据bin的id在list中删除b
def delete_bin(bins,b):
    for i in range(len(bins)):
        if b.id == bins[i].id:
            bins.remove(bins[i])
            break;



def find_lowest_line(lines):
    h=sys.maxsize
    res=-1
    for i in range(len(lines)):
        if h> lines[i].height and lines[i].is_able==True:
            h=lines[i].height
            res=i
    return res

def find_max_width(bins):
    max_width=bins[0]
    res=0
    for i in range(len(bins)):
        if max_width<bins[i].width:
            max_width=bins[i].width
            res=i
    return res


def find_min_width(bins):
    min_width=bins[0]
    res=0

    for i in range(len(bins)):
        if min_width>bins[i].width:
            min_width=bins[i].width
            res=i
    return res



#对一种情况下，放入某一个货物bin进行打分
def gene_score(line,bin):

    l=bin.length
    w=bin.width
    a=0.1

    if w==line.width and l==line.left_height:
        score=12
    elif w==line.width and l==line.right_height:
        score=11
    elif w==line.width and (1-a) * line.left_height <= l and l > (1+a)*line.left_height :
        score = 10
    elif w==line.width and l>=(1+a)*line.left_height:
        score=19
    elif w==line.width and (1-a) * line.right_height <= l and (1+a)*line.right_height:
        score=8
    elif line.width*(1-a) < w < line.width and l==line.left_height:
        score=7
    elif line.width*(1-a) < w<line.width and l==line.right_height:
        score=6
    elif line.width*(1-a) < w < line.width and line.left_height(1-a) < l < line.left_height*(1+a):
        score=5
    elif line.width*(1-a) < w < line.width and l < line.left_height(1+a) :
        score=4
    elif line.width * (1-a) < w < line.width and line.right_height*(1-a) < l < line.right_height*(1+a):
        score=3
    elif w<=line.width * (1-a) and l == line.left_height:
        score=2
    elif w<=line.width * (1-a) and l == line.right_height:
        score=1
    else:
        score = 0

    return score


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


def schedule_vehicle_first(mst,T,vehicle_list,total_weight,stations):
    first_weight=total_weight * 0.7
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
        choose_vehicle_num=choose_vehicle(station_weight,vehicle_list)
        choose_vehicle = vehicle_list[choose_vehicle_num]

        #vehicle顺着树跑路
        while True:
            choose_vehicle.usedTime= choose_vehicle.usedTime + choose_station.loading_time
            choose_vehicle.path.append(choose_station_id)
            choose_vehicle.station_bin[choose_station_id]={}
            max_height=skyline(choose_vehicle,choose_station)
            #不需要调度的情况
            if max_height == choose_vehicle.length and len(choose_vehicle.bin_list)>0:
                break
            else:#随机选择下一个站点
                #使用时间范围内，可到达的station
                enable_stations = []
                next_stations = mst[choose_station]
                for s in next_stations:
                    if choose_vehicle.usedTime + T[choose_station_id][s] <= 600 and stations[s].isEmpty==False:
                        enable_stations.append(s)
                if len(next_stations) == 0:#临近节点都不可用,可能需要补充继续调度节点的操作，直到vehicle的使用率达到一定的比率
                    break

                choose_station_num=random.randint(0,len(enable_stations)-1)
                j=0
                for s in enable_stations:
                    if j== choose_station_num:
                        choose_station=stations[s]
                        choose_vehicle.usedTime = choose_vehicle.usedTime + T[choose_station_id][s]
                        break
    createEntity.update_stations(stations)

#第二次调度车辆，根据第一次的结果，按照100%的比例分配车辆
def schedule_vehicle_second(mst,T,vehicle_list,total_weight,stations):

#最后一次调度车辆，根据第二次的结果，计算当前节点的状态，一辆一辆的分配车辆，直到全部收集完所有的货物
def schedule_vehicle_final(mst,T,vehicle_list,total_weight,stations):


def choose_vehicle(weight,vehicle_list):
    for i in vehicle_list:
        if vehicle_list[i].weight > weight:
            return i
    return find_max_vehicle(vehicle_list)


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



def cal_cost_and_rate(vehicle,mst):
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
        distance = distance + mst[start][cur]
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
