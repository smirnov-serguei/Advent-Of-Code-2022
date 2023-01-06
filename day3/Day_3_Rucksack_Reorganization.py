# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 00:22:05 2022

@author: Serguei
"""

from collections import Counter

filename = 'input.txt'
sum_prio = 0

def letter_prio(k):  
    if k.islower():
        prio = ord(k) - ord('a') + 1
    else:
        prio = ord(k) - ord('A') + 27
    return prio
    
with open(filename, 'r') as file:
    for row in file:
        row = row[:-1] # remove EOL
        half_len = int(len(row)/2)
        str_a = row[:half_len]
        str_b = row[half_len:]
        sack_a = Counter(str_a)
        sack_b = Counter(str_b)
        for k in sack_a.keys():
            if k in sack_b:
                break
        sum_prio += letter_prio(k)

sum_prio2 = 0
counter = 0
group = [None, None, None]

with open(filename, 'r') as file:
    for row in file:
        row = row[:-1] # remove EOL
        group[counter] = Counter(row)
        
        if counter==2:
            for k in group[2].keys():
                if (k in group[0]) and (k in group[1]):
                    break
            sum_prio2 += letter_prio(k)
            counter = 0
        else:
            counter += 1

print(f'Part 1: {sum_prio}')
print(f'Part 2: {sum_prio2}')