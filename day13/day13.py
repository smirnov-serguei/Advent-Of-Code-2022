# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 01:15:14 2022

@author: Serguei
"""

class MyItem():
    def __init__(self, l):
        self.l = l
    def __lt__(self, other):
        return compare(self.l, other.l)
    def __repr__(self):
        return(f'MyItem(l:{self.l})')
    
def compare(left, right):
    len_l = len(left)
    len_r = len(right)
    k = 0
    res = None
    for l, r in zip(left, right):
        k += 1
        result = None
        if isinstance(l, list) and isinstance(r, list):
            result = compare(l, r)
        elif isinstance(l, list) and isinstance(r, int):
            result = compare(l, [r])
        elif isinstance(l, int) and isinstance(r, list):
            result = compare([l], r)
        elif isinstance(l, int) and isinstance(r, int):
            if l == r: continue
            elif l < r: result = True
            elif r < l: result = False
        
        if result != None:
            return result
    if len_l == len_r:
        res = None
    elif k > len_l-1:
        res = True
    elif k > len_r-1:
        res = False
    
    if res != None:
        return res

left = None
right = None 
idx_right = []
filename = 'input.txt'
with open(filename) as file:
    data = file.read().splitlines()
    for l_idx, line in enumerate(data):
        if left == None:
            left = eval(line)
        elif right == None:
            right = eval(line)
            if compare(left, right):
                idx_right.append((l_idx-1)/3+1) # convert line nb to pair nb
        else:
            left = None
            right = None
print(f'Part 1: sum indeces = {sum(idx_right)}')

# Part 2
items = []
filename = 'input.txt'
with open(filename) as file:
    data = file.read().splitlines()
    for l_idx, line in enumerate(data):
        if line: 
            items.append(MyItem(eval(line)))
start_item = MyItem([[2]])
stop_item = MyItem([[6]])
items.append(start_item)
items.append(stop_item)
items.sort()
key = (items.index(start_item) + 1) * (items.index(stop_item) + 1)
print(f'Part 2: {key}')
        



