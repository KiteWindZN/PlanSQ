# -*- coding:utf-8 -*-

from entity import entity
import geneticAlgm
import sys
import random
#skyline算法，缺少组合装入和可装入的检测
def skyline(vehicle,station):
    if vehicle.id == u"V898":
        print ( "11111")

    #vehicle.path.append(station.id)
    bins=station.binList
    for b in bins:
        if b.local_station not in vehicle.station_bin:
            vehicle.station_bin[b.local_station] = []

    vehicle_length=vehicle.length
    vehicle_width=vehicle.width
    #lines中的线段按照严格的从左到右的顺序排列
    lines=vehicle.lines
    max_height=vehicle.max_height
    for l in lines:
        l.is_able = True
    '''
    start=entity.Point(0,0)
    end=entity.Point(vehicle_width,0)
    #line=entity.Line(start,end,vehicle_length,vehicle_length)
    for l in lines:
        l.is_able=True
    max_height=vehicle.max_height
    #车辆的初始状态
    if len(lines)==0:
        choose = find_max_width_2(bins,vehicle_width,vehicle_length)
        #先放进一个宽度最大的箱子，目前没有发现有箱子的尺寸比车子还大，故此处的if语句恒为True
        if choose == -1:
            print "dddd"
        if bins[choose].width <= vehicle_width and bins[choose].length <= vehicle_length:
            #left_start_x=0
            #left_start_y=0
            leftDown=entity.Point(0,0)
            rightDown=entity.Point(bins[choose].width,0)
            rightUp=entity.Point(bins[choose].width,bins[choose].length)
            leftUp=entity.Point(0,bins[choose].length)
            #bins[choose].set_pointList(leftDown,rightDown,rightUp,leftUp)
            bins[choose].set_pointList(entity.Point(0,0), entity.Point(bins[choose].width,0),
                                       entity.Point(bins[choose].width, bins[choose].length),
                                       entity.Point(0,bins[choose].length))
            line1=entity.Line(leftUp,rightUp,vehicle_length-rightUp.y,vehicle_length-rightUp.y)
            line2=entity.Line(rightDown,end,leftUp.y,vehicle_length)
            lines.append(line1)
            lines.append(line2)
            vehicle.station_bin[bins[choose].local_station].append(bins[choose])
            vehicle.bin_list.append(bins[choose])
            #vehicle.weight=vehicle.weight-bins[choose].weight
            vehicle.used_weight = vehicle.used_weight + bins[choose].weight
            max_height=bins[choose].length
            bins.remove(bins[choose])


    '''

    while max_height<=vehicle_length and vehicle.used_weight <= vehicle.weight and len(bins)>0:

        #merge line fragment
        index=find_min_width(bins,vehicle)
        min_width=min(bins[index].width,bins[index].length)
        merge_line(lines,min_width,vehicle)
        #cal_lines(vehicle,lines)

        choose=find_lowest_line(lines)
        if choose == -1:
            #print (vehicle.id , station.id , choose)
            break
        choose_bin=find_min_width(bins,vehicle)

        while lines[choose].width < bins[choose_bin].width:
            #merge_lowest_line(vehicle,lines,choose)
            lines[choose].is_able=False
            choose=find_lowest_line(lines)
            if choose == -1:
                break;

        if choose == -1:
            break
        bin_list=[]
        for i in range(len(bins)):
            b=bins[i]
            if (b.weight + vehicle.used_weight) > vehicle.weight:
                continue
            if b.width <= lines[choose].width and b.length + lines[choose].height <= vehicle_length:
                bin_list.append(b)
            elif b.length <= lines[choose].width and b.width + lines[choose].height <= vehicle_length:
                b.rotate_bin()
                bin_list.append(b)
        score=0
        final_bin=0
        for i in range(len(bin_list)):
            if bin_list[final_bin].length+lines[choose].height > vehicle_length or bin_list[final_bin].width > lines[choose].width:
                tmp_score1=-1
            else:
                tmp_score1=gene_score(lines[choose],bin_list[i])
            if bin_list[final_bin].width+lines[choose].height > vehicle_length or bin_list[final_bin].length > lines[choose].width:
                tmp_score2=-1
            else:
                bin_list[i].rotate_bin()
                tmp_score2=gene_score(lines[choose],bin_list[i])

            if tmp_score1 > tmp_score2 and tmp_score2 != -1: #再旋转回来
                bin_list[i].rotate_bin()
            tmp_score=max(tmp_score1,tmp_score2)
            if score<tmp_score:
                score = tmp_score
                final_bin=i

        if len(bin_list) == 0:
            lines[choose].is_able=False
            continue

        line=lines[choose]

        if score == 0:
            # 选择下一个line
            #choose a bin and put it on the line
            # if we can merge two lines when their |height1-height2| < a
            final_bin=find_max_width_2(bin_list,line.width,vehicle_length-line.height)
            #if bin_list[final_bin].id == u"B13019":
            #    print (2222)

            if bin_list[final_bin].length + line.height > max_height:
                max_height = bin_list[final_bin].length + line.height
            #leftDown = entity.Point(lines[choose].end.x - bin_list[final_bin].width, lines[choose].height)
            leftDown = entity.Point(lines[choose].start.x,lines[choose].height)

            #left_start_x = round(lines[choose].end.x - bin_list[final_bin].width, 5)
            left_start_x=round(lines[choose].end.x ,5)
            left_start_y=lines[choose].height
            tmp_r_height = lines[choose].right_height
            #if lines[choose].end.x- bin_list[final_bin].width< 0:
            #    print(44444)


            bin_list[final_bin].set_pointList(entity.Point(leftDown.x, leftDown.y)
                                              , entity.Point(leftDown.x + bin_list[final_bin].width, leftDown.y)
                                              , entity.Point(leftDown.x + bin_list[final_bin].width, leftDown.y + bin_list[final_bin].length),
                                              entity.Point(leftDown.x, leftDown.y + bin_list[final_bin].length))

            vehicle.bin_list.append(bin_list[final_bin])  # add to vehicle
            vehicle.station_bin[bin_list[final_bin].local_station].append(bin_list[final_bin])
            # 更新vehicle.used_weight
            vehicle.used_weight = vehicle.used_weight + bin_list[final_bin].weight
            # 因为bin可能发生旋转，所以根据id在原始的bins中查找，最终删除放入vehicle的bin
            delete_bin(bins, bin_list[final_bin])

            lines[choose].start=entity.Point(leftDown.x,leftDown.y+bin_list[final_bin].length)
            lines[choose].end = entity.Point(leftDown.x+bin_list[final_bin].width, leftDown.y + bin_list[final_bin].length)
            lines[choose].height = round(lines[choose].start.y, 5)
            lines[choose].width = round(bin_list[final_bin].width, 5)

            tmp_start = entity.Point(lines[choose].end.x, left_start_y)
            tmp_end = entity.Point(left_start_x, left_start_y)

            tmp_left_height = round(bin_list[final_bin].length, 5)
            tmp_right_height = tmp_r_height
            '''
            lines[choose].end=entity.Point(leftDown.x,leftDown.y)
            lines[choose].right_height = bin_list[final_bin].length
            lines[choose].width=round(lines[choose].width - bin_list[final_bin].width,5)
            lines[choose].height = round(lines[choose].height,5)

            tmp_start=entity.Point(left_start_x,left_start_y+bin_list[final_bin].length)
            tmp_end=entity.Point(left_start_x+bin_list[final_bin].width,left_start_y+bin_list[final_bin].length)

            tmp_left_height=round(vehicle_length - tmp_end.y,5)
            if choose+1 < len(lines) and lines[choose+1].height-tmp_end.y > 0:
                tmp_right_height=round(lines[choose+1].height-tmp_end.y,5)
            else:
                tmp_right_height=round(vehicle_length-tmp_end.y,5)
            '''
            tmp_line=entity.Line(tmp_start,tmp_end,tmp_left_height,tmp_right_height)
            if choose+1 < len(lines):
                lines.insert(choose+1,tmp_line)
            else:
                lines.append(tmp_line)
            cal_lines(vehicle,lines)
            #line.is_able = False
            continue
        #if bin_list[final_bin].id == u"B13019":
        #    print(2222)
        # 更新 max_height
        if bin_list[final_bin].length + line.height > max_height:
            max_height = round(bin_list[final_bin].length + line.height,5)

        # 把bin装入，计算四个点的坐标
        if score !=6 and score != 3 and score !=1 and score != 3.5:
            #left_start_x = lines[choose].end.x
            #left_start_y = lines[choose].start.y

            leftDown_1 = entity.Point(lines[choose].start.x, lines[choose].start.y)
            bin_list[final_bin].set_pointList(entity.Point(lines[choose].start.x, lines[choose].start.y),
                                              entity.Point(lines[choose].start.x + bin_list[final_bin].width, lines[choose].start.y)
                                              , entity.Point(lines[choose].start.x + bin_list[final_bin].width, lines[choose].start.y + bin_list[final_bin].length),
                                              entity.Point(lines[choose].start.x, lines[choose].start.y + bin_list[final_bin].length))
        else:
            leftDown_1 = entity.Point(lines[choose].end.x-bin_list[final_bin].width,lines[choose].height)

            bin_list[final_bin].set_pointList(entity.Point(lines[choose].end.x-bin_list[final_bin].width,lines[choose].height),
                                          entity.Point(leftDown_1.x + bin_list[final_bin].width, leftDown_1.y)
                                          , entity.Point(leftDown_1.x + bin_list[final_bin].width,
                                                         leftDown_1.y + bin_list[final_bin].length),
                                          entity.Point(leftDown_1.x, leftDown_1.y + bin_list[final_bin].length))

        vehicle.bin_list.append(bin_list[final_bin])  # add to vehicle
        vehicle.station_bin[bin_list[final_bin].local_station].append(bin_list[final_bin])
        #更新vehicle.used_weight
        vehicle.used_weight = round(vehicle.used_weight+bin_list[final_bin].weight,5)
        # 因为bin可能发生旋转，所以根据id在原始的bins中查找，最终删除放入vehicle的bin
        delete_bin(bins,bin_list[final_bin])

        #print(bin_list[final_bin].id, "  ", score)
        if score == 12:
            if lines[choose].left_height==lines[choose].right_height:
                if choose > 0 and choose+1 < len(lines):
                    lines[choose-1].end=entity.Point(lines[choose+1].end.x,lines[choose+1].end.y)
                    lines[choose-1].width = round(lines[choose-1].width + lines[choose].width + lines[choose+1].width,5)
                    lines[choose-1].right_height=lines[choose+1].right_height

                    lines.remove(lines[choose])
                    lines.remove(lines[choose])
                else : #装满了整个车
                    max_height=vehicle_length
                    break

            elif choose > 0:
                lines[choose-1].end=entity.Point(line.end.x,line.height+bin_list[final_bin].length)
                if choose+1 < len(lines):
                    lines[choose + 1].left_height =round(lines[choose].height - lines[choose + 1].height,5)

                #lines[choose-1].height = round(lines[choose-1].width + lines[choose].width,5)
                lines[choose-1].end.x = lines[choose].end.x
                lines[choose-1].width = round(lines[choose-1].width + lines[choose].width,5)

                lines.remove(lines[choose])

            elif choose == 0:
                lines[choose+1].left_height=round(vehicle_length-lines[choose+1].height,5)
                lines.remove(lines[choose])

        elif score == 11:
            if choose+1 < len(lines):
                lines[choose+1].start.x=lines[choose].start.x
                lines[choose+1].width=round(lines[choose].width + lines[choose+1].width,5)
                if choose>0:
                    if lines[choose-1].height > lines[choose+1].height:
                        lines[choose+1].left_height=round(lines[choose-1].height-lines[choose+1].height,5)
                    else:
                        lines[choose + 1].left_height = round(vehicle_length - lines[choose + 1].height, 5)
                else:
                    lines[choose + 1].left_height = round(vehicle_length - lines[choose + 1].height, 5)

            lines.remove(lines[choose])

        elif score == 10 or score == 9:

            lines[choose].start.y=round(lines[choose].start.y+bin_list[final_bin].length,5)
            lines[choose].end.y=lines[choose].start.y
            lines[choose].height=lines[choose].start.y

            if choose == 0:
                lines[choose].left_height = round(vehicle_length - lines[choose].height,5)
                if choose+1 < len(lines):
                    if lines[choose].height < lines[choose+1].height:
                        lines[choose].right_height=round(lines[choose+1].height - lines[choose].height,5)
                        lines[choose+1].left_height = round(vehicle_length - lines[choose+1].height,5)
                    else:
                        lines[choose].right_height=round(vehicle_length-lines[choose].height,5)
                        lines[choose+1].left_height=round(lines[choose].height - lines[choose+1].height,5)
                else:
                    lines[choose].right_height = round(vehicle_length - lines[choose].height,5)

            elif choose > 0 and choose + 1 < len(lines):
                if lines[choose].height < lines[choose-1].height:
                    lines[choose].left_height = round(lines[choose-1].height - lines[choose].height,5)
                    lines[choose-1].right_height = round(vehicle_length - lines[choose-1].height,5)
                else:
                    lines[choose].left_height = round(vehicle_length-lines[choose].height,5)
                    lines[choose-1].right_height = round(lines[choose].height - lines[choose-1].height,5)

                if lines[choose].height < lines[choose+1].height:
                    lines[choose].right_height=round(lines[choose+1].height - lines[choose].height,5)
                    lines[choose+1].left_height = round(vehicle_length - lines[choose+1].height,5)
                else:
                    lines[choose].right_height=round(vehicle_length-lines[choose].height,5)
                    lines[choose+1].left_height=round(lines[choose].height - lines[choose+1].height,5)

            elif choose+1 == len(lines):
                lines[choose].right_height = round(vehicle_length - lines[choose].height,5)

                if lines[choose].height < lines[choose-1].height:
                    lines[choose].left_height = round(lines[choose-1].height - lines[choose].height,5)
                    lines[choose-1].right_height = round(vehicle_length - lines[choose-1].height,5)
                else:
                    lines[choose].left_height= round(vehicle_length-lines[choose].height,5)
                    lines[choose-1].right_height = round(lines[choose].height - lines[choose-1].height,5)

        elif score == 8 or score==5.5:

            lines[choose].start.y = round(lines[choose].start.y + bin_list[final_bin].length,5)
            lines[choose].end.y = lines[choose].start.y
            lines[choose].height = lines[choose].start.y
            if choose ==0:
                lines[choose].left_height = round(vehicle_length - lines[choose].height, 5)
            if choose > 0:
                if lines[choose-1].height < lines[choose].height:
                    lines[choose].left_height = round(vehicle_length - lines[choose].height, 5)
                    lines[choose-1].right_height =  round(lines[choose].height - lines[choose-1].height,5)
                else:
                    lines[choose].left_height = round(lines[choose-1].height - lines[choose].height, 5)
                    lines[choose-1].right_height = round(vehicle_length - lines[choose-1].height,5)
            if choose + 1 < len(lines):
                if lines[choose+1].height > lines[choose].height:
                    lines[choose].right_height = round(lines[choose+1].height - lines[choose].height,5)
                    lines[choose+1].left_height =round(vehicle_length - lines[choose+1].height,5)
                else:
                    lines[choose].right_height = round(vehicle_length - lines[choose].height,5)
                    lines[choose+1].left_height = round(lines[choose].height - lines[choose+1].height,5)
            if choose + 1 == len(lines):
                lines[choose].right_height = round(vehicle_length - lines[choose].height,5)


        elif score == 7 or score == 4.5:

            lines[choose].start.x =round(lines[choose].start.x + bin_list[final_bin].width,5)
            lines[choose].width = round(lines[choose].width - bin_list[final_bin].width,5)
            if choose >0:
                lines[choose-1].end.x= round(lines[choose-1].end.x+bin_list[final_bin].width,5)
                lines[choose-1].width = round(lines[choose-1].width + bin_list[final_bin].width,5)

        elif score == 6 or score == 3.5:

            lines[choose].end.x = round(lines[choose].end.x-bin_list[final_bin].width,5)
            lines[choose].width = round(lines[choose].width - bin_list[final_bin].width,5)
            if choose+1 < len(lines):
                lines[choose+1].start.x = round(lines[choose+1].start.x - bin_list[final_bin].width,5)
                lines[choose+1].width = round(lines[choose+1].width + bin_list[final_bin].width,5)
        elif score == 5 or score == 4:
            lines[choose].left_height=bin_list[final_bin].length

            # 多出一条线段
            tmp_start=entity.Point(lines[choose].start.x,lines[choose].start.y+bin_list[final_bin].length)
            tmp_end=entity.Point(tmp_start.x+bin_list[final_bin].width,tmp_start.y)

            if tmp_start.y<lines[choose-1].height:
                tmp_left_height=round( lines[choose-1].height-tmp_start.y,5)
            else:
                tmp_left_height=round(vehicle_length-tmp_start.y,5)
                lines[choose-1].right_height = round(tmp_start.y - lines[choose-1].height,5)
            tmp_right_height=round(vehicle_length-tmp_start.y,5)

            tmp_line=entity.Line(tmp_start,tmp_end,tmp_left_height,tmp_right_height)
            lines[choose].start.x = round(lines[choose].start.x + bin_list[final_bin].width,5)
            lines[choose].width = round(lines[choose].width-bin_list[final_bin].width,5)
            lines.insert(choose,tmp_line)

        elif score == 3:
            lines[choose].end.x = round(lines[choose].end.x - bin_list[final_bin].width,5)
            lines[choose].right_height = round(bin_list[final_bin].length,5)
            lines[choose].width = round(lines[choose].width - bin_list[final_bin].width,5)

            tmp_start=entity.Point(lines[choose].end.x,lines[choose].end.y+bin_list[final_bin].length)
            tmp_end=entity.Point(tmp_start.x+bin_list[final_bin].width,tmp_start.y)

            tmp_left_height = round(vehicle_length- tmp_start.y,5)
            if choose+1 == len(lines):
                tmp_right_height = round(vehicle_length - tmp_start.y,5)
            elif tmp_start.y < lines[choose+1].height:
                tmp_right_height = round(lines[choose+1].height - tmp_start.y,5)
            else:
                tmp_right_height = round(vehicle_length - tmp_start.y,5)
            tmp_line=entity.Line(tmp_start,tmp_end,tmp_left_height,tmp_right_height)
            lines.insert(choose+1,tmp_line)

        elif score == 2:
            if choose > 0:
                lines[choose-1].end.x=round(lines[choose-1].end.x + bin_list[final_bin].width,5)
                lines[choose - 1].width = round(lines[choose - 1].width + bin_list[final_bin].width, 5)
            else:
                tmp_start=entity.Point(0,vehicle_length)
                tmp_end=entity.Point(bin_list[final_bin].width,vehicle_length)
                '''
                lines.insert(0,entity.Line(tmp_start,tmp_end,0,0))
            if choose == 0:
                choose = 1
            '''
            lines[choose].start.x=round(lines[choose].start.x + bin_list[final_bin].width,5)
            lines[choose].width = round(lines[choose].width-bin_list[final_bin].width,5)
        elif score == 1:
            if choose+1 < len(lines):
                lines[choose+1].start.x =round(lines[choose+1].start.x-bin_list[final_bin].width,5)
                lines[choose+1].width = round(lines[choose+1].width + bin_list[final_bin].width,5)
            else:
                tmp_start = entity.Point(lines[choose].end.x-bin_list[final_bin].width,vehicle_length)
                tmp_end = entity.Point(lines[choose].end.x, vehicle_length)
                #lines.append(entity.Line(tmp_start,tmp_end,0,0))
            lines[choose].end.x = round(lines[choose].end.x - bin_list[final_bin].width,5)
            lines[choose].width = round(lines[choose].width - bin_list[final_bin].width,5)

    #本站点的货物已经装完
    if len(bins)==0:
        station.isEmpty=True
    #如果max_height==vehicle.length则说明车厢已经装满，否则说明以下两种情况：
    # 1.站点的货物已经装载完
    # 2.车辆超重
    #这两种情况都可以通过检查车辆的状态来进一步判断，从而确定是否需要向此站点再派车辆，或者将此车辆继续调度
    vehicle.max_height=max_height
    return max_height


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
        if h > lines[i].height and lines[i].is_able==True:
            h=lines[i].height
            res=i
    return res


