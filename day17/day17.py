# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 15:43:59 2022

@author: Serguei Smirnov
"""
import time
import cProfile

shape_0 = [[0,0], [1,0], [2,0], [3,0]]
shape_1 = [[1,0], [0,1], [1,1], [2,1], [1,2]]
shape_2 = [[0,0], [1,0], [2,0], [2,1], [2,2]]
shape_3 = [[0,0], [0,1], [0,2], [0,3]]
shape_4 = [[0,0], [0,1], [1,0], [1,1]]
shapes = (shape_0, shape_1, shape_2, shape_3, shape_4)

def draw_map(my_map):
    map_str = ''
    for y in range(my_map['y_max'], my_map['y_min']-1, -1):
        for x in range(my_map['x_min'], my_map['x_max']+1): 
            map_str += my_map[(x,y)]
        map_str += '\n'
    print(map_str) #, flush=True

def make_map(width=7, height=4):
    my_map = {
        'x_min': 0,
        'x_max': width + 1,
        'y_min': 0,
        'y_max': height,
        'top' : 0,
        }
    # walls
    for y in range(0, height+2):
        my_map[(0, y)] = '#'
        my_map[(width+1, y)] = '#'
    for x in range(1, width+1):
        # floor
        my_map[(x, 0)] = '#'
        # air fill
        for y in range(1, height+2):
            my_map[(x, y)] = '.'
    return my_map

def add_height(my_map, height):
    if height > 0:
        for dy in range(height):
            y = my_map['y_max'] + dy + 1
            my_map[(0, y)] = '#'
            my_map[(my_map['x_max'], y)] = '#'
            for x in range(1, my_map['x_max']):
                my_map[(x,y)] = '.'
        my_map['y_max'] += height

def move_block(block, dx=0, dy=0):
    for point in block:
        point[0] += dx
        point[1] += dy

direction_list = {
    'v': (0, -1),
    '<': (-1, 0),
    '>': (1, 0),
    }
def check_move(my_map, my_block, direction):
    # if direction == 'v':
    #     dx = 0
    #     dy = -1
    # elif direction == '<':
    #     dx = -1
    #     dy = 0
    # elif direction == '>':
    #     dx = 1
    #     dy = 0
    dx, dy = direction_list[direction]
    can_move = True
    for (x,y) in my_block:
        if my_map[(x+dx, y+dy)] != '.':
            can_move = False
            break
    return can_move

def get_surface(my_map):
    surface = []
    for x in range(1, my_map['x_max']):
        y = my_map['y_max']
        while my_map[(x,y)] == '.':
            y -= 1
        surface.append(my_map['top'] - y)
    return surface

def compute(n_rocks, check_states):
    with open('input.txt') as file:
        data = file.read()
    
    my_map = make_map()
    # draw_map(my_map)
    states = {}
    
    direction_idx = 0
    for i in range(n_rocks):
        # create new block
        new_block = [s.copy() for s in shapes[i % len(shapes)]]
        
        # add space on top of map
        height = max([i for _,i in new_block]) +4 -my_map['y_max'] +my_map['top']
        add_height(my_map, height)
        # draw_map(my_map)
        
        # Set block in starting position
        move_block(new_block, dx=3, dy=my_map['top'] + 4)
        
        # loop while falling
        while True:
            # move by jet
            direction = data[direction_idx % len(data)]
            direction_idx += 1
            if check_move(my_map, new_block, direction):
                move_block(new_block, dx=(1 if direction=='>' else -1))
                
            # fall one tick
            if check_move(my_map, new_block, 'v'):
                move_block(new_block, dy=-1)
            else:
                break
        
        # add block to map
        for (x,y) in new_block:
            my_map[(x,y)] = '#'
        # update maps top height
        my_map['top'] = max(*[i for _,i in new_block], my_map['top'])
        
        # add state, can't be from first loop
        if check_states and i > len(data):
            shape_i = i % len(shapes)
            dir_i = direction_idx % len(data)
            surface = get_surface(my_map)
            state = (shape_i, dir_i, *surface)
            # print(state)
            if state in states: 
                # print('')
                # print(f"Current cycle {i}, state {state}, top {my_map['top']}")
                # print(f"Previous state (i, top): {states[state]}")
                break
            states[state] = (i, my_map['top'])
            
    if check_states:
        return my_map, states[state][0], states[state][1], i, my_map['top']
    else:
        return my_map

my_map, i1, top1, i2, top2 = compute(100000, True)
n_loops, rem_loops = divmod(1000000000000 - i2, i2 - i1)

# cProfile.run('my_map = compute(100)')

my_map = compute(i2 + rem_loops, False)
total_height = my_map['top'] + (top2 - top1) * n_loops
print(f'total_height {total_height}')

# draw_map(my_map)
# print(f"Part 1: tower height = {my_map['top']}")
