# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 22:45:35 2022

@author: Serguei Smirnov
"""
import networkx as nx
import time

G = nx.Graph()

filename = 'input.txt'
with open(filename) as file:
    data = file.read().splitlines()
    
# Create graph
valves = []
for line in data:
    temp = line.split(';')
    valve = {
        'name' : temp[0].split()[1],
        'rate' : int(temp[0].split('=')[1]),
        'to' : [v.split()[-1] for v in temp[1].split(',')]
        }
    valves.append(valve)
    G.add_node(
        valve['name'], 
        rate = valve['rate'],
        visited = valve['rate']==0,
        )
    for v in valve['to']:
        G.add_edge(valve['name'], v, weight=1)

# nx.draw_networkx(G)

# pre-calculate all shortest path lengths
shortest_paths = dict(nx.shortest_path_length(G))
non_null_nodes = [n for n in dict(G.nodes) if not G.nodes[n]['visited']]

def best_rate(start_node, curr_step, visited):
    if all(visited.values()):
        return 0
    max_rate = 0
    for n in non_null_nodes: #G.nodes:
        # print(n)
        length = shortest_paths[start_node][n]
        if (not visited[n]) and curr_step > length + 1:
            c_visited = visited.copy()
            c_visited[n] = True
            possible_rate = ((curr_step - length - 1) * G.nodes[n]['rate']
                             + best_rate(n, curr_step-length-1, c_visited))
            if possible_rate > max_rate:
                max_rate = possible_rate
    return max_rate

def best_rate_two(curr_node, other_node, curr_step, other_step, visited):
    if all(visited.values()):
        return 0
    max_rate = 0
    for n in non_null_nodes: #G.nodes:
        if curr_step >= other_step:
            length = shortest_paths[curr_node][n]
            if (not visited[n]) and curr_step > length + 1:
                c_visited = visited.copy()
                c_visited[n] = True
                possible_rate = ((curr_step - length - 1) * G.nodes[n]['rate']
                                 + best_rate_two(
                                             n, other_node, 
                                             curr_step-length-1, other_step, 
                                             c_visited))
                if possible_rate > max_rate:
                    max_rate = possible_rate
        else:
            length = shortest_paths[other_node][n]
            if (not visited[n]) and other_step > length + 1:
                c_visited = visited.copy()
                c_visited[n] = True
                possible_rate = ((other_step - length - 1) * G.nodes[n]['rate']
                                 + best_rate_two(
                                             curr_node, n, 
                                             curr_step, other_step-length-1,
                                             c_visited))
                if possible_rate > max_rate:
                    max_rate = possible_rate
    return max_rate

# Find best rate
total_rate = 0
start_node = 'AA'
curr_step = 30
visited = nx.get_node_attributes(G, 'visited')

start_time = time.time()
result = best_rate(start_node, curr_step, visited)
end_time = time.time()

print(f'Part 1, result  = {result}, exec time = {end_time-start_time} s')

# Find best rate === 900 SECONDS ===
total_rate = 0
start_node = 'AA'
curr_step = 26
visited = nx.get_node_attributes(G, 'visited')

start_time = time.time()
result = best_rate_two(start_node, start_node, curr_step, curr_step, visited)
end_time = time.time()

print(f'Part 2, result  = {result}, exec time = {end_time-start_time} s')



