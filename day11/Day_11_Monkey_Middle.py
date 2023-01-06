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
        self.items = [factorint(int(i)) for i in items.split(',')]
        
    def set_operation(self, operation):
        self.operation = operation.split()[2:]
        if self.operation[0] != 'old':
            self.operation[0] = factorint(int(self.operation[0]))
        if self.operation[2] != 'old':
            self.operation[2] = factorint(int(self.operation[2]))
        
    def set_test_div(self, test_div):
        self.test_div = int(test_div.split()[-1])
        
    def set_test_true(self, test_true):
        self.test_true = int(test_true.split()[-1])
        
    def set_test_false(self, test_false):
        self.test_false = int(test_false.split()[-1])
        
    def do_operation(self, i):
        self.inspects += 1
        old = self.items[i]
        left = old if self.operation[0]=='old' else self.operation[0]
        right = old if self.operation[2]=='old' else self.operation[2]
        if self.operation[1]=='+': 
            # result = left + right
            result = self.add_primes(left, right)
        elif self.operation[1]=='*': 
            # result = left * right
            result = self.mult_primes(left, right)
        else: raise ValueError(f'Unrecognised operation {self.operation[1]}')
        # result = result // 3
        # test = (result % self.test_div == 0)
        test = (self.test_div in result)
        return (self.test_true, result) if test else (self.test_false, result)
    
    def do_all_operations(self):
        returns = []
        for i in range(len(self.items)):
            (to_monkey, item) = self.do_operation(i)
            returns.append((to_monkey, item))
        self.items = []
        return returns
    
    def mult_primes(self, a, b):
        mult = a.copy()
        for k in b.keys():
            if k in mult:
                mult[k] += b[k]
            else:
                mult[k] = b[k]
        return mult
    
    def add_primes(self, a, b):
        ac = a.copy()
        bc = b.copy()
        # find common part
        common = {}
        for k in ac.keys():
            if k in bc:
                exp = min(ac[k], bc[k])
                common[k] = exp
        # divide both by common
        for k in common.keys():
            ac[k] -= common[k]
            bc[k] -= common[k]
        # add the other part in float domain
        temp_sum = self.prime_to_float(ac) + self.prime_to_float(bc)
        # find prime of the sum and multiply all
        return self.mult_primes(common, factorint(temp_sum))
        
    def prime_to_float(self, p):
        result = 1
        for k in p.keys():
            result *= k**p[k]
        return result

# Initialize all monkeys
monkeys = []
filename = 'test.txt'
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

rounds = 20
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

print(f'Part 1: business = {business}')
