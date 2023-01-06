# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 17:32:55 2022

@author: Serguei
"""
from anytree import AnyNode, RenderTree

class MyNode(AnyNode):
    def __init__(self, name, is_folder, size=None, parent=None, children=None):
        super().__init__()
        self.name = name
        self.is_folder = is_folder
        self.size = size
        self.parent = parent
        if children:
            self.children = children
    
    def __lt__(self, other):
        return self.size < other.size
    
    def draw(self):
        for pre, _, node in RenderTree(self):
            tag = '(dir)' if node.is_folder else '(file)' 
            print(f'{pre}{node.name}'.ljust(16), 
                  f' {tag}'.ljust(7), 
                  f'size = {node.size}')
    
    def get_child(self, name):
        for idx, child in enumerate(self.children):
            if child.name == name:
                break
            if idx == len(self.children) - 1:
                raise ValueError(f'{self.name}: Child {name} not found!')
        return child
    
    def update_size(self):
        new_size = 0
        for child in self.children:
            if child.is_folder: 
                child.update_size()
            new_size += child.size
        self.size = new_size

# Read input
filename = 'input.txt'
root = MyNode('/', True)
cd = root
with open(filename, 'r') as file:
    for row in file:
        row = row[:-1] # remove EOL

        # Command line
        if row.startswith('$'):
            row = row[2:]
            if row.startswith('cd'):
                new_dir_str = row.split(' ')[1]
                if new_dir_str=='/':
                    cd = root
                elif new_dir_str=='..':
                    cd = cd.parent
                else:
                    cd = cd.get_child(new_dir_str)
            # elif row.startswith('ls'):
            #     break
        
        # Output line
        else:
            temp = row.split(' ')
            if temp[0]=='dir':
                new_folder = MyNode(temp[1], True, parent=cd)
            else:
                new_file = MyNode(temp[1], False, size=int(temp[0]),
                                  parent=cd)
            
# Draw tree
root.update_size()
# root.draw()

# Find all of the directories with a total size of at most 100000
sum_sizes = 0
for node in root.descendants:
    if node.is_folder and node.size <= 100000:
        sum_sizes += node.size
print(f'Part 1: {sum_sizes}')

# Part 2
size_total = 70000000
size_need = 30000000
size_free = size_total - root.size
size_min_delete = size_need - size_free

all_folders = [f for f in root.descendants if f.is_folder]
all_folders.sort() 
for f in all_folders:
    if f.size > size_min_delete:
        break
print('Part 2:', f)
