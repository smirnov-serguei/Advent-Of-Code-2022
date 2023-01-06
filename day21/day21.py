# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 15:16:45 2022

@author: Serguei Smirnov
"""

filename = 'test.txt'
with open(filename) as file:
    data = file.read().splitlines()

monkeys_solved = {}
monkeys_unsolved = {}
for line in data:
    name, value = line.split(': ')
    if value.isnumeric():
        monkeys_solved[name] = int(value) # {'i':int(value)}
    else:
        monkeys_unsolved[name] = {'a':value.split()[0], 'op':value.split()[1], 
                                  'b':value.split()[2]}

while len(monkeys_unsolved):
    for m_key in list(monkeys_unsolved.keys()):
        m = monkeys_unsolved[m_key]
        if m['a'] in monkeys_solved and m['b'] in monkeys_solved:
            expr = f"{monkeys_solved[m['a']]}{m['op']}{monkeys_solved[m['b']]}"
            monkeys_solved[m_key] = eval(expr)
            monkeys_unsolved.pop(m_key)

print(f"Part 1: root {monkeys_solved['root']}")

