# -*- coding:utf-8 -*-
from process import geneticAlgm
from entity import entity
from process import skyLine

#skyline算法，缺少组合装入和可装入的检测
def multi_skyline(vehicle,station_list,stations):
    if vehicle.id == u"V657" :
        print ( "11111")
    bins = []
    for s in station_list:
        bins1 = s.binList
        vehicle.path.append(s.id)
        vehicle.station_bin[s.id] = []
        for b in bins1:
            bins.append(b)

    vehicle_length=vehicle.length
    vehicle_width=vehicle.width
    #lines中的线段按照严格的从左到右的顺序排列
    lines=vehicle.lines
    start=entity.Point(0,0)
    end=entity.Point(vehicle_width,0)
    #line=entity.Line(start,end,vehicle_length,vehicle_length)
    for l in lines:
        l.is_able=True
    max_height=vehicle.max_height
    #车辆的初始状态
    if len(lines)==0:
        choose = skyLine.find_max_width_2(bins,vehicle_width,vehicle_length)
        #先放进一个宽度最大的箱子，目前没有发现有箱子的尺寸比车子还大，故此处的if语句恒为True
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

            skyLine.delete_bin(stations[bins[choose].local_station].binList,bins[choose])
            bins.remove(bins[choose])



    while max_height<=vehicle_length and vehicle.used_weight <= vehicle.weight and len(bins)>0:

        #merge line fragment
        index=geneticAlgm.find_min_width(bins,vehicle)
        min_width=min(bins[index].width,bins[index].length)
        skyLine.merge_line(lines,min_width,vehicle)

        choose=skyLine.find_lowest_line(lines)
        if choose == -1:
            #print (vehicle.id , station.id , choose)
            break
        choose_bin=geneticAlgm.find_min_width(bins,vehicle)

        while lines[choose].width < bins[choose_bin].width:
            lines[choose].is_able=False
            choose=skyLine.find_lowest_line(lines)
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
                tmp_score1=skyLine.gene_score(lines[choose],bin_list[i])
            if bin_list[final_bin].width+lines[choose].height > vehicle_length or bin_list[final_bin].length > lines[choose].width:
                tmp_score2=-1
            else:
                bin_list[i].rotate_bin()
                tmp_score2=skyLine.gene_score(lines[choose],bin_list[i])

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
            final_bin=skyLine.find_max_width_2(bin_list,line.width,vehicle_length-line.height)
            #if bin_list[final_bin].id == u"B13019":
            #    print (2222)

            if bin_list[final_bin].length + line.height > max_height:
                max_height = bin_list[final_bin].length + line.height
            leftDown = entity.Point(lines[choose].end.x - bin_list[final_bin].width, lines[choose].height)


            left_start_x=round(lines[choose].end.x - bin_list[final_bin].width,5)
            left_start_y=lines[choose].height

            #if lines[choose].end.x- bin_list[final_bin].width< 0:
            #    print(44444)


            bin_list[final_bin].set_pointList(entity.Point(lines[choose].end.x - bin_list[final_bin].width, lines[choose].height)
                                              , entity.Point(leftDown.x + bin_list[final_bin].width, leftDown.y)
                                              , entity.Point(leftDown.x + bin_list[final_bin].width, leftDown.y + bin_list[final_bin].length),
                                              entity.Point(leftDown.x, leftDown.y + bin_list[final_bin].length))

            vehicle.bin_list.append(bin_list[final_bin])  # add to vehicle
            vehicle.station_bin[bin_list[final_bin].local_station].append(bin_list[final_bin])
            # 更新vehicle.used_weight
            vehicle.used_weight = vehicle.used_weight + bin_list[final_bin].weight
            # 因为bin可能发生旋转，所以根据id在原始的bins中查找，最终删除放入vehicle的bin

            skyLine.delete_bin(bins, bin_list[final_bin])
            skyLine.delete_bin(stations[bin_list[final_bin].local_station].binList, bin_list[final_bin])

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
            tmp_line=entity.Line(tmp_start,tmp_end,tmp_left_height,tmp_right_height)
            if choose+1 < len(lines):
                lines.insert(choose+1,tmp_line)
            else:
                lines.append(tmp_line)

            #line.is_able = False
            continue
        #if bin_list[final_bin].id == u"B13019":
        #    print(2222)
        # 更新 max_height
        if bin_list[final_bin].length + line.height > max_height:
            max_height = round(bin_list[final_bin].length + line.height,5)

        # 把bin装入，计算四个点的坐标
        if score !=6 and score != 3 and score !=1:
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
        skyLine.delete_bin(bins,bin_list[final_bin])

        skyLine.delete_bin(stations[bin_list[final_bin].local_station].binList, bin_list[final_bin])

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
                    lines[choose-1].right = round(lines[choose].height - lines[choose-1].height,5)

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
                    lines[choose-1].righ_height = round(vehicle_length - lines[choose-1].height,5)
            if choose + 1 < len(lines):
                if lines[choose+1].height > lines[choose].height:
                    lines[choose].right_height = round(lines[choose+1].height - lines[choose].height,5)
                    lines[choose+1].left_height =round(vehicle_length - lines[choose+1].height,5)
                else:
                    lines[choose].right_height = round(vehicle_length - lines[choose].height,5)
                    lines[choose+1].left_height = round(lines[choose].height - lines[choose+1].height,5)
            if choose + 1 == len(lines):
                lines[choose].right_height = round(vehicle_length - lines[choose].height,5)


        elif score == 7 :

            lines[choose].start.x =round(lines[choose].start.x + bin_list[final_bin].width,5)
            lines[choose].width = round(lines[choose].width - bin_list[final_bin].width,5)
            if choose >0:
                lines[choose-1].end.x= round(lines[choose-1].end.x+bin_list[final_bin].width,5)
                lines[choose-1].width = round(lines[choose-1].width + bin_list[final_bin].width,5)

        elif score == 6:

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
            lines[choose].start.x=round(lines[choose].start.x + bin_list[final_bin].width,5)
            lines[choose].width = round(lines[choose].width-bin_list[final_bin].width,5)
        elif score == 1:
            if choose+1 < len(lines):
                lines[choose+1].start.x =round(lines[choose+1].start.x-bin_list[final_bin].width,5)
                lines[choose+1].width = round(lines[choose+1].width + bin_list[final_bin].width,5)
            lines[choose].end.x = round(lines[choose].end.x - bin_list[final_bin].width,5)
            lines[choose].width = round(lines[choose].width - bin_list[final_bin].width,5)

    #本站点的货物已经装完
    for s in station_list:
        bins1=s.binList
        if len(bins1)==0:
            s.isEmpty=True

    #如果max_height==vehicle.length则说明车厢已经装满，否则说明以下两种情况：
    # 1.站点的货物已经装载完
    # 2.车辆超重
    #这两种情况都可以通过检查车辆的状态来进一步判断，从而确定是否需要向此站点再派车辆，或者将此车辆继续调度
    vehicle.max_height=max_height
    return max_height
