# Xinyu Sun 952469
# Shiyu Dong 870480
# Jie Luo 1122592
# Yuxiang Xia 969367
# Yixuan Tang 959698

import json
import csv

file = open("result_geo_aus.json")
file1 = open("result_geo_aus_2.json")
file2 = open("result_geo_aus_3.json")
file3 = open("result_geo_aus_4.json")
coordinates = open("coordinates.csv", "w")
writer = csv.writer(coordinates)
writer.writerow(["longitude","latitude"])

data = file.readline()
while(data):
        tweets = json.loads(data)
        if tweets["coordinates"]:
            print(tweets["coordinates"]["coordinates"])
            writer.writerow(tweets["coordinates"]["coordinates"])
        file.readline()
        data = file.readline()

data1 = file1.readline()
while(data1):
        tweets = json.loads(data1)
        if tweets["coordinates"]:
            print(tweets["coordinates"]["coordinates"])
            writer.writerow(tweets["coordinates"]["coordinates"])
        file1.readline()
        data1 = file1.readline()

data2 = file2.readline()
while(data2):
        tweets = json.loads(data2)
        if tweets["coordinates"]:
            print(tweets["coordinates"]["coordinates"])
            writer.writerow(tweets["coordinates"]["coordinates"])
        file2.readline()
        data2 = file2.readline()

data3 = file3.readline()
while(data3):
        tweets = json.loads(data3)
        if tweets["coordinates"]:
            print(tweets["coordinates"]["coordinates"])
            writer.writerow(tweets["coordinates"]["coordinates"])
        file3.readline()
        data3 = file3.readline()





