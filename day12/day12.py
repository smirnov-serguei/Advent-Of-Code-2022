# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 23:39:43 2022

@author: Serguei
"""

import networkx as nx

G = nx.MultiDiGraph()

# defines nodes
filename = 'input.txt'
with open(filename) as file:
    data = file.read().splitlines()
    for l_idx, line in enumerate(data):
        for c_idx, c in enumerate(line):
            if c=='S':
                elev = 0
                start = (l_idx, c_idx)
            elif c=='E':
                elev = ord('z') - ord('a')
                end = (l_idx, c_idx)
            else:
                elev = ord(c) - ord('a')
            G.add_node((l_idx, c_idx), elev=elev)

# define edges
for l_idx, _ in enumerate(data):
    for c_idx, _ in enumerate(line):
        curr_node_idx = (l_idx, c_idx)
        curr_node = G.nodes[curr_node_idx]
        # check left 
        if c_idx > 0:
            left_node_idx = (l_idx, c_idx - 1)
            left_node = G.nodes[left_node_idx]
            if curr_node['elev'] + 1 >= left_node['elev']:
                G.add_edge(curr_node_idx, left_node_idx)
            if curr_node['elev'] <= left_node['elev'] + 1:
                G.add_edge(left_node_idx, curr_node_idx)
        # check top
        if l_idx > 0:
            top_node_idx = (l_idx - 1, c_idx)
            top_node = G.nodes[top_node_idx]
            if curr_node['elev'] + 1 >= top_node['elev']:
                G.add_edge(curr_node_idx, top_node_idx)
            if curr_node['elev'] <= top_node['elev'] + 1:
                G.add_edge(top_node_idx, curr_node_idx)

sp = nx.shortest_path(G, source=start, target=end)
print(f'Task 1: len = {len(sp)-1}')

min_len = len(sp)
for l_idx, _ in enumerate(data):
    for c_idx, _ in enumerate(line):
        if G.nodes[(l_idx, c_idx)]['elev'] == 0:
            try:
                sp = nx.shortest_path(G, source=(l_idx, c_idx), target=end)
                min_len = min(min_len, len(sp) - 1)
            except:
                continue
print(f'Task 2: min_len = {min_len}')
                                                    
        
        
        
        