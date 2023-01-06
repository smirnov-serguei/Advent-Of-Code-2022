# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 19:25:52 2022

@author: Serguei
"""
import numpy as np

# Read data
filename = 'input.txt'
with open(filename, 'r') as file:
    data = file.read().splitlines()

# Create matrix
matrix = np.empty((len(data), len(data[0])), dtype=int)
for l, line in enumerate(data):
    for c, char in enumerate(line):
        matrix[l, c] = int(char)

# Perimeter trees
count_perim = 2*l + 2*c 
count_mid = 0
# Loop internal trees
for i in range(1, l):
    for j in range(1, c):
        # Check left
        if (np.all(matrix[i, :j] < matrix[i, j])):
            count_mid += 1
        # Check right
        elif (np.all(matrix[i, j+1:] < matrix[i, j])):
            count_mid += 1
        # Check top
        elif (np.all(matrix[:i, j] < matrix[i, j])):
            count_mid += 1
        # Check bottom
        elif (np.all(matrix[i+1:, j] < matrix[i, j])):
            count_mid += 1
print(f'Part 1: {count_perim + count_mid}')

# Part 2
count_max = 0
for i in range(1, l):
    for j in range(1, c):
        check_left = matrix[i, :j] < matrix[i, j]
        if not check_left.any(): # all bigger
            count_left = 1
        elif check_left.all(): # all smaller
            count_left = len(check_left)
        else:
            count_left = 1 + check_left[::-1].argmin()
        
        check_right = matrix[i, j+1:] < matrix[i, j]
        if not check_right.any(): # all bigger
            count_right = 1
        elif check_right.all(): # all smaller
            count_right = len(check_right)
        else:
            count_right = 1 + check_right.argmin()
        
        check_top = matrix[:i, j] < matrix[i, j]
        if not check_top.any(): # all bigger
            count_top = 1
        elif check_top.all(): # all smaller
            count_top = len(check_top)
        else:
            count_top = 1 + check_top[::-1].argmin()
        
        check_bottom = matrix[i+1:, j] < matrix[i, j]
        if not check_bottom.any(): # all bigger
            count_bottom = 1
        elif check_bottom.all(): # all smaller
            count_bottom = len(check_bottom)
        else:
            count_bottom = 1 + check_bottom.argmin()
        
        count_all = count_left * count_right * count_top * count_bottom
        count_max = max(count_max, count_all)
     
print(f'Part 2: {count_max}')






