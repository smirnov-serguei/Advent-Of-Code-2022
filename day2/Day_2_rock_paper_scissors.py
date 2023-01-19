# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 14:43:03 2022

@author: Serguei Smirnov
"""
import os
import time

VALUE_LOSE = 0
VALUE_DRAW = 3
VALUE_WIN = 6
VALUE_SHAPE = {'r':1, 'p':2, 's':3}
OP_PLAY = {'A':'r', 'B':'p', 'C':'s'}
MY_PLAY = {'X':'r', 'Y':'p', 'Z':'s'}

def match(op, my):
    op = OP_PLAY[op]
    my = MY_PLAY[my]
    shape = VALUE_SHAPE[my]
    
    if op==my:
        value_round = VALUE_DRAW
    elif ((op=='r' and my=='s') or (op=='s' and my=='p') 
            or (op=='p' and my=='r')):
        value_round = VALUE_LOSE
    else:
        value_round = VALUE_WIN

    return shape + value_round

def match2(op, my):
    op = OP_PLAY[op]

    if my=='Y':
        value_round = VALUE_DRAW
        my_shape = op
    elif my=='X':
        value_round = VALUE_LOSE
        if op=='r': my_shape='s'
        elif op=='p': my_shape='r'
        else: my_shape='p'
    else:
        value_round = VALUE_WIN
        if op=='r': my_shape='p'
        elif op=='p': my_shape='s'
        else: my_shape='r'
    
    shape = VALUE_SHAPE[my_shape]
    return shape + value_round

def main():
    dirname = os.path.dirname(__file__)
    filename = r'\input.txt'
    my_score = 0
    my_score2 = 0

    with open(dirname + filename, 'r') as file:
        for row in file:
            row = row[:-1] # remove EOL
            op, my = row.split(' ')
            my_score += match(op, my)
            my_score2 += match2(op, my)

    print('Part 1:', my_score)
    print('Part 2:', my_score2)


if __name__ == '__main__':
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f'Time: {t2-t1:.3f} s')
