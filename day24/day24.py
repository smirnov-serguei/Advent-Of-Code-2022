# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 02:04:25 2022

@author: Serguei Smirnov
"""

import numpy as np
import networkx as nx

symb_to_int = {
    '.': 0,
    '<': 1,
    '^': 2,
    '>': 3,
    'v': 4,
    '#': -1,
    }
symb_to_step = {
    '<': (0, -1),
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    }
neighbours = ((-1,0), (0,-1), (0,0), (0,1), (1,0))

def init_map(data):
    # Initialize map and blizzards
    my_map = np.zeros((len(data), len(data[0])), dtype=int)
    blizzards = {}
    blizzards_count = 0
    
    for idx, _ in np.ndenumerate(my_map):
        symb = data[idx[0]][idx[1]]
        my_map[idx] = symb_to_int[symb]
        # add blizzard to list
        if my_map[idx] > 0:
            blizzards_count += 1
            blizzards[blizzards_count] = {'idx':idx, 'symb':symb}

    return (np.expand_dims(my_map, axis=0), blizzards)

def new_map_level(my_map):
    # add new level
    new_map = np.concatenate((my_map, [my_map[0].copy()]), axis=0) 
    # delete all copied blizzards
    new_map[-1][new_map[-1] > 0] = 0
    return new_map

def step_blizzards(my_map, blizzards):
    for bliz in blizzards:
        # get direction and coord of moving blizzard
        step = np.array(symb_to_step[blizzards[bliz]['symb']])
        new_coord = np.array(blizzards[bliz]['idx']) + step
        # correct for walls
        if new_coord[0] == 0: new_coord[0] = n_lines - 2 # top
        elif new_coord[0] == n_lines - 1: new_coord[0] = 1 # bottom
        elif new_coord[1] == 0: new_coord[1] = n_cols - 2 # left
        elif new_coord[1] == n_cols - 1: new_coord[1] = 1 # right
        # update list of blizzards and new map 
        blizzards[bliz]['idx'] = tuple(new_coord)
        my_map[-1][tuple(new_coord)] = symb_to_int[blizzards[bliz]['symb']]

def update_graph(my_map, G, r):
    for idx, value in np.ndenumerate(my_map[r]):
        # if current point has been reached already and it's a valid space
        if (r, *idx) in G and value == 0:
            # check all reachable neighbours
            for n_coords in neighbours:
                new_line = n_coords[0] + idx[0]
                new_col = n_coords[1] + idx[1]
                # make sure coords are within map boundaries
                if (new_line >= 0 and new_col >= 0 
                    and new_line < my_map.shape[1] 
                    and new_col <= my_map.shape[2]):
                    # neightbour is a valid waking space
                    if my_map[(r+1, new_line, new_col)] == 0:
                        G.add_edge((r, *idx), (r+1, new_line, new_col))
    

with open('input.txt') as file:
    data = file.read().splitlines()
    
(my_map, blizzards) = init_map(data)
n_lines = my_map.shape[1]
n_cols = my_map.shape[2]
end_point = (n_lines-1, n_cols-2)

G = nx.DiGraph()
G.add_node((0,0,1)) # starting point
r = 0
while r < 1000:
    print(f'\rminutes: {r+1}', end='')
    my_map = new_map_level(my_map)
    # Calc next locations of blizzards
    step_blizzards(my_map, blizzards)
    # Create graph nodes & edges
    update_graph(my_map, G, r)
    
    if (r+1, *end_point) in G:
        break
    r += 1
print(f'\nOne way minutes: {r+1}')

# Back to start
G = nx.DiGraph()
G.add_node((r+1, *end_point)) # starting point
end_point = (0,1)

while r < 1000:
    print(f'\rminutes: {r+1}', end='')
    my_map = new_map_level(my_map)
    # Calc next locations of blizzards
    step_blizzards(my_map, blizzards)
    # Create graph nodes & edges
    update_graph(my_map, G, r)
    
    if (r+1, *end_point) in G:
        break
    r += 1
print(f'\nBack to start minutes: {r+1}')

# Back to end
G = nx.DiGraph()
G.add_node((r+1, 0, 1)) # starting point
end_point = (n_lines-1, n_cols-2)

while r < 1000:
    print(f'\rminutes: {r+1}', end='')
    my_map = new_map_level(my_map)
    # Calc next locations of blizzards
    step_blizzards(my_map, blizzards)
    # Create graph nodes & edges
    update_graph(my_map, G, r)
    
    if (r+1, *end_point) in G:
        break
    r += 1
print(f'\nBack to end minutes: {r+1}')

# print(my_map)
# nx.draw_networkx(G)
