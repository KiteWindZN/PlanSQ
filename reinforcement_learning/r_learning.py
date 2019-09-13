# -*- coding:utf-8 -*-
from process import skyLine
from entity import entity
from process import bin_packing
from process import geneticAlgm
#寻找最适合放入选中line的bin的组合
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

        bin_map[i].append(geneticAlgm.create_new_bin(available_bins[i]))
        bin_sort[i].append(0)
        sum_score=0
        next_line_index,tmp_score = get_next_line(vehicle,available_bins[i],choose,0)#正着放


        while tmp_score!=-1:
            sum_score += tmp_score
            if tmp_score >= 8 or tmp_score == 5.5:
                break
            #根据打分规则选出下一个分数最高的bin
            bin_list,final_bin,score=choose_next_bin(vehicle,bins,next_line_index,bin_map[i])
            if final_bin != -1:
                next_line_index, tmp_score = get_next_line(vehicle, bin_list[final_bin], next_line_index, 0)  # 正着放:
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

        tmp_value_0 = round(sum_score/len(bin_map[i])-5*tmp_waste_0,5)
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

        while tmp_score!=-1:
            sum_score += tmp_score
            if tmp_score >= 8 or tmp_score == 5.5:
                break
            # 根据打分规则选出下一个分数最高的bin
            bin_list,final_bin,score=choose_next_bin(vehicle,bins,next_line_index,bin_map[i])
            if final_bin!=-1:
                next_line_index, tmp_score = get_next_line(vehicle, bin_list[final_bin], next_line_index, 0)  # 正着放:
                lines=vehicle.lines
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
        tmp_value_1 = round(sum_score/len(bin_map[i])-5*tmp_waste_1,5)

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
    # 本站点的货物已经装完
    return  next_index,score

#寻找下一个分数最高的bin
def choose_next_bin(vehicle,bins,choose,choosed_bins):
    lines = vehicle.lines
    vehicle_length = vehicle.length
    bin_list = skyLine.get_available_bin_list(vehicle, bins, choose)
    if len(bin_list) == 0:
        return bin_list,-1, -1
    score = 0
    final_bin = -1
    for i in range(len(bin_list)):
        if is_in_bin_list(bin_list[i], choosed_bins) == True:
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

def cal_value(vehicle,bins,index):
    print ("avg score subtract waste area")


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
        max_height=bin_packing.add_compose_bins(vehicle,choose,bin_list,bin_sort,bins)
    if len(station.binList)==0:
        station.isEmpty=True
    vehicle.max_height=max_height
    return max_height

