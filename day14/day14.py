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
    UP = "\x1B[3A"
    for y in range(my_map['y_min'], my_map['y_max']+1):
        for x in range(my_map['x_min'], my_map['x_max']+1): 
            print(my_map[(x,y)][-1], end='')
        print('')

filename = 'input.txt'
with open(filename) as file:
    data = file.read().splitlines()
    
# Construct the map
x_min, x_max = None, None
y_min, y_max = 0, None
for line in data:
    for coord in line.split(' -> '):
        (x,y) = str_coord(coord)
        if not x_min:
            x_min, x_max, y_max = x, x, y
        else:
            x_min = min(x_min, x)
            x_max = max(x_max, x)
            y_max = max(y_max, y)
x_min -= 1
x_max += 1
y_max += 1

mymap = {}
mymap['x_min'] = x_min
mymap['y_min'] = y_min
mymap['x_max'] = x_max
mymap['y_max'] = y_max
for x in range(x_min, x_max+1): 
    for y in range(y_min, y_max):
        mymap[(x,y)] = 'air.'
    mymap[(x,y+1)] = 'void_'

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
    while True:
        if mymap[(x,y+1)].startswith('v'):
            finished = True
            break
        elif mymap[(x,y+1)].startswith('a'):
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

print(f'Part: sands = {sands}')
draw_map(mymap)