# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 21:31:02 2022

@author: Serguei Smirnov
"""

char_to_value = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2,
    }
value_to_char = {v: k for k, v in char_to_value.items()}
# value_to_char[3] = '='
# value_to_char[4] = '-'

base = 5

def snafu_to_dec(snafu):
    value = 0
    for idx, c in enumerate(snafu[::-1]):
        value += char_to_value[c] * base ** (idx)
    return value

def dec_to_snafu(dec):
    div = dec
    snafu = ''
    while div > 0:
        div, rem = divmod(div, base)
        if rem > 2:
            rem -= base
            div += 1
        snafu = value_to_char[rem] + snafu
    return snafu

with open('input.txt') as file:
    data = file.read().splitlines()

my_sum = 0
for line in data:
    my_sum += snafu_to_dec(line)
    
print(my_sum, dec_to_snafu(my_sum))
