# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 22:32:27 2022

@author: Serguei
"""
from collections import Counter

class Rope():
    def __init__(self, n_tails):
        self.n_tails = n_tails
        self.nodes = [[0,0]]
        for n in range(n_tails):
            self.nodes.append([0,0])
        self.visited = Counter()
    
    def move_head(self, direction, n_steps):
        for n in range(int(n_steps)):
            if direction == 'R':
                self.nodes[0][1] += 1
            elif direction == 'L':
                self.nodes[0][1] -= 1
            elif direction == 'U':
                self.nodes[0][0] += 1
            elif direction == 'D':
                self.nodes[0][0] -= 1
            self.update_tail(1)
            
    def update_tail(self, n):
        dx = self.nodes[n-1][1] - self.nodes[n][1]
        dy = self.nodes[n-1][0] - self.nodes[n][0]
        # move current tail node
        if (abs(dx) > 1 and abs(dy) > 1):
            self.nodes[n][1] += int(dx/2)
            self.nodes[n][0] += int(dy/2)
        elif (abs(dx) > 1):
            self.nodes[n][1] += int(dx/2)
            self.nodes[n][0] += dy
        elif (abs(dy) > 1):
            self.nodes[n][1] += dx
            self.nodes[n][0] += int(dy/2)
            
        if n == self.n_tails:
            # Save end tail location
            self.visited[tuple(self.nodes[n])] += 1
        else:
            # Update next tail node
            self.update_tail(n+1)

rope = Rope(1)
# Read data
filename = 'input.txt'
with open(filename, 'r') as file:
    data = file.read().splitlines()
    for line in data:
        rope.move_head(*line.split(' '))
        # print(rope.tail)
print(f'Part 1. number visited locations: {len(rope.visited)}')

rope = Rope(9)
# Read data
filename = 'input.txt'
with open(filename, 'r') as file:
    data = file.read().splitlines()
    for line in data:
        rope.move_head(*line.split(' '))
        # print(rope.nodes)
print(f'Part 2. number visited locations: {len(rope.visited)}')

