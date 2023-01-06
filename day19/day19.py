# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 19:00:34 2022

@author: Serguei Smirnov
"""
import re
import numpy as np
import time
# import math
import itertools

with open('input.txt') as file:
    data = file.read().splitlines()

# Extract all numbers from the string: blueprint number and
# robot costs: ore (ore), clay (ore), obsi (ore, clay), geode (ore, obsi)
blueprint = [int(i) for i in re.findall(r'\d+', data[2])]
global_max = 0
minutes_max = 32
# no need to create more robots than ore ever used per minute
max_needed_robots = [
    max(blueprint[1], blueprint[2], blueprint[3], blueprint[5]),
    blueprint[4], 
    blueprint[6]
    ] # ore, clay, and obsi

def triang(num): return sum([i for i in range(1,num+1)])

def compute(robots, ores, minute, could_build):
    global global_max 
    # Finished or Last minute, no need making robots
    if minute == minutes_max:
        return ores
    elif minute == minutes_max - 1:
        return ores + robots
    # check how many possibly can make, stop checking if less than global max
    if (global_max > ores[-1] + robots[-1] * (minutes_max - minute) 
        + triang(minutes_max - minute - 1)):
        return np.array([0, 0, 0, 0])
    
    start_robots = robots.copy()
    result = []
    
    # check if can make new robot, one per round
    if (not could_build[3] and 
        ores[0] >= blueprint[5] and ores[2] >= blueprint[6]): # geode robot
        cb = (False, False, False, False)
        end_robots = robots.copy()
        end_ores = ores.copy()
        end_ores[0] -= blueprint[5]
        end_ores[2] -= blueprint[6]
        end_robots[3] += 1
        end_ores += start_robots
        result.append(compute(end_robots, end_ores, minute+1, cb))
        # print(result)
        global_max = max(global_max, list(itertools.chain(*result))[-1])
    else:
        if (not could_build[2] and minute < minutes_max - 1 
            and start_robots[2] < max_needed_robots[2]
            and ores[0] >= blueprint[3] and ores[1] >= blueprint[4]): # obsi 
            cb = (False, False, False, False)
            end_robots = robots.copy()
            end_ores = ores.copy()
            end_ores[0] -= blueprint[3]
            end_ores[1] -= blueprint[4]
            end_robots[2] += 1
            end_ores += start_robots
            result.append(compute(end_robots, end_ores, minute+1, cb))
            global_max = max(global_max, list(itertools.chain(*result))[-1])
            
        if (not could_build[1] and minute < minutes_max - 1 
            and start_robots[1] < max_needed_robots[1]
            and ores[0] >= blueprint[2]): # clay robot
            cb = (False, False, False, False)
            end_robots = robots.copy()
            end_ores = ores.copy()
            end_ores[0] -= blueprint[2]
            end_robots[1] += 1
            end_ores += start_robots
            result.append(compute(end_robots, end_ores, minute+1, cb))
            global_max = max(global_max, list(itertools.chain(*result))[-1])
            
        if (not could_build[0] and minute < minutes_max - 1 
            and start_robots[0] < max_needed_robots[0]
            and ores[0] >= blueprint[1]): # ore robot
            cb = (False, False, False, False)
            end_robots = robots.copy()
            end_ores = ores.copy()
            end_ores[0] -= blueprint[1]
            end_robots[0] += 1
            end_ores += start_robots
            result.append(compute(end_robots, end_ores, minute+1, cb))
            global_max = max(global_max, list(itertools.chain(*result))[-1])
            
        # not building any robot this turn
        end_ores = ores.copy()
        end_ores += start_robots
        could_build = (ores[0] >= blueprint[1], 
                       ores[0] >= blueprint[2],
                       ores[0] >= blueprint[3] and ores[1] >= blueprint[4],
                       ores[0] >= blueprint[5] and ores[2] >= blueprint[6])
        result.append(compute(start_robots, end_ores, minute+1, could_build))
        global_max = max(global_max, list(itertools.chain(*result))[-1])
    # return highest geode count
    # print(result)
    return result[np.argmax([i[-1] for i in result])]
    
# starting params
robots = np.array([1, 0, 0, 0]) # ore, clay, obsidian, geode
ores = np.array([0, 0, 0, 0])
could_build = (False, False, False, False)

s_time = time.time()
result = compute(robots, ores, 0, could_build)
print(f'time = {time.time() - s_time:.2f}')

print(result)
