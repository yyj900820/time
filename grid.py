import numpy as np
import math
import pandas as pd
import time
import os

def generate_grids(max_long,max_lat,min_long,min_lat,resolution):
	grids_lib = []
	dlat = resolution * 360 / (2 * math.pi * 6371004)
	#dlon = resolution * 360 / (2 * math.pi * 6371004 * math.cos((min_lat + max_lat) / 2))
	dlon = resolution * 360 / (2 * math.pi * 6371004) * 1.17647
	longs = np.arange(min_long - dlon/2, max_long, dlon)
	lats = np.arange(min_lat - dlat/2,max_lat,dlat)
	for i in range(len(longs) - 1):
		for j in range(len(lats) - 1):
			grids_lib.append([round(float(longs[i]), 6), round(float(lats[j]), 6)])
		# yield [round(float(longs[i]),6),round(float(lats[j]),6),round(float(longs[i+1]),6),round(float(lats[j+1]),6)]
	return grids_lib

max_long = 121.975185
min_long = 119.920013
max_lat = 32.711134
min_lat = 30.262322
resolution = 1000

grid=generate_grids(max_long,max_lat,min_long,min_lat,resolution)
print('划分后的网格数：', len(grid))
data_csv = {}
lons, lats = [], []
for i in range(len(grid)):
	lons.append(grid[i][0])
	lats.append(grid[i][1])
data_csv['lon'], data_csv['lat'] = lons,lats
df = pd.DataFrame(data_csv)
file_name = 'sfq_sg' + ".csv"
file_path = "c:" + os.sep + "test" + os.sep + "code" + os.sep + "time" + os.sep + file_name
df.to_csv(file_path, index=False, encoding='utf_8_sig')
print('写入成功')