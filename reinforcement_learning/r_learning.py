# -*- coding:utf-8 -*-
'''
此文件为强化学习的实现部分，通过skyline的打分规则，来选取可以放入线段L1的Bin，
通过探索环境的方式来找出放入L1的最优的Bin的组合
'''

from process import skyLine
from entity import entity
from process import bin_packing
from process import geneticAlgm
from process import createEntity
import sys

#通过对环境的探索,寻找最适合放入选中line的bin的组合
def find_next_bin_list(vehicle,bins,choose):
    #print ("find the next bin with reinforcement learning method")
    lines=vehicle.lines
    line=lines[choose]
    vehicle_length = vehicle.length
    res_map=[]
    res_value=[]
    res_sort=[]
    bin_map=[]
    bin_sort=[]

    available_bins=[]
    for b in bins:
        if b.weight + vehicle.used_weight > vehicle.weight:
            continue
        if b.width <= line.width and b.length+line.height <= vehicle_length and b.length + line.height <= vehicle.length :
            available_bins.append(b)
        elif b.length <= line.width and b.width + line.height <= vehicle_length and b.width + line.height <= vehicle.length:
            available_bins.append(b)

    if len(available_bins) == 0:
        line.is_able=False
        return [], [], -1

    for i in range(len(available_bins)):
        bin_map.append([])
        bin_sort.append([])
        res_map.append([])
        res_sort.append([])
        res_value.append(-100)
        if is_first_shape(available_bins,i) == False:

            continue
        #深拷贝lines
        copy_lines=deep_copy_lines(lines)

        used_weight=vehicle.used_weight
        used_weight += available_bins[i].weight
        bin_map[i].append(geneticAlgm.create_new_bin(available_bins[i]))
        bin_sort[i].append(0)
        sum_score=0
        next_line_index,tmp_score = get_next_line(vehicle,available_bins[i],choose,0)#正着放

        while tmp_score!=-1:
            sum_score += tmp_score
            if tmp_score >= 8 or tmp_score == 5.5:
                break
            #根据打分规则选出下一个分数最高的bin
            bin_list,final_bin,score=choose_next_bin(vehicle,bins,next_line_index,bin_map[i],used_weight)
            if final_bin != -1:
                next_line_index, tmp_score = get_next_line(vehicle, bin_list[final_bin], next_line_index, 0)  # 正着放:
                used_weight +=bin_list[final_bin].weight
                lines=vehicle.lines
            else:
                tmp_score=-1
            if tmp_score!=-1:
                #sum_score += tmp_score
                bin_map[i].append(geneticAlgm.create_new_bin(bin_list[final_bin]))
                bin_sort[i].append(0)

        if tmp_score >= 8 or tmp_score == 5.5:
            tmp_waste_0=0
        else:
            tmp_waste_0 = lines[next_line_index].width * bin_map[i][-1].length
            #tmp_waste_0 = lines[next_line_index].width
        tmp_area=0
        large_num=0
        for b in bin_map[i]:
            tmp_area += round(b.length * b.width,5)
            if b.length > 0.9 and b.width > 0.9:
                large_num += 1
        if bins[i].local_station == u"S011" or bins[i].local_station == u"S154":
            tmp_value_0 = round(0.5*sum_score/len(bin_map[i])-3*tmp_waste_0 - 0.8*len(bin_map[i])+ 0.9*tmp_area+3.2*large_num,5)
        else:
            tmp_value_0 = round(0.5 * sum_score / len(bin_map[i]) - 3 * tmp_waste_0 - 0.8 * len(
            bin_map[i]) + tmp_area + 3 * large_num, 5)
        #tmp_value_0 = round(sum_score / len(bin_map[i]) - 5 * tmp_waste_0 , 5)
        #赋值res_value,res_sort,res_map
        for j in range(len(bin_map[i])):
            res_map[i].append(bin_map[i][j])
            res_sort[i].append(bin_sort[i][j])
            res_value[i]=tmp_value_0

        lines=deep_copy_lines(copy_lines)
        vehicle.lines=lines
        bin_map[i]=[]
        bin_sort[i]=[]
        sum_score = 0

        bin_map[i].append(geneticAlgm.create_new_bin(available_bins[i]))
        bin_sort[i].append(1)
        sum_score = 0
        next_line_index,tmp_score = get_next_line(vehicle,available_bins[i],choose,1)#倒着放
        used_weight=vehicle.used_weight
        used_weight += available_bins[i].weight

        while tmp_score!=-1:
            sum_score += tmp_score
            if tmp_score >= 8 or tmp_score == 5.5:
                break
            # 根据打分规则选出下一个分数最高的bin
            bin_list,final_bin,score=choose_next_bin(vehicle,bins,next_line_index,bin_map[i],used_weight)
            if final_bin!=-1:
                next_line_index, tmp_score = get_next_line(vehicle, bin_list[final_bin], next_line_index, 0)  # 正着放:
                lines=vehicle.lines
                used_weight += bin_list[final_bin].weight
            else:
                tmp_score=-1
            if tmp_score!=-1:
                #sum_score += tmp_score
                bin_map[i].append(geneticAlgm.create_new_bin(bin_list[final_bin]))
                bin_sort[i].append(0)
                if tmp_score >=8  or tmp_score==5.5 :
                    sum_score +=tmp_score
                    break
        #if next_line_index==1:
        #    print ("ffff")
        if tmp_score >= 8 or tmp_score == 5.5:
            tmp_waste_1=0
        else:
            tmp_waste_1 = lines[next_line_index].width * bin_map[i][-1].length
            #tmp_waste_1 = lines[next_line_index].width
        tmp_area = 0
        large_num=0
        for b in bin_map[i]:
            tmp_area += round(b.length * b.width, 5)
            if b.length >0.9 and b.width>0.9:
                large_num += 1
        if bins[i].local_station == u"S011" or bins[i].local_station == u"S154":
            tmp_value_1 = round(0.5*sum_score/len(bin_map[i])-3*tmp_waste_1 - 0.8*len(bin_map[i])+0.9*tmp_area + 3.2*large_num,5)
        else:
            tmp_value_1 = round(0.5 * sum_score / len(bin_map[i]) - 3 * tmp_waste_1 - 0.8 * len(
                bin_map[i]) + tmp_area + 3 * large_num, 5)
        #tmp_value_1 = round(sum_score / len(bin_map[i]) - 5 * tmp_waste_1, 5)

        if tmp_value_1 > tmp_value_0:
            res_map[i]=[]
            res_sort[i]=[]
            for j in range(len(bin_map[i])):
                res_map[i].append(bin_map[i][j])
                res_sort[i].append(bin_sort[i][j])
                res_value[i] = tmp_value_1

        lines = deep_copy_lines(copy_lines)
        vehicle.lines=lines

    res_index=0
    tmp_value=res_value[0]
    for i in range(len(res_value)):
        if tmp_value < res_value[i]:
            tmp_value = res_value[i]
            res_index = i
    vehicle.lines=deep_copy_lines(copy_lines)
    # 也可以直接return res_map[res_index][0], res_sort[res_index][0]
    modify_bin_list(vehicle.lines[choose],res_map[res_index],res_sort[res_index])
    return res_map[res_index],res_sort[res_index],res_value[res_index]