def find_max_width_2(bins,width,height):
    max=0
    res=-1
    for i in range(len(bins)):
        b=bins[i]
        if b.width<= width and b.length <= height:
            if max < b.width:
                max = b.width
                res=i
        if b.length <= width and b.width <= height:
            if max < b.length:
                max=b.length
                b.rotate_bin()
                res=i
    return res

def find_max_width(bins):
    max_width=bins[0].width
    res=0
    for i in range(len(bins)):
        if max_width<bins[i].width:
            max_width=bins[i].width
            res=i
    return res


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

# merge line fragment
def merge_line(lines,min_width,vehicle):
    N=len(lines)
    if N <= 1:
        return
    i=0

    for line in lines:
        line.width = round(line.end.x - line.start.x, 5)
        if line.width == 0:
            lines.remove(line)
    N=len(lines)
    if N <= 1:
        return

    res=-1
    tmp_len=sys.maxsize
    for i in range(N):
        if tmp_len > lines[i].height:
            tmp_len = lines[i].height
            res=i
    i=0
    while i < N:
    #if i==res:
        if N==1:
            break

        cur_width=lines[i].width
        if cur_width < min_width: #merge

            if i == 0:
                if lines[i].height < lines[i+1].height:
                    lines[i+1].start.x=round(lines[i].start.x,5)
                    #lines[i+1].left_height =round( vehicle.length-lines[i+1].height,5)
                    lines[i+1].width = round(lines[i].width+lines[i+1].width,5)
                    lines[i+1].is_able=True
                    cal_waste_area(vehicle, lines[i])
                    lines.remove(lines[i])
                    cal_lines(vehicle, lines)
                    i = i - 1
                else:
                    if lines[i].height - lines[i+1].height >0.5:
                        i=i+1
                        continue
                    lines[i].end.x=round(lines[i+1].end.x,5)
                    lines[i].width = round(lines[i].width + lines[i + 1].width, 5)
                    lines[i].is_able = True

                    if i+2<len(lines):
                        if lines[i+2].height>lines[i].height:
                            lines[i].right_height = round(lines[i+2].height - lines[i].height, 5)
                            lines[i+2].left_height = round(vehicle.length - lines[i+2].height, 5)
                        elif lines[i+2].height<lines[i].height:
                            lines[i].right_height = round(vehicle.length - lines[i].height, 5)
                            lines[i + 2].left_height = round(lines[i].height - lines[i + 2].height, 5)
                        else:
                            lines[i].end.x=lines[i+2].end.x
                            lines[i].width = round(lines[i].width + lines[i + 2].width, 5)
                            lines[i].right_height = lines[i+2].right_height
                            lines.remove(lines[i + 2])
                        cal_waste_area(vehicle, lines[i+1])
                        lines.remove(lines[i + 1])

                    else:
                        lines[i].right_height = round(vehicle.length - lines[i].height, 5)
                        cal_waste_area(vehicle, lines[i + 1])
                        lines.remove(lines[i+1]) #####
                        cal_lines(vehicle, lines)


            elif i == N-1:

                if lines[i].height>lines[i-1].height:
                    if lines[i].height - lines[i-1].height >0.5:
                        i=i+1
                        continue
                    else:
                    #if lines[i-1].width < min_width:#merge
                        cal_waste_area(vehicle, lines[i - 1])
                        lines[i-1].start.y = lines[i].start.y
                        lines[i-1].end.y= lines[i].start.y
                        lines[i-1].end.x = lines[i].end.x
                        lines[i-1].width = round(lines[i-1].width + lines[i].width,5)
                        lines[i-1].height = lines[i-1].start.y
                        lines[i-1].right_height = lines[i].right_height
                        lines[i-1].is_able = True
                        lines.remove(lines[i])
                        cal_lines(vehicle, lines)
                        i=i-1
                    #else:
                    #    print("TODO")
                else:
                    lines[i-1].end.x = lines[i].end.x
                    lines[i-1].width = round(lines[i-1].width + lines[i].width,5)
                    lines[i-1].right_height = round(vehicle.length-lines[i-1].height,5)
                    lines[i-1].is_able = True
                    cal_waste_area(vehicle, lines[i])

                    lines.remove(lines[i])
                    cal_lines(vehicle, lines)
                    i=i-1
            else:
                if lines[i-1].height < lines[i+1].height:
                    if lines[i-1].height > lines[i].height:
                        lines[i-1].width = round(lines[i-1].width + lines[i].width,5)
                        lines[i-1].end.x=lines[i].end.x
                        lines[i-1].right_height = round(lines[i+1].height - lines[i-1].height,5)
                        lines[i+1].left_height = round(vehicle.length - lines[i+1].height,5)
                        lines[i-1].is_able = True
                        cal_waste_area(vehicle, lines[i])
                        lines.remove(lines[i])
                        cal_lines(vehicle, lines)
                        i=i-1
                    else:
                        lines[i].start.x = lines[i-1].start.x
                        cal_waste_area(vehicle, lines[i-1])
                        flag=0
                        if i-1 == 0:
                            lines[i].left_height = round(vehicle.length - lines[i].height,5)
                        else:
                            flag=0
                            if lines[i-2].height < lines[i].height:
                                lines[i].left_height = round(vehicle.length - lines[i].height,5)
                                lines[i-2].right_height = round(lines[i].height - lines[i-2].height,5)
                            elif lines[i-2].height > lines[i].height:
                                lines[i].left_height = round(lines[i-2].height - lines[i].height,5)
                                lines[i - 2].right_height = round(vehicle.length - lines[i - 2].height,5)
                            else:
                                lines[i].left_height = lines[i-2].left_height
                                lines[i].width = round(lines[i - 2].width + lines[i].width, 5)
                                lines[i].start.x= lines[i-2].start.x

                                lines.remove(lines[i-2])
                                flag=1

                        lines[i].width = round(lines[i - 1].width + lines[i].width, 5)
                        lines[i].is_able = True
                        lines.remove(lines[i-1])
                        cal_lines(vehicle, lines)
                        i=i-1
                        if flag == 1:
                            i=i-1
                elif lines[i-1].height == lines[i+1].height:
                    if lines[i].height < lines[i-1].height:
                        lines[i-1].width = round(lines[i-1].width + lines[i].width + lines[i+1].width,5)
                        lines[i-1].end.x = lines[i+1].end.x
                        lines[i-1].right_height = lines[i+1].right_height
                        lines[i-1].is_able=True
                        cal_waste_area(vehicle, lines[i])
                        lines.remove(lines[i])
                        lines.remove(lines[i])
                        cal_lines(vehicle, lines)
                        i=i-2

                else:
                    if lines[i].height< lines[i+1].height:
                        lines[i+1].start.x = lines[i].start.x
                        lines[i+1].width = round(lines[i].width+lines[i+1].width,5)

                        lines[i-1].right_height = round(vehicle.length - lines[i-1].height,5)
                        lines[i+1].left_height = round(lines[i-1].height - lines[i+1].height,5)
                        lines[i+1].is_able=True
                        cal_waste_area(vehicle, lines[i])
                        lines.remove(lines[i])
                        cal_lines(vehicle, lines)
                        i=i-1
                    else:
                        if lines[i+1].start.x == 5.6 and lines[i+1].start.y==1.28:
                            print("cccc")
                        lines[i].end.x = lines[i+1].end.x
                        lines[i].width = round(lines[i].width+lines[i+1].width,5)
                        lines[i].right_height = lines[i+1].right_height
                        lines[i].is_able=True

                        cal_waste_area(vehicle, lines[i+1])
                        lines.remove(lines[i+1])
                        cal_lines(vehicle, lines)

        i=i+1
        N=len(lines)

    for line in lines:
        line.width= round(line.end.x - line.start.x,5)
        if line.width ==0:
            lines.remove(line)
    lines[0].left_height = round(vehicle.length - lines[0].height,5)

    i=1
    while i < len(lines):
        if lines[i-1].height>lines[i].height:
            lines[i-1].right_height =round(vehicle.length - lines[i-1].height,5)
            lines[i].left_height = round(lines[i-1].height - lines[i].height,5)
        else:
            lines[i - 1].right_height = round(lines[i].height - lines[i - 1].height,5)
            lines[i].left_height = round(vehicle.length - lines[i].height,5)
        i = i+1
    i=len(lines)
    lines[i-1].right_height=round(vehicle.length - lines[i-1].height,5)


