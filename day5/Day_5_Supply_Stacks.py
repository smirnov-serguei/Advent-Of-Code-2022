# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 13:58:37 2022

@author: Serguei
"""

filename = 'input.txt'

with open(filename, 'r') as file:
    # Read puzzle
    for idx, row in enumerate(file):
        if row.startswith(' 1'):
            break
        row = row[:-1] # remove EOL
        if idx==0:
            # Construct empty stacks
            n_stacks = int((len(row)+1)/4)
            # can't do: n_stacks*[[]], because each stack would be linked copy
            stacks = []
            for i in range(n_stacks):
                stacks.append([])
        # Fill stacks for current row
        for i in range(n_stacks):
            idx_char = i*4+1
            if row[idx_char].isalpha():
                # insert, not append because filling rows from top to bottom
                stacks[i].insert(0, row[idx_char])
    print(stacks)
            
    # Read moves
    for row in file:
        if row.startswith('move'):
            row = row[:-1] # remove EOL
            # Could also do regex here:
            temp = row.split(' ')
            n_moves = int(temp[1])
            st_from = int(temp[3]) - 1 # -1 to correct index
            st_to = int(temp[5]) - 1
            # Move items
            temp = []
            for i in range(n_moves):
                # Task 1
                # stacks[st_to].append(stacks[st_from].pop())
                # Task 2
                temp.append(stacks[st_from].pop())
            # Task 2
            temp.reverse()
            # not append here, because temp not one object:
            stacks[st_to] += temp
    print(stacks)
    
    # Read top crate of each stack
    result = ''
    for i in range(n_stacks):
        result += stacks[i][-1]
    print(result)