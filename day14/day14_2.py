# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 22:43:11 2022

@author: Serguei
"""
import numpy as np

def str_coord(text):
    x = int(text.split(',')[0])
    y = int(text.split(',')[1])
    return (x,y)

def draw_map(my_map):
    map_str = ''
    for y in range(my_map['y_min'], my_map['y_max']+1):
        for x in range(my_map['x_min'], my_map['x_max']+1): 
            map_str += my_map[(x,y)][-1]
        map_str += '\n'
    print(map_str, end='', flush=True)

filename = 'test.txt'
with open(filename) as file:
    data = file.read().splitlines()
    
# Construct the map
y_max = None
for line in data:
    for coord in line.split(' -> '):
        (x,y) = str_coord(coord)
        if not y_max:
            y_max = y
        else:
            y_max = max(y_max, y)
y_min = 0
y_max += 2
x_min = 500 - y_max
x_max = 500 + y_max

mymap = {}
mymap['x_min'] = x_min
mymap['y_min'] = y_min
mymap['x_max'] = x_max
mymap['y_max'] = y_max
for x in range(x_min, x_max+1): 
    for y in range(y_min, y_max):
        mymap[(x,y)] = 'air.'
    mymap[(x,y+1)] = 'stone#'

for line in data:
    coords = line.split(' -> ')
    for idx, c in enumerate(coords):
        if idx == len(coords) - 1:
            break
        c_curr = str_coord(c)
        c_next = str_coord(coords[idx+1])
        x_step = 1 if c_curr[0] <= c_next[0] else -1
        y_step = 1 if c_curr[1] <= c_next[1] else -1
        for x in np.arange(c_curr[0], c_next[0]+x_step, step=x_step): 
            for y in np.arange(c_curr[1], c_next[1]+y_step, step=y_step):
                mymap[(x,y)] = 'stone#'
# draw_map(mymap)

# sand 
finished = False
sands = 0
while not finished:
    (x, y) = (500,0)
    if mymap[(x,y)].startswith('sa'):
        break
    while True:
        if mymap[(x,y+1)].startswith('a'):
            y += 1
        elif mymap[(x-1,y+1)].startswith('a'):
            x -= 1
            y += 1
        elif mymap[(x+1,y+1)].startswith('a'):
            x += 1
            y += 1
        else:
            mymap[(x,y)] = 'sand_o'
            sands += 1
            break
draw_map(mymap)

print(f'Part: sands = {sands}')