def cal_lines(vehicle,lines):
    for line in lines:
        line.width= round(line.end.x - line.start.x,5)
        if line.width ==0:
            lines.remove(line)

    i=1
    N = len(lines)
    while i < N:
        if lines[i].start.y ==lines[i-1].end.y:
            lines[i].start.x = lines[i-1].start.x
            lines[i].width = round(lines[i-1].width+lines[i].width,5)
            lines.remove(lines[i-1])
            i=i-1
        i=i+1
        N=len(lines)

    lines[0].left_height = round(vehicle.length - lines[0].height,5)

    i=1
    while i < len(lines):
        if lines[i-1].height>lines[i].height:
            lines[i-1].right_height =round(vehicle.length - lines[i-1].height,5)
            lines[i].left_height = round(lines[i-1].height - lines[i].height,5)
        else:
            lines[i - 1].right_height = round(lines[i].height - lines[i - 1].height,5)
            lines[i].left_height = round(vehicle.length - lines[i].height,5)
        i = i+1
    i=len(lines)
    lines[i-1].right_height=round(vehicle.length - lines[i-1].height,5)


def cal_waste_area(vehicle,line):
    #tmp_start=entity.Point(line.start.x,line.start.y)
    #tmp_end=entity.Point(line.end.x,line.end.y)
    tmp_left_height=min(line.left_height,line.right_height)
    tmp_right_height=tmp_left_height

    tmp_line=entity.Line(entity.Point(line.start.x,line.start.y),entity.Point(line.end.x,line.end.y),tmp_left_height,tmp_right_height)
    if tmp_line.width>=0.03 and tmp_line.left_height>=0.03:
        vehicle.waste_area.append(tmp_line)


