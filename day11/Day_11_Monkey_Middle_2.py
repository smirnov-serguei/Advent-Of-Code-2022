# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 11:47:59 2022

@author: Serguei Smirnov
"""
from sympy.ntheory import factorint
# import numpy as np

class Monkey():
    def __init__(self, i):
        self.i = i
        self.inspects = 0
        
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def __repr__(self):
        return(f'Monkey(i:{self.i}, items:{self.items})')
        
    def add_item(self, item):
        self.items.append(item)
        
    def set_items(self, items):
        self.temp_items = [int(i) for i in items.split(',')]
    
    def init_items(self, n_items):
        self.items = []
        for n in range(len(self.temp_items)):
            self.items.append([self.temp_items[n] for _ in range(n_items)])
    
    def init_divs(self, divs):
        self.divs = divs
        
    def set_operation(self, operation):
        self.operation = operation.split()[2:]
        if self.operation[0] != 'old':
            self.operation[0] = int(self.operation[0])
        if self.operation[2] != 'old':
            self.operation[2] = int(self.operation[2])
        
    def set_test_div(self, test_div):
        self.test_div = int(test_div.split()[-1])
        
    def set_test_true(self, test_true):
        self.test_true = int(test_true.split()[-1])
        
    def set_test_false(self, test_false):
        self.test_false = int(test_false.split()[-1])
        
    def do_operation(self, i):
        self.inspects += 1
        for div_iter in range(len(self.items[i])):
            curr_div = self.divs[div_iter]
            old = self.items[i][div_iter]
            left = old if self.operation[0]=='old' else self.operation[0]
            right = old if self.operation[2]=='old' else self.operation[2]
            if self.operation[1]=='+': 
                result = (left % curr_div + right % curr_div) % curr_div
            elif self.operation[1]=='*': 
                result = (left % curr_div * right % curr_div) % curr_div
            else: raise ValueError(f'Unknown operation {self.operation[1]}')
            self.items[i][div_iter] = result
        # result = result // 3
        test = (self.items[i][self.i] % self.test_div == 0)
        if test:
            return (self.test_true, self.items[i]) 
        else:
            return (self.test_false, self.items[i])
    
    def do_all_operations(self):
        returns = []
        for i in range(len(self.items)):
            (to_monkey, item) = self.do_operation(i)
            returns.append((to_monkey, item))
        self.items = []
        return returns

# Initialize all monkeys
monkeys = []
filename = 'input.txt'
with open(filename) as file:
    data = [line.lstrip() for line in file.read().splitlines()]
    for line in data:
        if line.startswith('M'):
            i = int(line[-2])
            monkeys.append(Monkey(i))
        elif line.startswith('S'):
            monkeys[i].set_items(line.split(':')[1])
        elif line.startswith('O'):
            monkeys[i].set_operation(line.split(':')[1])
        elif line.startswith('T'):
            monkeys[i].set_test_div(line.split(':')[1])
        elif line.startswith('If t'):
            monkeys[i].set_test_true(line.split(':')[1])
        elif line.startswith('If f'):
            monkeys[i].set_test_false(line.split(':')[1])
for m in monkeys:
    m.init_items(len(monkeys))
    m.init_divs([m.test_div for m in monkeys])

rounds = 10000
for r in range(rounds):
    print(f'\rRound {r}/{rounds}', end='', flush=True)
    for m in monkeys:
        returns = m.do_all_operations()
        for (to_monkey, item) in returns:
            monkeys[to_monkey].add_item(item)
print(' Done!')

for m in monkeys:
    print(f'Monkey {m.i}, inspects: {m.inspects}')

all_inspects = [m.inspects for m in monkeys]
all_inspects.sort()
business = all_inspects[-2] * all_inspects[-1]

print(f'Part 2 business = {business}')