#此种形状的块是否是第一次出现
def is_first_shape(bin_list,index):
    for i in range(index):
        if bin_list[i].length == bin_list[index].length and bin_list[i].width == bin_list[index].width:
            return False
        if bin_list[i].width == bin_list[index].length and bin_list[i].length == bin_list[index].width:
            return False
    return True

#尝试将一个bin放入某个line后，得到的车辆的状态
def get_next_line(vehicle,bin,choose,rotate):
    lines=vehicle.lines
    line=lines[choose]
    vehicle_length=vehicle.length
    bin_length=bin.length
    bin_width=bin.width

    if rotate == 0:
        if bin.length + line.height > vehicle_length or bin.width > line.width:
            tmp_score1 = -1
        else:
            tmp_score1 = skyLine.gene_score(line, bin)
        if tmp_score1 == -1:
            return choose,-1
        score = tmp_score1
    if rotate == 1:
        if bin.width + line.height > vehicle_length or bin.length > line.width:
            tmp_score2 = -1
        else:
            tmp_bin=entity.Bin(id,bin.width,bin.length,bin.weight,bin.local_station)
            tmp_score2 = skyLine.gene_score(line, tmp_bin)
            bin_length=bin.width
            bin_width=bin.length
        if tmp_score2 == -1:
            return choose,-1
        score = tmp_score2

    if score == 0:

        leftDown = entity.Point(lines[choose].start.x, lines[choose].height)

        left_start_x = round(lines[choose].end.x, 5)
        left_start_y = lines[choose].height
        tmp_r_height = lines[choose].right_height


        #vehicle.used_weight = vehicle.used_weight + bin.weight
        # 因为bin可能发生旋转，所以根据id在原始的bins中查找，最终删除放入vehicle的bin


        lines[choose].start = entity.Point(leftDown.x, leftDown.y + bin_length)
        lines[choose].end = entity.Point(leftDown.x + bin_width,
                                         leftDown.y + bin_length)
        lines[choose].height = round(lines[choose].start.y, 5)
        lines[choose].width = round(bin_width, 5)

        tmp_start = entity.Point(lines[choose].end.x, left_start_y)
        tmp_end = entity.Point(left_start_x, left_start_y)

        tmp_left_height = round(bin_length, 5)
        tmp_right_height = tmp_r_height

        tmp_line = entity.Line(tmp_start, tmp_end, tmp_left_height, tmp_right_height)
        if choose + 1 < len(lines):
            lines.insert(choose + 1, tmp_line)
        else:
            lines.append(tmp_line)
        skyLine.cal_lines(vehicle, lines)
        # line.is_able = False
        return choose+1,0

    next_index=choose
    #vehicle.used_weight = round(vehicle.used_weight + bin.weight, 5)

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
                lines[choose].height = vehicle_length
                lines[choose].left_right = 0
                lines[choose].right_right = 0
                lines[choose].start.x = 0
                lines[choose].end.x = vehicle.width
                lines[choose].start.y = vehicle_length
                lines[choose].end.y = vehicle_length

                #break

        elif choose > 0:
            lines[choose - 1].end = entity.Point(line.end.x, line.height + bin_length)
            if choose + 1 < len(lines):
                lines[choose + 1].left_height = round(lines[choose].height - lines[choose + 1].height, 5)

            # lines[choose-1].height = round(lines[choose-1].width + lines[choose].width,5)
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

        lines[choose].start.y = round(lines[choose].start.y + bin_length, 5)
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

        lines[choose].start.y = round(lines[choose].start.y + bin_length, 5)
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

        lines[choose].start.x = round(lines[choose].start.x + bin_width, 5)
        lines[choose].width = round(lines[choose].width - bin_width, 5)
        if choose > 0:
            lines[choose - 1].end.x = round(lines[choose - 1].end.x + bin_width, 5)
            lines[choose - 1].width = round(lines[choose - 1].width + bin_width, 5)

    elif score == 6 or score == 3.5:

        lines[choose].end.x = round(lines[choose].end.x - bin_width, 5)
        lines[choose].width = round(lines[choose].width - bin_width, 5)
        if choose + 1 < len(lines):
            lines[choose + 1].start.x = round(lines[choose + 1].start.x - bin_width, 5)
            lines[choose + 1].width = round(lines[choose + 1].width + bin_width, 5)
    elif score == 5 or score == 4:
        lines[choose].left_height = bin_length

        # 多出一条线段
        tmp_start = entity.Point(lines[choose].start.x, lines[choose].start.y + bin_length)
        tmp_end = entity.Point(tmp_start.x + bin_width, tmp_start.y)

        if tmp_start.y < lines[choose - 1].height:
            tmp_left_height = round(lines[choose - 1].height - tmp_start.y, 5)
        else:
            tmp_left_height = round(vehicle_length - tmp_start.y, 5)
            lines[choose - 1].right_height = round(tmp_start.y - lines[choose - 1].height, 5)
        tmp_right_height = round(vehicle_length - tmp_start.y, 5)

        tmp_line = entity.Line(tmp_start, tmp_end, tmp_left_height, tmp_right_height)
        lines[choose].start.x = round(lines[choose].start.x + bin_width, 5)
        lines[choose].width = round(lines[choose].width - bin_width, 5)
        lines.insert(choose, tmp_line)

        next_index=choose+1

    elif score == 3:
        lines[choose].end.x = round(lines[choose].end.x - bin_width, 5)
        lines[choose].right_height = round(bin_length, 5)
        lines[choose].width = round(lines[choose].width - bin_width, 5)

        tmp_start = entity.Point(lines[choose].end.x, lines[choose].end.y + bin_length)
        tmp_end = entity.Point(tmp_start.x + bin_width, tmp_start.y)

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
            lines[choose - 1].end.x = round(lines[choose - 1].end.x + bin_width, 5)
            lines[choose - 1].width = round(lines[choose - 1].width + bin_width, 5)
        else:
            tmp_start = entity.Point(0, vehicle_length)
            tmp_end = entity.Point(bin_width, vehicle_length)
            '''
            lines.insert(0,entity.Line(tmp_start,tmp_end,0,0))
        if choose == 0:
            choose = 1
        '''
        lines[choose].start.x = round(lines[choose].start.x + bin_width, 5)
        lines[choose].width = round(lines[choose].width - bin_width, 5)
    elif score == 1:
        if choose + 1 < len(lines):
            lines[choose + 1].start.x = round(lines[choose + 1].start.x - bin_width, 5)
            lines[choose + 1].width = round(lines[choose + 1].width + bin_width, 5)
        else:
            tmp_start = entity.Point(lines[choose].end.x - bin_width, vehicle_length)
            tmp_end = entity.Point(lines[choose].end.x, vehicle_length)
            # lines.append(entity.Line(tmp_start,tmp_end,0,0))
        lines[choose].end.x = round(lines[choose].end.x - bin_width, 5)
        lines[choose].width = round(lines[choose].width - bin_width, 5)

    skyLine.cal_lines(vehicle, lines)

    return  next_index,score

