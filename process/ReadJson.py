#"bin_id": "B00001",
#           "bin_length": 1.65,
#            "bin_width": 0.85,
#           "bin_weight": 132,
#           "station": "S039"
import json
def resolveBinJson(path):
    file=open(path,"r")
    fileJson=json.load(file)
    #print(fileJson)
    bins=fileJson["Bin"]

    bin_id = []
    bin_length = []
    bin_width = []
    bin_weight = []
    station = []
    for bin in bins:
        #print(bin['bin_id'])

        bin_id.append(bin["bin_id"])
        bin_length.append(bin["bin_length"])
        bin_width.append(bin["bin_width"])
        bin_weight.append(bin["bin_weight"])
        station.append(bin["station"])

    return bin_id,bin_length,bin_width,bin_weight,station

# "Station": [
#        {
#            "station_id": "S001",
#            "vehicle_limit": 8,
#            "loading_time": 24
#        },
#
def resolveStationJson(path):
    file=open(path,"r")
    fileJson=json.load(file)
    stations=fileJson["Station"]
    station_id=[]
    vehicle_limit=[]
    loading_time=[]

    for station in stations:
        station_id.append(station["station_id"])
        vehicle_limit.append(station["vehicle_limit"])
        loading_time.append(station["loading_time"])
    return station_id,vehicle_limit,loading_time

#"Vehicle": [{"vehicle_id": "V001", "vehicle_length": 7.8, "vehicle_width": 2.3, "vehicle_weight": 10000, "flag_down_fare": 888, "distance_fare": 0.004},

def resolveVehicleJson(path):
    file=open(path,"r")
    fileJson=json.load(file)
    vehicles=fileJson["Vehicle"]
    vehicle_id=[]
    vehicle_length=[]
    vehicle_width=[]
    vehicle_weight=[]
    flag_down_fare=[]
    distance_fare=[]

    for vehicle in vehicles:
        vehicle_id.append(vehicle["vehicle_id"])
        vehicle_length.append(vehicle["vehicle_length"])
        vehicle_width.append(vehicle["vehicle_width"])
        vehicle_weight.append(vehicle["vehicle_weight"])
        flag_down_fare.append(vehicle["flag_down_fare"])
        distance_fare.append(vehicle["distance_fare"])
    return vehicle_id,vehicle_length,vehicle_width,vehicle_weight,flag_down_fare,distance_fare

#"Matrix": [{"departure_station_id": "S001", "arrival_station_id": "S001", "distance": 1, "time": 1.0},
#

def resolveMatrixJson(path):
    file=open(path,"r")
    fileJson=json.load(file)
    matrixes=fileJson["Matrix"]
    departure_station_id=[]
    arrival_station_id=[]
    distance=[]
    time=[]

    for matrix in matrixes:
        departure_station_id.append(matrix["departure_station_id"])
        arrival_station_id.append(matrix["arrival_station_id"])
        distance.append(matrix["distance"])
        time.append(matrix["time"])
    return departure_station_id,arrival_station_id,distance,time


if __name__=='__main__':

    bin_id,bin_length,bin_width,bin_weight,station=resolveBinJson("../dataset/bin.json")
    vehicle_id,vehicle_length,vehicle_width,vehicle_weight,flag_down_fare,distance_fare=resolveVehicleJson("../dataset/vehicle.json")
    station_id,vehicle_limit,loading_time=resolveStationJson("../dataset/station.json")
    departure_station_id,arrival_station_id,distance,time=resolveMatrixJson("../dataset/matrix.json")
    print(departure_station_id)