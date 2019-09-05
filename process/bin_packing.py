# -*- coding:utf-8 -*-
import skyLine
from entity import entity
import sys
def waste_area(vehicle,line,bins):

    bin_waste={}
    bin_map=[]
    res_map=[]

    bin_sort=[]
    res_sort=[]

    for i in range(len(bins)):
        bin_waste[i] = sys.maxsize
        bin_map.append([])
        res_map.append([])
        bin_sort.append([])
        res_sort.append([])

    for i in range(len(bins)):
        cal_next_bin(vehicle, line, bins, bin_map, bin_waste, res_map,bin_sort,res_sort, i)
    return bin_waste,res_map,res_sort


def cal_next_bin(vehicle,line,bins,bin_map,bin_waste,res_map,bin_sort,res_sort,index):
    vehicle_length = vehicle.length
    i=index
    for i in range(len(bins)):
        if i < index:
            continue
        bin=bins[i]
        if bin.width <= line.width and bin.length+line.start.y <= vehicle_length and i not in bin_map[index]:
            bin_map[index].append(i)
            bin_sort[index].append(0)
            tmp_index, min_width = find_next_min_width(bins, vehicle,bin_map[index])

            if bin.width == line.width or tmp_index == -1 or min_width > (line.width - bin.width):
                tmp_area = round((line.width - bin.width) * bin.length, 5)
                if bin_waste[index] > tmp_area:
                    bin_waste[index] = tmp_area
                    res_map[index] = []
                    res_sort[index] = []
                    j=0
                    for j in range(len(bin_map[index])):
                        tmp=bin_map[index][j]
                        res_map[index].append(tmp)
                        res_sort[index].append(bin_sort[index][j])

            else:
                tmp_line=entity.Line(entity.Point(line.start.x + bin.width,line.start.y),entity.Point(line.end.x,line.start.y),bin.length,line.right_height)
                cal_next_bin(vehicle, tmp_line, bins,bin_map,bin_waste, res_map,bin_sort,res_sort,index)
            bin_map[index].remove(bin_map[index][-1])
            bin_sort[index].remove(bin_sort[index][-1])
        if bin.length <= line.width and bin.width+line.start.y <= vehicle_length and i not in bin_map[index]:
            bin_map[index].append(i)
            bin_sort[index].append(1)
            tmp_index,min_width = find_next_min_width(bins, vehicle,bin_map[index])

            if bin.length == line.width or tmp_index == -1 or min_width > (line.width - bin.length):
                tmp_area=round((line.width-bin.length) * bin.width,5)
                if bin_waste[index] > tmp_area:
                    bin_waste[index] = tmp_area
                    res_map[index]=[]
                    res_sort[index] = []

                    for j in range(len(bin_map[index])):
                        tmp=bin_map[index][j]
                        res_map[index].append(tmp)
                        res_sort[index].append(bin_sort[index][j])
            else:
                tmp_line = entity.Line(entity.Point(line.start.x + bin.length, line.start.y),
                                   entity.Point(line.end.x, line.start.y), bin.width, line.right_height)
                cal_next_bin(vehicle, tmp_line, bins,bin_map,bin_waste, res_map,bin_sort,res_sort, index)
            bin_map[index].remove(bin_map[index][-1])
            bin_sort[index].remove(bin_sort[index][-1])


def choose_bin(vehicle,lines,bins):
    vehicle_length = vehicle.length
    vehicle_width = vehicle.width
    bin_map = {}
    bin_socre = {}
    for i in range(len(lines)):
        bin_map[i] = []
        bin_socre[i] = []

    for i in range(len(lines)):
        line = lines[i]
        for i in range(len(bins)):
            b=bins[i]
            if (b.weight + vehicle.used_weight) > vehicle.weight:
                continue
            if b.width <= line.width and b.length + line.height <= vehicle_length:
                bin_map[i].append(b)
            elif b.length <= line.width and b.width + line.height <= vehicle_length:
                b.rotate_bin()
                bin_map[i].append(b)