#寻找下一个分数最高的bin
def choose_next_bin(vehicle,bins,choose,choosed_bins,used_weight):
    lines = vehicle.lines
    vehicle_length = vehicle.length
    bin_list = skyLine.get_available_bin_list(vehicle, bins, choose)
    if len(bin_list) == 0:
        return bin_list,-1, -1
    score = -2
    final_bin = -1
    for i in range(len(bin_list)):
        if is_in_bin_list(bin_list[i], choosed_bins) == True or used_weight+bin_list[i].weight > vehicle.weight:
            continue
        if bin_list[i].length + lines[choose].height > vehicle_length or bin_list[i].width > lines[choose].width:
            tmp_score1 = -1
        else:
            tmp_score1 = skyLine.gene_score(lines[choose], bin_list[i])
        if bin_list[i].width + lines[choose].height > vehicle_length or bin_list[i].length > lines[choose].width:
            tmp_score2 = -1
        else:
            bin_list[i].rotate_bin()
            tmp_score2 = skyLine.gene_score(lines[choose], bin_list[i])

        if tmp_score1 > tmp_score2 and tmp_score2 != -1:  # 再旋转回来
            bin_list[i].rotate_bin()
        tmp_score = max(tmp_score1, tmp_score2)
        if score < tmp_score:
            score = tmp_score
            final_bin = i
    return bin_list, final_bin, score