def make_new_binList(station,q):
    bin_list=station.binList
    new_list=[]

    for i in range(len(bin_list)):
        j = random.randint(0,len(bin_list)-1)
        tmp_rate=random.random()
        while tmp_rate>q or bin_list[j] in new_list:
            j = (j+1) % len(bin_list)
            tmp_rate = random.random()
        new_list.append(bin_list[j])
    station.binList=[]
    station.binList=new_list


def merge_lowest_line(vehicle,lines,index):
    if len(lines) == 1:
        print(1111)
        lines[index].is_able=False
        return
    if index == 0:
        lines[index+1].start.x=lines[index].start.x
        lines[index+1].width = round(lines[index+1].width+lines[index].width,5)
    elif index == len(lines)-1:
        lines[index-1].end.x = lines[index].end.x
        lines[index - 1].width = round(lines[index - 1].width + lines[index].width, 5)
    else:
        if lines[index-1].height < lines[index+1].height:
            lines[index - 1].end.x = lines[index].end.x
            lines[index - 1].width = round(lines[index - 1].width + lines[index].width, 5)
        elif lines[index-1].height < lines[index+1].height:
            lines[index - 1].end.x = lines[index+1].end.x
            lines[index - 1].width = round(lines[index - 1].width + lines[index].width+lines[index+1].width, 5)
            lines.remove(lines[index+1])
        else:
            lines[index + 1].start.x = lines[index].start.x
            lines[index + 1].width = round(lines[index + 1].width + lines[index].width, 5)
    lines[index-1].is_able=True
    cal_waste_area(vehicle,lines[index])
    lines.remove(lines[index])
    cal_lines(vehicle,lines)


