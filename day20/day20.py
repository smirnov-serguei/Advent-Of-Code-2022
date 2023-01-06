# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 20:11:23 2022

@author: Serguei Smirnov
"""
import math

class MyItem():
    def __init__(self, i):
        self.i = int(i)
        
    def __lt__(self, other):
        if isinstance(other, MyItem):
            other_i = other.i
        else:
            other_i = int(other)
        return self.i < other_i
    
    def __repr__(self):
        return(f'MyItem({self.i})')
        
# key = 1
# rounds = 1
key = 811589153
rounds = 10

filename = 'input.txt'
with open(filename) as file:
    data = [MyItem(int(i)*key) for i in file.read().splitlines()]

# copy list to save the original order
data_c = data.copy()
# Move items around
for _ in range(rounds):
    for item in data_c:
        index = data.index(item)
        index_to = (index + item.i) % (len(data) - 1)
        data.insert(index_to, data.pop(index))

# Find 0 and get results
item_zero = [item for item in data if item.i==0][0]
index_zero = data.index(item_zero)
coords = []
for i in (1000, 2000, 3000,):
    index_at = (index_zero + i) % len(data)
    coords.append(data[index_at].i)

print(f'Result {sum(coords)}')