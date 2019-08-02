from entity import entity
import sys
#遗传算法
def genetic():
    print("genetic Algm")
#模拟退火算法
def simulated_annealing(bins,vehicle):
    T=10000
    a=0.9

#skyline算法
def skyline(vehicle,station):
    bins=station.binList
    station_id=station.id
    vehicle.station_bin[station_id]=[]
    vehicle_length=vehicle.length
    vehicle_width=vehicle.width
    lines=vehicle.lines
    start=entity.Point(0,0)
    end=entity.Point(0,vehicle_width)
    #line=entity.Line(start,end,vehicle_length,vehicle_length)
    max_height=0
    if len(lines)==0:
        choose = find_max_width(bins)
        #先放进一个最大的箱子
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
            vehicle.weight=vehicle.weight-bins[choose].weight
            max_height=bins[choose].length
            vehicle.used_weight = vehicle.used_weight+bins[choose].weight


    while max_height<vehicle_length:

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
        vehicle.used_weight = vehicle.used_weight+bin_list[final_bin].weight
        # 因为bin可能发生旋转，所以根据id在原始的bins中查找，最终删除放入vehicle的bin
        delete_bin(bins,bin_list[final_bin])

        if score == 12:
            #lines.remove(line)
            if lines[choose].left_height==lines[choose].right_height:
                if choose > 0 and choose+1 < len(lines):
                    lines[choose-1].end=lines[choose+1].end
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
        elif score == 5 or score == 4 :
            lines[choose].left_height=bin_list[final_bin].length
            # 多出一条线段
            tmp_start=entity.Point(lines[choose].start.x,lines[choose].start.y+bin_list[final_bin].length)
            tmp_end=entity.Point(tmp_start.x+bin_list[final_bin].width,tmp_start.y)
            #tmp_left_height=0.0
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