#对一种情况下，放入某一个货物bin进行打分
def gene_score(line,bin):

    l=bin.length
    w=bin.width

    a=0.2


    if w==line.width and l==line.left_height:
        score=12
    elif w==line.width and l==line.right_height:
        score=11
    elif w==line.width and (1-a) * line.left_height <= l < (1+a)*line.left_height :
        score = 10
    elif w==line.width and l >= (1+a)*line.left_height:
        score=9
    elif w==line.width and (1-a) * line.right_height <= l < (1+a)*line.right_height:
        score=8
    elif line.width*(1-a) < w < line.width and l==line.left_height:
        score=7
    elif line.width*(1-a) < w < line.width and l==line.right_height:
        score=6
    elif w==line.width:
        score = 5.5

    elif l == line.left_height:
        score = 4.5
    elif l == line.right_height:
        score = 3.5

    elif line.width*(1-a) < w < line.width and line.left_height*(1-a) < l < line.left_height*(1+a):
        score=5
    elif line.width*(1-a) < w < line.width and l >= line.left_height*(1+a):
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


def add_bin(lines,choose_line,bin,vehicle):
    vehicle_length=vehicle.length
    line=lines[choose_line]

    if bin.width == line.width:
        leftDown = entity.Point(line.start.x,line.start.y)

        line.start.y = line.start.y + bin.length
        line.end.y = line.start.y
        line.height = line.start.y
        if choose_line != len(lines)-1:
            if choose_line+1 < len(lines) and line.height < lines[choose_line+1].height:
                line.right_height = lines[choose_line+1].height - line.height
                lines[choose_line+1].left_height = vehicle_length - lines[choose_line+1].height
            elif choose_line+1 < len(lines) and line.height > lines[choose_line+1].height:
                line.right_height = vehicle_length - line.height
                lines[choose_line + 1].left_height = line.height - lines[choose_line + 1].height
        if choose_line != 0:
            if lines[choose_line - 1].height < lines[choose_line].height:
                lines[choose_line].left_height = round(vehicle_length - lines[choose_line].height, 5)
                lines[choose_line - 1].right_height = round(lines[choose_line].height - lines[choose_line - 1].height,5)
            else:
                lines[choose_line].left_height = round(lines[choose_line - 1].height - lines[choose_line].height, 5)
                lines[choose_line - 1].right_height = round(vehicle_length - lines[choose_line - 1].height,5)

        if choose_line == 0:
            line.left_height = vehicle_length - line.height

        if choose_line+1 < len(lines):
            line.right_height = vehicle_length -line.height

    else:
        if line.right_height == bin.length: #right
            leftDown = entity.Point(line.end.x-bin.width,line.end.y)

            lines.end.x = line.end.x - bin.width
            line.height = line.start.y
            line.width = line.width - bin.width
            line.right_height = bin.length
            if choose_line < len(lines)-1:
                lines[choose_line+1].start.x = line.end.x
                lines[choose_line+1].width = lines[choose_line+1].width + bin.width

        else:#left
            leftDown = entity.Point(line.start.x, line.start.y)
            if bin.length == line.left_height:
                if choose_line > 0:
                    lines[choose_line - 1].end.x = lines[choose_line-1].end.x + bin.width
                    lines[choose_line - 1].width = lines[choose_line - 1].width + bin.width
                line.start.x= line.start.x + bin.width
                line.width =line.width - bin.width
            else:

                tmp_start = entity.Point(line.start.x,line.start.y+bin.length)
                tmp_end = entity.Point(tmp_start.x+bin.width,tmp_start.y)
                tmp_right = vehicle_length - tmp_start.y
                if bin.length < line.left_height:
                    tmp_left = line.left_height - bin.length
                else:
                    tmp_left = vehicle_length - bin.length
                    if choose_line >0:
                        lines[choose_line-1] = tmp_start.y - lines[choose_line-1].height
                tmp_line = entity.Line(tmp_start,tmp_end,tmp_left,tmp_right)
                line.start.x = line.start.x + bin.width
                line.width = line.width - bin.width
                line.left_height=bin.length

                lines.insert(choose_line,tmp_line)

    bin.set_pointList(entity.Point(leftDown.x, leftDown.y),
                      entity.Point(leftDown.x + bin.width, leftDown.y),
                      entity.Point(leftDown.x + bin.width, leftDown.y + bin.length),
                      entity.Point(leftDown.x, leftDown.y + bin.length))
    merge_line_add(lines) # merge adjacent lines with the same height


