#! /usr/bin/python3

from typing import List
import sys

global_car_capacity = 4
# 乘客输入示例：
# [ 起点， 终点， 人数]
gloabl_trips = [ [22, 35, 4],\
                 [ 5,  4, 1],\
                 [18, 30, 2],\
                 [ 3, 20, 1],\
                 [ 9, 21, 2] \
               ]

def carPooling(trips: List[List[int]], capacity: int):
    # 给所有乘客打标签
    for i in range(len(trips)):
        trips[i].append('P{0}'.format(i + 1))
    # 附加是接还是送
    for trip in trips:
        trip.append('src')
    trips.sort(key=lambda x:x[0])
    # 接第一个乘客
    while trips:
        for i in range(len(trips)):
            trip = trips[i]
            if trip[4] == 'src':
                if trip[0] > trip[1]:
                    print('{0}不接,本车不回头'.format(trip[3]))
                    del trips[i]
                    break
                if trip[0] == trip[1]:
                    print('{0}不接,原地坐车的不接'.format(trip[3]))
                    del trips[i]
                    break
                if trip[2] > capacity:
                    print('{0}不接,本车没位置了'.format(trip[3]))
                    del trips[i]
                    break
                else:
                    print('{0}已上车'.format(trip[3]))
                    capacity = capacity - trip[2]
                    trip[4] = 'dst'
                    trip[0] = trip[1]
                    trip[1] = -1
                    trips.sort(key=lambda x:x[0])
                    break
            else:
                print('{0}已下车'.format(trip[3]))
                capacity = capacity + trip[2]
                del trips[i]
                break
        else:
            break

def print_passenger(trips):
    print('idx    Src          Dst       Number of passenger')
    for i in range(len(trips)):
        trip = trips[i]
        print('P%d     %3d          %3d                        %2d'%(i+1,trip[0],trip[1],trip[2]))


if __name__ == "__main__":
    print_passenger(gloabl_trips)
    carPooling(trips=gloabl_trips, capacity=global_car_capacity)

