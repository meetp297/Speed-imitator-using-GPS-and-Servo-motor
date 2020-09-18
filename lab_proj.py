import csv
import numpy as np
from math import radians, cos, sin, asin, sqrt

def load_elements(s):
    lat = []
    lon = []
    time = []
    with open(s) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for rows in csv_reader:
            time.append(rows[0])
            lat.append(rows[1])
            lon.append(rows[2])

    lat =  np.array(lat[1:],dtype=float)
    lon = np.array(lon[1:],dtype=float)
    time = time[1:]
    # print(time)
    h = [time[i][11:13] for i in range(len(time))]

    h = np.array(h,dtype=float)
    # print(h)
    m = [time[i][14:16] for i in range(len(time))]
    m = np.array(m,dtype=float)
    # print(m)
    s = [time[i][17:23] for i in range(len(time))]
    s = np.array(s,dtype=float)
    # print(s)
    return lat,lon,h,m,s

lat,lon,h,m,s = load_elements("gps_data.csv")
distance = []
time = []
for i in range(lat.shape[0]-1):
    lon1 = radians(lon[i]) 
    lon2 = radians(lon[i+1]) 
    lat1 = radians(lat[i]) 
    lat2 = radians(lat[i+1]) 
       
    # Haversine formula  
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  
    c = 2 * asin(sqrt(a))  
     
    # Radius of earth in meters. Use 3956 for miles 
    r = 6371000
    distance.append(r*c) 


for i in range(h.shape[0]-1):
    time.append((s[i+1] - s[i]) + (m[i+1] - m[i])*60 + (h[i+1] - h[i])*3600)

print(time)
time = np.array(time)
distance = np.array(distance)
speed = distance/time

speed[np.isnan(speed)] = 0
#removing all the negative speed and negative time
speed=speed[speed>=0]
time=time[time>=0]

#scale speed by 100 for fine tuning in arduino
speed=speed*100 
print(speed)