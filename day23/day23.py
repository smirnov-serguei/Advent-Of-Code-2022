# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 20:07:53 2022

@author: Serguei Smirnov
"""
import numpy as np

DEBUG = not True

n_rounds = 100 # just to make map big enough
filename = 'input.txt'
with open(filename) as file:
    data = file.read().splitlines()

neighbours = {
    'all': [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]],
    'N': [[-1, -1], [-1, 0], [-1, 1]],
    'S': [[1, -1], [1, 0], [1, 1]],
    'W': [[-1, -1], [0, -1], [1, -1]],
    'E': [[-1, 1], [0, 1], [1, 1]],
    }

move_order = ['N', 'S', 'W', 'E']

# compress my_map to minimum rectangle
def compress_map(my_map):
    min_idx_line = my_map.argmax(axis=0)
    min_idx_line = min(min_idx_line[min_idx_line != 0])
    max_idx_line = np.flipud(my_map).argmax(axis=0)
    max_idx_line = my_map.shape[1] - min(max_idx_line[max_idx_line != 0])
    
    min_idx_col = my_map.argmax(axis=1)
    min_idx_col = min(min_idx_col[min_idx_col != 0])
    max_idx_col = np.fliplr(my_map).argmax(axis=1)
    max_idx_col = my_map.shape[0] - min(max_idx_col[max_idx_col != 0])
    return my_map[min_idx_line:max_idx_line, min_idx_col:max_idx_col]

n_cols = len(data[0]) + 2 * n_rounds
n_rows = len(data) + 2 * n_rounds
my_map = np.zeros((n_rows, n_cols), dtype=int)

elves = {}

for idx_l, line in enumerate(data):
    for idx_c, c in enumerate(line):
        if c=='#':
            my_map[idx_l+n_rounds, idx_c+n_rounds] = 1
            elves[(idx_l+n_rounds, idx_c+n_rounds)] = None

# print(my_map)
rounds = 0
# finished = False
while True: #not finished:
# for r in range(n_rounds):
    rounds += 1
    print('Round ', rounds)
    if DEBUG: print(my_map)
    # First half of round
    for e_l, e_c in elves:
        if DEBUG: print(f'Elf {e_l}, {e_c}')
        
        # Check all surrounding spots for elves
        no_neighbours = True
        for n_l, n_c in neighbours['all']:
            if my_map[e_l + n_l, e_c + n_c] == 1:
                no_neighbours = False
                break
        if no_neighbours: # do nothing for current elf
            if DEBUG: print('No eighbours, do nothing')
            continue
        
        # Check the four directions in order
        for direction in move_order:
            no_neighbours = True
            if DEBUG: print(f'Check {direction}')
            for n_l, n_c in neighbours[direction]:
                if DEBUG: print(n_l, n_c)
                if my_map[e_l + n_l, e_c + n_c] == 1:
                    no_neighbours = False
                    if DEBUG: print('Neighbour found', n_l, n_c)
                    break
            if no_neighbours: # found direction to move
                if DEBUG: print(f'No neighbours {direction}')
                break
        if not no_neighbours: 
            # neighbours everywhere do nothing
            move_l, move_c = 0, 0
            # break
        else:
            # set moving coord for current elf
            move_l, move_c = neighbours[direction][1]
        elves[(e_l, e_c)] = e_l + move_l, e_c + move_c
        if DEBUG: print(f'Moving to {elves[(e_l, e_c)]}')
    if DEBUG: print(elves)
    
    # Second half of round
    elves_c = elves.copy()
    elves = {}
    some_moved = False
    for e in elves_c:
        if DEBUG: print('Elf', e)
        # check if only current elf wants to move to the new location
        if list(elves_c.values()).count(elves_c[e]) == 1:
            if DEBUG: print('count 1')
            new_e = elves_c[e]
            elves[new_e] = None
            # Write new positions to mmap
            my_map[e] = 0
            my_map[new_e] = 1
            some_moved = True
        else:
            if DEBUG: print('count > 1')
            elves[e] = None
        if DEBUG: print(elves)
    if DEBUG: print(elves)
    
    if not some_moved:
        break
        
    # Rotate the order of directions to look at first
    move_order.append(move_order.pop(0))
        
compressed_map = compress_map(my_map)
non_zero_elems = compressed_map.size - compressed_map.nonzero()[0].size
print(f'non_zero_elems {non_zero_elems}')