def find_next_min_width(bins,vehicle,list):
    min_width=sys.maxsize
    res=-1

    for i in range(len(bins)):
        if i in list:
            continue
        if min_width>bins[i].width and (bins[i].weight + vehicle.used_weight) <= vehicle.weight:
            min_width=bins[i].width
            res=i
        if min_width>bins[i].length and (bins[i].weight + vehicle.used_weight) <= vehicle.weight:
            min_width=bins[i].length
            res=i
            #bins[i].rotate_bin()
    if res == -1:
        return res,-1
    return res,min(bins[res].width, bins[res].length)


def my_test():
    bin_list=[]
    vehicle=entity.Vehicle("V001",7.8,2.3,10000,888,0.004)
    line= entity.Line(entity.Point(0,0),entity.Point(2.3,0),7.8,7.8)
    for i in range(20):
        b=entity.Bin(id,1.13,1.45,100,"S095")
        bin_list.append(b)

    bin_waste, res_map, res_sort =waste_area(vehicle, line, bin_list)
    print (bin_waste)
    print (res_map)
    print (res_sort)


def put_bin(vehicle,choose,bin,rotate):
    next_index=choose
    vehicle_length=vehicle.length
    max_height=vehicle.max_height

    lines=vehicle.lines
    if rotate == 1:
        bin.rotate_bin()
    score=skyLine.gene_score(lines[choose],bin)
    # 把bin装入，计算四个点的坐标
    if score != 6 and score != 3 and score != 1 and score != 3.5:

        bin.set_pointList(entity.Point(lines[choose].start.x, lines[choose].start.y),
                                          entity.Point(lines[choose].start.x + bin.width,
                                                       lines[choose].start.y)
                                          , entity.Point(lines[choose].start.x + bin.width,
                                                         lines[choose].start.y + bin.length),
                                          entity.Point(lines[choose].start.x,
                                                       lines[choose].start.y + bin.length))
    else:
        leftDown_1 = entity.Point(lines[choose].end.x - bin.width, lines[choose].height)

        bin.set_pointList(
            entity.Point(lines[choose].end.x - bin.width, lines[choose].height),
            entity.Point(leftDown_1.x + bin.width, leftDown_1.y)
            , entity.Point(leftDown_1.x + bin.width,
                           leftDown_1.y + bin.length),
            entity.Point(leftDown_1.x, leftDown_1.y + bin.length))

    vehicle.bin_list.append(bin)  # add to vehicle
    vehicle.station_bin[bin.local_station].append(bin)
    # 更新vehicle.used_weight
    vehicle.used_weight = round(vehicle.used_weight + bin.weight, 5)
    # 因为bin可能发生旋转，所以根据id在原始的bins中查找，最终删除放入vehicle的bin


    # print(bin_list[final_bin].id, "  ", score)
    if score == 12:
        if lines[choose].left_height == lines[choose].right_height:
            if choose > 0 and choose + 1 < len(lines):
                lines[choose - 1].end = entity.Point(lines[choose + 1].end.x, lines[choose + 1].end.y)
                lines[choose - 1].width = round(lines[choose - 1].width + lines[choose].width + lines[choose + 1].width,
                                                5)
                lines[choose - 1].right_height = lines[choose + 1].right_height

                lines.remove(lines[choose])
                lines.remove(lines[choose])
            else:  # 装满了整个车
                max_height = vehicle_length


        elif choose > 0:
            lines[choose - 1].end = entity.Point(lines[choose].end.x, lines[choose].height + bin.length)
            if choose + 1 < len(lines):
                lines[choose + 1].left_height = round(lines[choose].height - lines[choose + 1].height, 5)

            lines[choose - 1].end.x = lines[choose].end.x
            lines[choose - 1].width = round(lines[choose - 1].width + lines[choose].width, 5)

            lines.remove(lines[choose])

        elif choose == 0:
            lines[choose + 1].left_height = round(vehicle_length - lines[choose + 1].height, 5)
            lines.remove(lines[choose])

    elif score == 11:
        if choose + 1 < len(lines):
            lines[choose + 1].start.x = lines[choose].start.x
            lines[choose + 1].width = round(lines[choose].width + lines[choose + 1].width, 5)
            if choose > 0:
                if lines[choose - 1].height > lines[choose + 1].height:
                    lines[choose + 1].left_height = round(lines[choose - 1].height - lines[choose + 1].height, 5)
                else:
                    lines[choose + 1].left_height = round(vehicle_length - lines[choose + 1].height, 5)
            else:
                lines[choose + 1].left_height = round(vehicle_length - lines[choose + 1].height, 5)

        lines.remove(lines[choose])

    elif score == 10 or score == 9:

        lines[choose].start.y = round(lines[choose].start.y + bin.length, 5)
        lines[choose].end.y = lines[choose].start.y
        lines[choose].height = lines[choose].start.y

        if choose == 0:
            lines[choose].left_height = round(vehicle_length - lines[choose].height, 5)
            if choose + 1 < len(lines):
                if lines[choose].height < lines[choose + 1].height:
                    lines[choose].right_height = round(lines[choose + 1].height - lines[choose].height, 5)
                    lines[choose + 1].left_height = round(vehicle_length - lines[choose + 1].height, 5)
                else:
                    lines[choose].right_height = round(vehicle_length - lines[choose].height, 5)
                    lines[choose + 1].left_height = round(lines[choose].height - lines[choose + 1].height, 5)
            else:
                lines[choose].right_height = round(vehicle_length - lines[choose].height, 5)

        elif choose > 0 and choose + 1 < len(lines):
            if lines[choose].height < lines[choose - 1].height:
                lines[choose].left_height = round(lines[choose - 1].height - lines[choose].height, 5)
                lines[choose - 1].right_height = round(vehicle_length - lines[choose - 1].height, 5)
            else:
                lines[choose].left_height = round(vehicle_length - lines[choose].height, 5)
                lines[choose - 1].right_height = round(lines[choose].height - lines[choose - 1].height, 5)

            if lines[choose].height < lines[choose + 1].height:
                lines[choose].right_height = round(lines[choose + 1].height - lines[choose].height, 5)
                lines[choose + 1].left_height = round(vehicle_length - lines[choose + 1].height, 5)
            else:
                lines[choose].right_height = round(vehicle_length - lines[choose].height, 5)
                lines[choose + 1].left_height = round(lines[choose].height - lines[choose + 1].height, 5)

        elif choose + 1 == len(lines):
            lines[choose].right_height = round(vehicle_length - lines[choose].height, 5)

            if lines[choose].height < lines[choose - 1].height:
                lines[choose].left_height = round(lines[choose - 1].height - lines[choose].height, 5)
                lines[choose - 1].right_height = round(vehicle_length - lines[choose - 1].height, 5)
            else:
                lines[choose].left_height = round(vehicle_length - lines[choose].height, 5)
                lines[choose - 1].right_height = round(lines[choose].height - lines[choose - 1].height, 5)

    elif score == 8 or score == 5.5:

        lines[choose].start.y = round(lines[choose].start.y + bin.length, 5)
        lines[choose].end.y = lines[choose].start.y
        lines[choose].height = lines[choose].start.y
        if choose == 0:
            lines[choose].left_height = round(vehicle_length - lines[choose].height, 5)
        if choose > 0:
            if lines[choose - 1].height < lines[choose].height:
                lines[choose].left_height = round(vehicle_length - lines[choose].height, 5)
                lines[choose - 1].right_height = round(lines[choose].height - lines[choose - 1].height, 5)
            else:
                lines[choose].left_height = round(lines[choose - 1].height - lines[choose].height, 5)
                lines[choose - 1].right_height = round(vehicle_length - lines[choose - 1].height, 5)
        if choose + 1 < len(lines):
            if lines[choose + 1].height > lines[choose].height:
                lines[choose].right_height = round(lines[choose + 1].height - lines[choose].height, 5)
                lines[choose + 1].left_height = round(vehicle_length - lines[choose + 1].height, 5)
            else:
                lines[choose].right_height = round(vehicle_length - lines[choose].height, 5)
                lines[choose + 1].left_height = round(lines[choose].height - lines[choose + 1].height, 5)
        if choose + 1 == len(lines):
            lines[choose].right_height = round(vehicle_length - lines[choose].height, 5)


    elif score == 7 or score == 4.5:

        lines[choose].start.x = round(lines[choose].start.x + bin.width, 5)
        lines[choose].width = round(lines[choose].width - bin.width, 5)
        if choose > 0:
            lines[choose - 1].end.x = round(lines[choose - 1].end.x + bin.width, 5)
            lines[choose - 1].width = round(lines[choose - 1].width + bin.width, 5)

    elif score == 6 or score == 3.5:

        lines[choose].end.x = round(lines[choose].end.x - bin.width, 5)
        lines[choose].width = round(lines[choose].width - bin.width, 5)
        if choose + 1 < len(lines):
            lines[choose + 1].start.x = round(lines[choose + 1].start.x - bin.width, 5)
            lines[choose + 1].width = round(lines[choose + 1].width + bin.width, 5)
    elif score == 5 or score == 4:
        lines[choose].left_height = bin.length

        # 多出一条线段
        tmp_start = entity.Point(lines[choose].start.x, lines[choose].start.y + bin.length)
        tmp_end = entity.Point(tmp_start.x + bin.width, tmp_start.y)

        if tmp_start.y < lines[choose - 1].height:
            tmp_left_height = round(lines[choose - 1].height - tmp_start.y, 5)
        else:
            tmp_left_height = round(vehicle_length - tmp_start.y, 5)
            lines[choose - 1].right_height = round(tmp_start.y - lines[choose - 1].height, 5)
        tmp_right_height = round(vehicle_length - tmp_start.y, 5)

        tmp_line = entity.Line(tmp_start, tmp_end, tmp_left_height, tmp_right_height)
        lines[choose].start.x = round(lines[choose].start.x + bin.width, 5)
        lines[choose].width = round(lines[choose].width - bin.width, 5)
        lines.insert(choose, tmp_line)
        next_index = choose+1

    elif score == 3:
        lines[choose].end.x = round(lines[choose].end.x - bin.width, 5)
        lines[choose].right_height = round(bin.length, 5)
        lines[choose].width = round(lines[choose].width - bin.width, 5)

        tmp_start = entity.Point(lines[choose].end.x, lines[choose].end.y + bin.length)
        tmp_end = entity.Point(tmp_start.x + bin.width, tmp_start.y)

        tmp_left_height = round(vehicle_length - tmp_start.y, 5)
        if choose + 1 == len(lines):
            tmp_right_height = round(vehicle_length - tmp_start.y, 5)
        elif tmp_start.y < lines[choose + 1].height:
            tmp_right_height = round(lines[choose + 1].height - tmp_start.y, 5)
        else:
            tmp_right_height = round(vehicle_length - tmp_start.y, 5)
        tmp_line = entity.Line(tmp_start, tmp_end, tmp_left_height, tmp_right_height)
        lines.insert(choose + 1, tmp_line)

    elif score == 2:
        if choose > 0:
            lines[choose - 1].end.x = round(lines[choose - 1].end.x + bin.width, 5)
            lines[choose - 1].width = round(lines[choose - 1].width + bin.width, 5)
        else:
            tmp_start = entity.Point(0, vehicle_length)
            tmp_end = entity.Point(bin.width, vehicle_length)
            '''
            lines.insert(0,entity.Line(tmp_start,tmp_end,0,0))
        if choose == 0:
            choose = 1
        '''
        lines[choose].start.x = round(lines[choose].start.x + bin.width, 5)
        lines[choose].width = round(lines[choose].width - bin.width, 5)
    elif score == 1:
        if choose + 1 < len(lines):
            lines[choose + 1].start.x = round(lines[choose + 1].start.x - bin.width, 5)
            lines[choose + 1].width = round(lines[choose + 1].width + bin.width, 5)
        else:
            tmp_start = entity.Point(lines[choose].end.x - bin.width, vehicle_length)
            tmp_end = entity.Point(lines[choose].end.x, vehicle_length)
            # lines.append(entity.Line(tmp_start,tmp_end,0,0))
        lines[choose].end.x = round(lines[choose].end.x - bin.width, 5)
        lines[choose].width = round(lines[choose].width - bin.width, 5)

    max_height = max(max_height,bin.length+lines[choose].height)
    vehicle.max_height=max_height
    skyLine.cal_lines(vehicle,lines)

    return next_index


def add_compose_bins(vehicle,index,bin_list,sort_list,bins):
    next_index=index
    for i in range(len(bin_list)):
        bin_index=bin_list[i]
        next_index=put_bin(vehicle,next_index,bins[bin_index],sort_list[i])

    bin_list.sort()
    bin_list.reverse()
    for i in range(len(bin_list)):
        bin_index=bin_list[i]
        bins.remove(bins[bin_index])


my_test()