#判断一个bin是否在某一个binList中
def is_in_bin_list(bin,bin_list):
    for b in bin_list:
        if b.id == bin.id:
            return True
    return False


#深拷贝vehicle的lines，保存每一次搜索前的车辆的状态
def deep_copy_lines(lines):
    tmp_lines=[]
    for line in lines:
        tmp_lines.append(entity.Line(entity.Point(line.start.x,line.start.y),
                                     entity.Point(line.end.x,line.end.y),
                                     line.left_height,line.right_height))

    return tmp_lines

#以skyLine和机器学习为基础的的组合装箱算法的调用入口
def bin_packing_function(vehicle,station):

    vehicle.path.append(station.id)
    bins = station.binList
    for b in bins:
        if b.local_station not in vehicle.station_bin:
            vehicle.station_bin[b.local_station] = []

    vehicle_length = vehicle.length
    vehicle_width = vehicle.width
    # lines中的线段按照严格的从左到右的顺序排列
    lines = vehicle.lines
    for l in lines:
        l.is_able=True

    max_height = vehicle.max_height
    if len(lines)==0:
        lines.append(entity.Line(entity.Point(0,0),entity.Point(vehicle.width,0),vehicle.length,vehicle.length))

    while max_height <= vehicle_length and vehicle.used_weight <= vehicle.weight and len(bins) > 0:
        choose = skyLine.get_choose_line(vehicle, bins)

        if choose == -1:
            break
        bin_list,bin_sort,bin_value=find_next_bin_list(vehicle, bins, choose)
        lines=vehicle.lines
        if len(bin_list)==0:
            lines[choose].is_able=False
            continue

        tmp_list=[]
        tmp_sort=[]
        tmp_list.append(bin_list[0])
        tmp_sort.append(bin_sort[0])
        bin_list=tmp_list
        bin_sort=tmp_sort


        max_height=bin_packing.add_compose_bins(vehicle,choose,bin_list,bin_sort,bins)
    if len(station.binList)==0:
        station.isEmpty=True
    vehicle.max_height=max_height
    return max_height

