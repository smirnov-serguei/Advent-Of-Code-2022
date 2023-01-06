# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 22:43:16 2022

@author: Serguei
"""
import numpy as np
import time

test = not True
filename = 'input.txt'
if test:
    filename = 'test.txt'

def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def draw_map(my_map):
    map_str = ''
    for y in range(my_map['y_min'], my_map['y_max']+1):
        for x in range(my_map['x_min'], my_map['x_max']+1): 
            map_str += my_map[(x,y)]
        map_str += '\n'
    print(map_str, end='', flush=True)

with open(filename) as file:
    data = file.read().splitlines()
    
#%% Initialize map params
mymap = {}
sensors = {}
x_min, y_min = np.inf, np.inf
x_max, y_max = -np.inf, -np.inf
dist_max = 0
for line in data:
    temp = line.split()
    (x_sens, y_sens) = int(temp[2][2:-1]), int(temp[3][2:-1])
    x_min = min(x_min, x_sens)
    x_max = max(x_max, x_sens)
    y_min = min(y_min, y_sens)
    y_max = max(y_max, y_sens)
    (x_beac, y_beac) = int(temp[-2][2:-1]), int(temp[-1][2:])
    x_min = min(x_min, x_beac)
    x_max = max(x_max, x_beac)
    y_min = min(y_min, y_beac)
    y_max = max(y_max, y_beac)
    dist_max = max(dist_max, dist((x_sens, y_sens), (x_beac, y_beac)))
    sensors[(x_sens, y_sens)] = (x_beac, y_beac)
x_min -= dist_max
x_max += dist_max
y_min -= dist_max
y_max += dist_max
mymap['x_min'] = x_min
mymap['y_min'] = y_min
mymap['x_max'] = x_max
mymap['y_max'] = y_max

#%% Construct the map
if test:
    for x in range(x_min, x_max+1):
        for y in range(y_min, y_max+1):
            mymap[(x,y)] = '.'
        print(f'\rx = {x-x_min}/{x_max-x_min}', end='')
    print('')
    for sens in sensors.keys():
        beac = sensors[sens]
        mymap[sens] = 'S'
        mymap[beac] = 'B'
        for x in range(x_min, x_max+1):
            for y in range(y_min, y_max+1):
                if dist((x,y), sens) <= dist(beac, sens) and mymap[(x,y)] == '.':
                    mymap[(x, y)] = '+'
    
    draw_map(mymap)

#%% Count results
y = 2000000
if test:
    y = 10
count = 0
for x in range(x_min, x_max+1):
    in_range = False
    for sens in sensors.keys():
        beac = sensors[sens]
        if beac == (x,y):
            in_range = False
            break
        if dist((x,y), sens) <= dist(beac, sens):
            in_range = True
            break
    if in_range:
        count += 1
    print(f'\rx = {x-x_min}/{x_max-x_min}', end='')
print('')

print(f'Part 1: count = {count}')

#%% Part 2
max_search = 4000000
if test:
    max_search = 20

x = 0 
y = 0
while y <= max_search:
    while x <= max_search:
        detected = False
        for sens in sensors.keys():
            beac = sensors[sens]
            if dist((x,y), sens) <= dist(beac, sens):
                x = sens[0] + dist(beac, sens) - abs(y - sens[1]) + 1
                detected = True
                break
        if not detected:
            break
    if not detected:
        break
    y += 1
    x = 0
    
    
    print(f'\ry = {y}/{max_search}', end='')
print('')

print(f'Part 2: x {x}, y {y}, freq {x * 4000000 + y}')
