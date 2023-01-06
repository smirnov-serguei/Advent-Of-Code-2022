# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 10:18:00 2022

@author: Serguei Smirnov
"""

from collections import deque

class MyStack():
    def __init__(self, length):
        self.length = length
        self.stack = deque(length*['noop']) # initial instruction stack
        self.X = 1 # initial register
        self.cycle = 1 # cycle counter
        self.signal_strength = []
        self.to_draw = ''
    
    def exec_cycle(self, new_exec):
        to_exec = self.stack.popleft()
        self.stack.append(new_exec)
        # print(f'Cycle {self.cycle} start, to_exec {to_exec}. X {self.X}')
        
        if to_exec.startswith('a'):
            self.inc_cycle()
            value = to_exec.split()[1]
            self.X += int(value)
            # print(f'Cycle {self.cycle-1} end, stack {self.stack}. X {self.X}')
        
        self.inc_cycle()
        # print(f'Cycle {self.cycle-1} end, stack {self.stack}. X {self.X}')
        
    def inc_cycle(self):
        self.signal_strength.append(self.X * self.cycle)
        pixel = (self.cycle - 1) % 40
        if not pixel:
            self.to_draw += '\n'
        # print(f'Cycle {self.cycle}, pixel {pixel}, X {self.X}')
        if pixel >= self.X-1 and pixel <= self.X+1:
            self.to_draw += '#'
        else:
            self.to_draw += '.'
        self.cycle += 1
        
        
my_stack = MyStack(1)

filename = 'input.txt'
with open(filename) as file:
    data = file.read().splitlines()
    for line in data:
        my_stack.exec_cycle(line)
        
# finish executing commands in the stack
while my_stack.stack.count('noop') < my_stack.length:
    my_stack.exec_cycle('noop')
        
total_strength = sum(my_stack.signal_strength[19::40])

print(f'Task 1: signal_strength = {total_strength}')
print('Task 2:', my_stack.to_draw)