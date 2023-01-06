# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 16:41:36 2022

@author: Serguei
"""

from collections import deque

def buffer_diff(b):
    for c in b:
        if b.count(c) > 1:
            return False
    return True

filename = 'input.txt'
# maxlen = 4 # Task 1
maxlen = 14 # Task 2

buffer = deque(maxlen=maxlen)

with open(filename, 'r') as file:
    for row in file:
        row = row[:-1] # remove EOL
        for idx, char in enumerate(row):
            buffer.appendleft(char)
            if idx >= maxlen-1 and buffer_diff(buffer):
                print(idx+1)
                break

