# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 23:33:32 2022

@author: Serguei Smirnov
"""

import numpy as np

def draw_map(my_map, current_pos={'yx':(0,0), 'facing':'>'}):
    map_str = ''
    for y in range(my_map.shape[0]):
        for x in range(my_map.shape[1]): 
            if current_pos['yx'] == (y, x):
                map_str += current_pos['facing']
            else:
                map_str += str(my_map[y,x])
        map_str += '\n'
    print(map_str)

def create_map(data):
    # path to follow
    path = ['']
    for c in data[-1]:
        if c.isdigit(): path[-1] = path[-1] + c
        else: path.append(c)
    # create map
    x_max = max([len(line) for line in data[:-1]]) + 2
    y_max = len(data)
    my_map = np.ones((y_max, x_max), dtype=int) * 2
    
    for idx_line, line in enumerate(data):
        for idx_col, char in enumerate(line):
            if char == '.': my_map[idx_line+1, idx_col+1] = 0
            elif char == '#': my_map[idx_line+1, idx_col+1] = 1
    return path, my_map

def rotate(init_facing, rotate_dir):
    dirs = ['<', '^', '>', 'v']
    init_idx = dirs.index(init_facing)
    final_idx = (init_idx + (1 if rotate_dir=='R' else -1)) % len(dirs)
    return dirs[final_idx]

def get_coords_part1(my_map, current_pos):
    (y, x) = current_pos['yx']
    new_x, new_y = x, y
    # if horizontal loop
    if dx == 1:
        new_x = (my_map[y] < 2).argmax()
    elif dx == -1:
        new_x = len(my_map[y]) -1 -(my_map[y] < 2)[::-1].argmax()
    # if vertical loop
    if dy == 1:
        new_y = (my_map[:,x] < 2).argmax()
    elif dy == -1:
        new_y = len(my_map[:,x]) -1 -(my_map[:,x] < 2)[::-1].argmax()
    
    new_facing = current_pos['facing'] # unchanged
    return (new_x, new_y, new_facing)

def get_coords_part2(my_map, current_pos):
    (y, x) = current_pos['yx']
    facing = current_pos['facing']
    new_x, new_y = x, y
    new_facing = facing
    
    if (y==1 and x>=51 and x<=100 and facing=='^'):# 1
        new_x = 1
        new_y = x + 100
        new_facing = '>'
    elif (y==1 and x>=101 and x<=150 and facing=='^'):# 2
        new_x = x - 100
        new_y = 200
        new_facing = '^'
    elif (x==150 and y>=1 and y<=50 and facing=='>'):# 3
        new_x = 100
        new_y = 151 - y
        new_facing = '<'
    elif (y==50 and x>=101 and x<=150 and facing=='v'):# 4
        new_x = 100
        new_y = x - 50
        new_facing = '<'
    elif (x==101 and y>=51 and y<=100 and facing=='>'):# 5
        new_x = y + 50
        new_y = 50
        new_facing = '^'
    elif (x==100 and y>=101 and y<=150 and facing=='>'):# 6
        new_x = 150
        new_y = 151 - y
        new_facing = '<'
    elif (y==150 and x>=51 and x<=100 and facing=='v'):# 7
        new_x = 50
        new_y = x + 100
        new_facing = '<'
    elif (x==50 and y>=151 and y<=200 and facing=='>'):# 8
        new_x = y -100
        new_y = 150
        new_facing = '^'
    elif (y==200 and x>=1 and x<=50 and facing=='v'):# 9
        new_x = x + 100
        new_y = 1
        new_facing = 'v'
    elif (x==1 and y>=151 and y<=200 and facing=='<'):# 10
        new_x = y - 100
        new_y = 1
        new_facing = 'v'
    elif (x==1 and y>=101 and y<=150 and facing=='<'):# 11
        new_x = 51
        new_y = 151 - y
        new_facing = '>'
    elif (y==101 and x>=1 and x<=50 and facing=='^'):# 12
        new_x = 51
        new_y = x + 50
        new_facing = '>'
    elif (x==51 and y>=51 and y<=100 and facing=='<'):# 13
        new_x = y - 50
        new_y = 101
        new_facing = 'v'
    elif (x==51 and y>=1 and y<=50 and facing=='<'):# 14
        new_x = 1
        new_y = 151 - y
        new_facing = '>'
    # else:
    #     print(current_pos)

    # print(current_pos, new_y, new_x, new_facing, file=open('log.txt', 'a'))
    return (new_x, new_y, new_facing)

step_size = { # dy, dx
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1),
    '^': (-1, 0),
    }

filename = 'input.txt'
with open(filename) as file:
    data = file.read().splitlines()

path, my_map = create_map(data)
current_pos = {'yx': (1, my_map[1].argmin()), # line, col
         'facing': '>'}
# draw_map(my_map, current_pos)

for next_move in path:
    # print(next_move, file=open('log.txt', 'a'))
    # rotate if needed
    if next_move[0].isalpha():
        facing = rotate(current_pos['facing'], next_move[0])
        steps = int(next_move[1:])
    else:
        facing = current_pos['facing']
        steps = int(next_move)
    current_pos['facing'] = facing
    
    # perform number of steps
    # print(next_move, facing)
    for s in range(steps):
        # update facing in case piece of the map changed
        (dy, dx) = step_size[current_pos['facing']]
        (y, x) = current_pos['yx']
        # print(y, x, dy, dx)
        # if stone do nothing
        if my_map[y+dy, x+dx] == 1:
            break
        # if end of map check other side for stone, or move
        elif my_map[y+dy, x+dx] == 2:
            # (new_x, new_y, new_facing) = get_coords_part1(my_map, current_pos)
            (new_x, new_y, new_facing) = get_coords_part2(my_map, current_pos)
            if my_map[new_y, new_x] == 1: # stone
                break
            else:
                current_pos['yx'] = (new_y, new_x)
                current_pos['facing'] = new_facing
        else:
            current_pos['yx'] = (y+dy, x+dx)
        # print(current_pos, file=open('log.txt', 'a'))

    # draw_map(my_map, current_pos)

facing_idx = ['>', 'v', '<', '^'].index(current_pos['facing'])
password = 1000*current_pos['yx'][0] + 4*current_pos['yx'][1] + facing_idx
print(f"Part 1: password {password}")