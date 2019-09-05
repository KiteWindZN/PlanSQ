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

my_test()