def merge_line_add(lines):
    N=len(lines)
    i=0
    while i < N-1:

        line_1=lines[i]
        line_2=lines[i+1]
        if line_1.width == 0:
            lines.remove(line_1)
            break
        if line_2.width == 0:
            lines.remove(line_2)
            break
        if line_1.height == line_2.height:#merge
            line_1.end.x=line_2.end.x
            line_1.width = line_1.width +line_2.width
            line_1.right_height = line_2.right_height

            lines.remove(line_2)
            i=i-1

        i = i+1
        N=len(lines)
    line = lines[len(lines)-1]
    if line.width ==0:
        lines.remove(line)


def pre_skyline(vehicle,station):

    vehicle.path.append(station.id)
    bins=station.binList

    #station_id=station.id
    vehicle_1 = geneticAlgm.create_new_vehicle(vehicle)
    vehicle_2 = geneticAlgm.create_new_vehicle(vehicle)

    for b in bins:
        if b.local_station not in vehicle.station_bin:
            vehicle_1.station_bin[b.local_station] = []
            vehicle_2.station_bin[b.local_station] = []
            vehicle.station_bin[b.local_station] = []
    vehicle_1.path.append(station.id)
    vehicle_2.path.append(station.id)

    vehicle_length=vehicle.length
    vehicle_width=vehicle.width
    #lines中的线段按照严格的从左到右的顺序排列
    lines=vehicle.lines

    end=entity.Point(vehicle_width,0)


    #车辆的初始状态
    if len(lines)==0:
        choose = find_max_width_2(bins,vehicle_width,vehicle_length)

        #先放进一个宽度最大的箱子，目前没有发现有箱子的尺寸比车子还大，故此处的if语句恒为True
        if choose == -1:
            print "dddd"
        if bins[choose].length < vehicle_width and bins[choose].width <= vehicle_length:
            b=geneticAlgm.create_new_bin(bins[choose])
            b.rotate_bin()
            b.set_pointList(entity.Point(0, 0), entity.Point(b.width, 0),
                                       entity.Point(b.width, b.length),
                                       entity.Point(0, b.length))
            rightDown1 = entity.Point(b.width, 0)
            rightUp1 = entity.Point(b.width, b.length)
            leftUp1 = entity.Point(0, b.length)
            line11 = entity.Line(leftUp1, rightUp1, vehicle_length - rightUp1.y, vehicle_length - rightUp1.y)
            line12 = entity.Line(rightDown1, end, leftUp1.y, vehicle_length)
            vehicle_1.lines.append(line11)
            vehicle_1.lines.append(line12)
            vehicle_1.station_bin[b.local_station].append(bins[choose])
            vehicle_1.bin_list.append(b)
            # vehicle.weight=vehicle.weight-bins[choose].weight
            vehicle_1.used_weight = vehicle_1.used_weight + b.weight
            vehicle_1.max_height = b.length

        if bins[choose].width <= vehicle_width and bins[choose].length <= vehicle_length:

            rightDown=entity.Point(bins[choose].width,0)
            rightUp=entity.Point(bins[choose].width,bins[choose].length)
            leftUp=entity.Point(0,bins[choose].length)
            #bins[choose].set_pointList(leftDown,rightDown,rightUp,leftUp)
            bins[choose].set_pointList(entity.Point(0,0), entity.Point(bins[choose].width,0),
                                       entity.Point(bins[choose].width, bins[choose].length),
                                       entity.Point(0,bins[choose].length))
            line1=entity.Line(leftUp,rightUp,vehicle_length-rightUp.y,vehicle_length-rightUp.y)
            line2=entity.Line(rightDown,end,leftUp.y,vehicle_length)
            vehicle_2.lines.append(line1)
            vehicle_2.lines.append(line2)
            vehicle_2.station_bin[bins[choose].local_station].append(bins[choose])
            vehicle_2.bin_list.append(bins[choose])
            #vehicle.weight=vehicle.weight-bins[choose].weight
            vehicle.used_weight = vehicle.used_weight + bins[choose].weight
            vehicle_2.max_height=bins[choose].length
            bins.remove(bins[choose])
        return vehicle_1,vehicle_2



def process_skyline(vehicle,station):
    if len(vehicle.bin_list) == 0:

        vehicle_1,vehicle_2 = pre_skyline(vehicle,station)
        station_1 = geneticAlgm.create_new_station(station)
        station_2 = geneticAlgm.create_new_station(station)

        skyline(vehicle_1,station_1)
        skyline(vehicle_2,station_2)

        if geneticAlgm.cal_used_rate(vehicle_1) > geneticAlgm.cal_used_rate(vehicle_2):
            vehicle=vehicle_1
            station=station_1
            return vehicle_1.max_height,vehicle_1,station_1
        else:
            vehicle=vehicle_2
            station=station_2
            return vehicle_2.max_height,vehicle_2,station_2
    else:
        vehicle.path.append(station.id)

        skyline(vehicle,station)
        return vehicle.max_height ,vehicle, station