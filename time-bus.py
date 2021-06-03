import xlrd
import urllib.request
from urllib.parse import quote
import json
import pandas as pd
import time
import os


def rgrid(read_file_dir):
    myWordbookr = xlrd.open_workbook(read_file_dir)
    mySheetsr = myWordbookr.sheets()
    mySheetr = mySheetsr[no_sheet]
    # 获取列数
    nrows = mySheetr.nrows
    grid = []
    for i in range(1, nrows):
        lon = mySheetr.cell_value(i, 1)
        lat = mySheetr.cell_value(i, 2)
        grid.append([round(lon, 6), round(lat, 6)])
    return grid


read_file_dir = "sfq-grid.xls"  # 输入测算范围栅格坐标文件，作为起点
no_sheet = 0
grid = rgrid(read_file_dir)
key = ''  # 输入你的key
des = [120.802392,31.061964]  # 终点坐标，单一，通过高德地图坐标拾取器查询
uri = 'https://restapi.amap.com/v3/direction/transit/integrated?origin='
city = '0512'  # 支持市内公交换乘/跨城公交的起点城市，规则：城市名称/citycode
data_csv = {}
times, lons, lats, distances = [], [], [], []
for i in range(len(grid)):
    url = uri + str(grid[i][0]) + ',' + str(grid[i][1]) + '&destination=' + str(des[0]) + ',' + str(
        des[1]) + '&city=' + str(city) + '&cityd=' + str(city)+ '&key=' + key
    print(url)
    temp = urllib.request.urlopen(url)
    temp = json.loads(temp.read())
    data = temp["route"]
    lons.append(data["origin"].split(",")[0])
    lats.append(data["origin"].split(",")[1])
    try:
        distances.append(data["transits"][0]["distance"])
        times.append(data["transits"][0]["duration"])
        print("已完成：", i, "/", len(grid))
    except:
        print(1)
        distances.append(no_sheet)
        times.append(no_sheet)
data_csv['lon'], data_csv['lat'], data_csv['distance'], data_csv['time'] = lons, lats, distances, times
df = pd.DataFrame(data_csv)
file_name = 'time_bus' + str(des[0]) + '_' + str(des[1]) + ".csv"
file_path = "c:" + os.sep + "test" + os.sep + file_name
df.to_csv(file_path, index=False, encoding='utf_8_sig')
print('写入成功')
