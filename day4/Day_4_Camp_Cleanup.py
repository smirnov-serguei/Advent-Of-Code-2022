# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 13:27:08 2022

@author: Serguei
"""

filename = 'input.txt'
counter = 0
counter2 = 0

def range_contains(range1, range2):
    for j in range2:
        if j not in range1:
            return False
    return True

def range_overlaps(range1, range2):
    for j in range2:
        if j in range1:
            return True
    return False

with open(filename, 'r') as file:
    for row in file:
        row = row[:-1] # remove EOL
        temp1, temp2 = row.split(',')
        elf1 = range(int(temp1.split('-')[0]), 
                     int(temp1.split('-')[1])+1)
        elf2 = range(int(temp2.split('-')[0]), 
                     int(temp2.split('-')[1])+1)
        if range_contains(elf1, elf2) or range_contains(elf2, elf1):
            counter +=1
        if range_overlaps(elf2, elf1):
            counter2 +=1
            
print(f'Part 1: {counter}')
print(f'Part 2: {counter2}')