#合并vehicle经过的站点
def merge_stations(vehicle,stations):

    merge_station = entity.Station(stations[vehicle.path[0]].id, stations[vehicle.path[0]].vehicle_limit, 0)
    for b in vehicle.bin_list:
        #b.pointList = []
        merge_station.binList.append(geneticAlgm.create_new_bin(b))

    return merge_station

#合并两个站点
def merge_two_station(station1,station2):
    merge_station = entity.Station(station1.id, min(station1.vehicle_limit,station2.vehicle_limit), 0)
    for b in station1.binList:
        merge_station.binList.append(geneticAlgm.create_new_bin(b))
    for b in station2.binList:
        merge_station.binList.append(geneticAlgm.create_new_bin(b))
    return merge_station

#根据vehicle里面装入的bin，来将对应站点的bin删除
def delete_packedbins(vehicle,stations):
    bin_list=vehicle.bin_list
    for b in bin_list:
        local_station=b.local_station
        skyLine.delete_bin(stations[local_station].binList,b)

    for p in vehicle.path:
        createEntity.cal_station_area_weight(stations[p])


#因为map为非对称结构图，所以根据vehicle的现有的路径，求出最优路径
def cal_path(vehicle,map):
    path=vehicle.path
    n=len(path)
    if n == 2:
        if path[1] in map[path[0]] and path[0] in map[path[1]]:
            if map[path[1]][path[0]] < map[path[0]][path[1]]:
                tmp_p = path[0]
                path[0] = path[1]
                path[1] = tmp_p
        return
    list=get_full_sort(n)
    tmp_dis=sys.maxsize
    res=-1
    for j in range(len(list)):
        L=list[j]
        sum_dis=0
        start=L[0]
        for i in range(len(L)):
            if i==0:
                continue
            cur=L[i]
            if path[cur] in map[path[start]]:
                sum_dis+=map[path[start]][path[cur]]
            else:
                sum_dis=sys.maxsize
                break
            start=cur
        if tmp_dis > sum_dis:
            tmp_dis=sum_dis
            res=j

    tmp_path=[]

    for i in range(n):
        tmp_path.append(path[list[res][i]])

    vehicle.path=tmp_path

#根据实际装货的情况，得到vehicle的path
def cal_vehicle_list_path(vehicle_list, map):
    for v in vehicle_list:
        if len(v.path) == 1:
            continue
        cal_path(v, map)

#得到全排列
def get_full_sort(n):
    list=[]
    sub_list=[]
    cal_full_sort(list,sub_list,n)
    return list

#得到list的全排列
def cal_full_sort(list,sub_list,n):
    if len(sub_list) == n:
        tmp_list=[]
        for num in sub_list:
            tmp_list.append(num)
        list.append(tmp_list)
        return
    for i in range(n):
        if i not in sub_list:
            sub_list.append(i)
            cal_full_sort(list,sub_list,n)
            sub_list.remove(sub_list[-1])

#调整bin_list的放置方向，以减少浪费空间
def modify_bin_list(line,bin_list,bin_sort):
    width=line.width
    for i in range(len(bin_list)):
        b=bin_list[i]
        if bin_sort[i]==0:
            w=b.width
        else:
            w=b.length
        width -= w
    for i in range(len(bin_list)):
        b=bin_list[i]
        if bin_sort[i]==0:
            l=b.length
            w=b.width
        else:
            l=b.width
            w=b.length
        if l>w and l-w<=width:
            bin_sort[i]=1-bin_sort[i]
            width = width-(l-w)

