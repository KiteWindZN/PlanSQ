from process import createEntity
import datetime

def createFileJson():
    date=datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    path="../result/"+date+'-result.json'
    return path

def createJson(json_path,vehicle_list):
    with open(json_path,"w+",encoding="utf-8") as f:
        f.write("{\n")

        for j in range(len(vehicle_list)):
            vehicle=vehicle_list[j]

            f.write("\t\""+vehicle.id+"\": {\n")
            f.write("\t\t\"Route\": [")
            for i in range(len(vehicle.path)):
                s=vehicle[i]
                if i==0:
                    f.write("\""+s.id+"\"")
                else:
                    f.write(", \"" + s.id + "\"")

            f.write("],\n")

            for i in range(len(vehicle.path)):
                s=vehicle[i]
                bin_list=vehicle.station_bin[s]
                f.write("\t\t\""+s+"\": {\n")
                for h in range(len(bin_list)):
                    tmp_bin=bin_list[h]
                    f.write("\t\t\t\""+tmp_bin.id+"\": [")
                    point_list=tmp_bin.pointList
                    for g in range(len(point_list)):
                        if (g+1) < len(point_list):
                            f.write("["+point_list[g].x+", "+point_list[g].y+"],")
                        else:
                            f.write("[" + point_list[g].x + ", " + point_list[g].y + "]")
                    if (h+1)<len(bin_list):
                        f.write("],\n")
                    else:
                        f.write("]\n")

                if (i+1) ==len(vehicle.path):
                    f.write("\t\t}\n")
                else:
                    f.write("\t\t},\n")

            if j+1 == len(vehicle_list):
                f.write("\t}\n")
            else:
                f.write("\t},\n")

        f.write("}")


if __name__== '__main__':
    path=createFileJson()
    vehicle_list = createEntity.createVehicle("../dataset/month3/vehicle.json")
    createJson(path,vehicle_list)