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
# 将读取的栅格中心点转为起点坐标对，坐标对见用“| ”分隔；经度和纬度用","分隔
ori = []
ori1 = ''

type = 1  # 0：直线距离 1：驾车导航距离（仅支持国内坐标） 3：步行规划距离（仅支持5km之间的距离）
for i in range(len(grid)):
    if ori1 == '':
        ori1 = str(grid[i][0]) + ',' + str(grid[i][1])
    else:
        ori1 = ori1 + '|' + str(grid[i][0]) + ',' + str(grid[i][1])
    if (i % 90 == 0) and (i > 0):
        ori.append(ori1)
        ori1 = ''
uri = 'https://restapi.amap.com/v3/distance?origins='
data_csv = {}
times, lons, lats, distances = [], [], [], []
for i in range(len(ori)):
    url = uri + ori[i] + '&destination=' + str(des[0]) + ',' + str(des[1]) + '&type=' + str(type) + '&key=' + key
    temp = urllib.request.urlopen(url)
    temp = json.loads(temp.read())
    data = temp["results"]
    for j in range(len(data)):
        lons.append(ori[i].split("|")[j].split(",")[0])
        lats.append(ori[i].split("|")[j].split(",")[1])
        distances.append(data[j]["distance"])
        times.append(data[j]["duration"])
    print("已完成：", i, "/", len(ori))
data_csv['lon'], data_csv['lat'], data_csv['distance'], data_csv['time'] = lons, lats, distances, times
df = pd.DataFrame(data_csv)
file_name = 'time_' + str(des[0]) + '_' + str(des[1]) + ".csv"
file_path = "c:" + os.sep + "test" + os.sep + file_name
df.to_csv(file_path, index=False, encoding='utf_8_sig')
print('写入成功')