#为站点打上标记
def label_station(station):
    bin_list = station.binList
    small = 0
    large = 0
    for b in bin_list:
        if b.width > 0.9 and b.length > 0.9 and (b.length != 1.45 and b.width != 1.45):
            large += 1
        elif b.length != 1.45 and b.width != 1.45:
            small += 1
    station.small=small
    station.large=large
    #if large * 0.7 < small and small - 0.5*large > 30:
    if large * 0.6 < small and small > 40:
        station.label = 1
    #elif large * 0.3 > small and large - 2 * small > 30:
    elif large * 0.4 > small and large > 40:
        station.label = -1
    else:
        station.label = 0

#通过label将stations分类
def get_station_id_by_label(stations,list_id):
    list1=[]
    list2=[]
    list3=[]

    for s in list_id:
        if stations[s].label==-1:
            list1.append(s)
        elif stations[s].label==0:
            list2.append(s)
        else:
            list3.append(s)
    return list1,list2,list3


#标记station是否含有很多的小的bin
def label_stations(stations):
    for s in stations:
        label_station(stations[s])

#计算小货的个数
def cal_small_bin(station):
    bin_list=station.binList
    small=0
    for b in bin_list:
        if b.width<= 0.9 or b.length <= 0.9:
            small += 1
    return small

#计算大货的个数
def cal_large_bin(station):
    bin_list=station.binList
    large=0
    for b in bin_list:
        if b.width > 0.9 and b.length > 0.9:
            large += 1
    return large

#合并站点，然后进行装箱
def merge_packing(vehicle,stations):
    geneticAlgm.check_vehicle(vehicle)
    merge_station=merge_stations(vehicle,stations)
    choose_vehicle = geneticAlgm.create_new_vehicle(vehicle)
    tmp_line = entity.Line(entity.Point(0, 0), entity.Point(choose_vehicle.width, 0), choose_vehicle.length,
                           choose_vehicle.length)
    choose_vehicle.lines.append(tmp_line)

    choose_vehicle.max_height = 0

    bin_packing_function(choose_vehicle, merge_station)

    if len(merge_station.binList)>0:
        return vehicle.max_height,vehicle
    
    last_station=stations[vehicle.path[-1]]
    max_height = bin_packing_function(choose_vehicle,last_station)
    choose_vehicle.path = vehicle.path
    vehicle = choose_vehicle

    return max_height,vehicle


#根据vehicle里面装入的bin，来将对应站点的bin删除
def delete_packedbins(vehicle,stations):
    get_real_path(vehicle)
    bin_list=vehicle.bin_list
    for b in bin_list:
        local_station=b.local_station
        skyLine.delete_bin(stations[local_station].binList,b)

    for p in vehicle.path:
        createEntity.cal_station_area_weight(stations[p])

#获得vehicle的真实的路径信息
def get_real_path(vehicle):
    station_bin = vehicle.station_bin
    path=[]
    for s in station_bin:
        if len(station_bin[s]) > 0:
            path.append(s)
    vehicle.path=path


def choose_partner_station(vehicle,s_id,stations,map,T):
    station=stations[s_id]
    nabor_list=map[s_id]
    cur_label = station.label
    tmp_dis = sys.maxsize
    next_id = "-1"
    for s in nabor_list:
        tmp_station=stations[s]
        tmp_label=tmp_station.label
        if tmp_label == 1:
            if tmp_dis > map[s_id][s] and stations[s].vehicle_limit >= vehicle.length and vehicle.usedTime+T[s_id][s]+stations[s].loading_time<=600:
                tmp_dis = map[s_id][s]
                next_id = s

    if tmp_dis > 50000:
        #choose the nearest station
        next_id, tmp_dis = next_station(vehicle, s_id, stations, map, T)
    return next_id,tmp_dis


def next_station(vehicle,s_id,stations,map,time):
    nobor_list = map[s_id]
    tmp_dis = sys.maxsize
    next_s_id = "-1"
    next_list = []
    next_dis = []
    for n_s in nobor_list:
        if map[s_id][n_s] < tmp_dis and n_s != s_id and stations[n_s].isEmpty == False and stations[n_s].vehicle_limit >= vehicle.length\
                and vehicle.usedTime+time[s_id][n_s] + stations[n_s].loading_time <= 600 and n_s not in vehicle.path:
            tmp_dis = map[s_id][n_s]
            next_s_id = n_s
            next_list.append(n_s)
            next_dis.append(tmp_dis)
    return next_s_id, tmp_dis

