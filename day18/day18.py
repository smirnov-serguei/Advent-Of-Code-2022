# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 01:26:52 2022

@author: Serguei Smirnov
"""
import numpy as np
import time

filename = 'input.txt'
with open(filename) as file:
    data = file.read().splitlines()
    
points = []
for line in data:
    points.append(tuple([int(i)+1 for i in line.split(',')]))
points.sort()

xs = [i for i,_,_ in points]
ys = [i for _,i,_ in points]
zs = [i for _,_,i in points]

six_neighbours = [(0,0,1),(0,0,-1),(0,1,0),(0,-1,0),(1,0,0),(-1,0,0)]

count = 0
for (x,y,z) in points:
    for (dx,dy,dz) in six_neighbours:
        if (x+dx, y+dy, z+dz) not in points:
            count += 1

print(f'Part 1: count {count}')

my_array = np.zeros((max(xs)+2, max(ys)+2, max(zs)+2))
for (x,y,z) in points:
    my_array[x,y,z] = 2

start_time = time.time()
to_fill = [(0,0,0)]
while len(to_fill) > 0:
    (x,y,z) = to_fill.pop()
    my_array[x,y,z] = 1
    for (dx,dy,dz) in six_neighbours:
        if (x+dx < my_array.shape[0] and x+dx >= 0 
            and y+dy < my_array.shape[1] and y+dy >= 0
            and z+dz < my_array.shape[2] and z+dz >= 0
            ):
            if (my_array[x+dx, y+dy, z+dz] == 0 
                and (x+dx, y+dy, z+dz) not in to_fill):
                to_fill.append((x+dx, y+dy, z+dz))
print(f'time = {time.time() - start_time} sec')

count = 0
for (x,y,z) in points:
    for (dx,dy,dz) in six_neighbours:
        if my_array[x+dx, y+dy, z+dz] == 1:
            count += 1

print(f'Part 2: count {count}')

