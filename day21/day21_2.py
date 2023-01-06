# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 15:16:45 2022

@author: Serguei Smirnov
"""
import time
from sympy import Symbol

filename = 'input.txt'
with open(filename) as file:
    data = file.read().splitlines()

monkeys_solved = {}
monkeys_unsolved = {}
for line in data:
    name, value = line.split(': ')
    if value.isnumeric():
        if name == 'humn':
            monkeys_solved[name] = name
        else:
            monkeys_solved[name] = (value) # {'i':int(value)}
    else:
        monkeys_unsolved[name] = {'a':value.split()[0], 'op':value.split()[1], 
                                  'b':value.split()[2]}

while len(monkeys_unsolved) > 1:
    for m_key in list(monkeys_unsolved.keys()):
        if m_key != 'root':
            m = monkeys_unsolved[m_key]
            if m['a'] in monkeys_solved and m['b'] in monkeys_solved:
                expr = f"({monkeys_solved[m['a']]}{m['op']}{monkeys_solved[m['b']]})"
                if 'humn' in expr:
                    monkeys_solved[m_key] = (expr)
                else:
                    monkeys_solved[m_key] = eval(expr)
                monkeys_unsolved.pop(m_key)

humn = Symbol('humn')
print(monkeys_solved[monkeys_unsolved['root']['b']])
print(eval(monkeys_solved[monkeys_unsolved['root']['a']]))
