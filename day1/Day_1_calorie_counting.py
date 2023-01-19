# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 14:43:03 2022

@author: Serguei Smirnov
"""
import os
import time

def main():
    dirname = os.path.dirname(__file__)
    filename = r'\input.txt'
    elves = []
    calories = 0

    with open(dirname + filename, 'r') as file:
        for row in file:
            row = row[:-1] # remove EOL
            # row contains a number
            if row:
                calories += int(row)
            # row is empty
            else:
                elves.append(calories)
                calories = 0
        # add last elf to the list manually
        elves.append(calories)

    elves.sort(reverse=True)
    calories_sum = sum(elves[:3])

    print(f'Part 1: {elves[0]}')
    print(f'Part 2: {calories_sum}')

if __name__ == '__main__':
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f'Time: {t2-t1:.3f} s')