#合并两个站点
def merge_two_stations(station1,station2):
    merge_station = entity.Station(station1.id, min(station1.vehicle_limit,station2.vehicle_limit), 0)
    for b in station1.binList:
        #b.pointList = []
        merge_station.binList.append(geneticAlgm.create_new_bin(b))
    for b in station2.binList:
        #b.pointList = []
        merge_station.binList.append(geneticAlgm.create_new_bin(b))
    return merge_station

# 合并两个距离最近的站点
def merge_nearest_stations(stations,map):
    for s in stations:
        stations[s].is_merged=0

    res_station_list=[]
    for s_1 in map:
        tmp_dis= sys.maxsize
        choose_s="-1"
        if stations[s_1].is_merged == 1 or stations[s_1].isEmpty==True:
            continue
        for s_2 in map[s_1]:
            if s_1 == s_2:
                continue
            if tmp_dis > map[s_1][s_2] and map[s_1][s_2] <= 1000 and stations[s_1].vehicle_limit == stations[s_2].vehicle_limit and stations[s_2].is_merged == 0 and stations[s_2].isEmpty==False:
                tmp_dis = map[s_1][s_2]
                choose_s = s_2
        if choose_s == "-1":
            continue
        if s_1==u"S114" or choose_s==u"S114":
            print "nearest,S114"
        merge_station = merge_two_station(stations[s_1],stations[choose_s])
        stations[s_1].is_merged=1
        stations[choose_s].is_merged=1
        if len(merge_station.binList) == 0:
            stations[s_1].isEmpty=True
            stations[choose_s].isEmpty==True
            continue
        res_station_list.append(merge_station)
    return res_station_list

#检查路径中的某个站点是否已经为空
def is_one_empty(path,stations):

    for p in path:
        if stations[p].isEmpty==True:
            return True
    return False

#打印函数
def print_nearest_stations(map):
    my_set=set()
    for s_1 in map:
        for s_2 in map[s_1]:
            if s_1 == s_2:
                continue
            if map[s_1][s_2] <= 1000:
                print s_1,s_2,map[s_1][s_2]
                my_set.add(s_1)
                my_set.add(s_2)
    print len(my_set)

#根据vehicle_limit得到标签为-1的站点的列表
def get_large_station_id_list(stations,vehicle_limit):
    large_bin_station = []
    for s in stations:
        if stations[s].label == -1 and stations[s].vehicle_limit == vehicle_limit:
            #print s, len(stations[s].binList)
            large_bin_station.append(s)
    return large_bin_station

#根据vehicle_limit得到标签为1的站点的列表
def get_small_station_id_list(stations,vehicle_limit):
    small_bin_station = []
    for s in stations:
        if stations[s].label == 1 and stations[s].vehicle_limit == vehicle_limit:
            #print s, len(stations[s].binList)
            small_bin_station.append(s)
    return small_bin_station


#根据vehicle已经装入的货物列表，在合并的虚拟站点中删除货物
def delete_from_merged_station(merge_list,station,vehicle):
    for s in merge_list:
        if len(s.binList)==0:
            continue
        path=[]
        path.append(s.binList[0].local_station)
        path.append(s.binList[-1].local_station)
        if station.id in path:
            for b in vehicle.bin_list:
                if b.local_station == station.id:
                    skyLine.delete_bin(s.binList,b)



if __name__ == '__main__':
    path = "../dataset/month4/"
    map, time = createEntity.createMap(path + "matrix.json")
    #print_nearest_stations(map)
    stations, maxLimit = createEntity.createStation(path + "station.json")

    bins = createEntity.createBin(path + "bin.json", stations)
    label_stations(stations)
    #station_list=merge_nearest_stations(stations,map)
    #print len(station_list)
    #merge_diff_size_stations(stations,map)
    large_bin_station=[]
    small_bin_station=[]

    for s in stations:
        if stations[s].label==1 and stations[s].vehicle_limit==18:
            print s,len(stations[s].binList)

    #process_merge_by_label_stations(stations,map,18)

    #print get_full_sort(2)