# coding: utf-8
import pyperclip
s = pyperclip.paste()
s
lines = s.splitlines()
import regex
LAST_TWO_INTS_RE = regex.compile(r'((?<=\s+)(-?\d+))(?=\s*$)')
for line in lines:
    match LAST_TWO_INTS_RE.search(line):
        case regex.Match() as m:
            print(m[0])
        
LAST_TWO_INTS_RE = regex.compile(r'((?<=\s+)(-?\d+))\{2}(?=\s*$)')
last_two_ints = []
for line in lines:
    match LAST_TWO_INTS_RE.search(line):
        case regex.Match() as m:
            last_two_ints.append(m[0])
            
last_two_ints
lines
regex.search(r'((\s\+)(-?\d+))\{2}(?=\s*$)', lines[1])
regex.search(r'((\s\+)(-?\d+))\{2}(?=\s*)', lines[1])
regex.search(r'((\s\+)(-?\d+))\{2}', lines[1])
regex.search(r'((\s\+)(-?\d+))', lines[1])
regex.search(r'((\s+)(-?\d+))\{2}(?=\s*$)', lines[1])
regex.search(r'((\s+)(-?\d+))\{2}', lines[1])
regex.search(r'((\s+)(-?\d+))', lines[1])
regex.search(r'((\s+)(-?\d+)){2}', lines[1])
regex.search(r'((\s+)(-?\d+)){2}$', lines[1])
regex.search(r'((\s+)(-?\d+)){2}\s*$', lines[1])
LAST_TWO_INTS_RE = regex.compile(r'((\s+)(-?\d+)){2}(?=\s*$)')
regex.search(r'((\s+)(-?\d+)){2}(?=\s*$)', lines[1])
LAST_TWO_INTS_RE.search(lines[1])
get_ipython().run_line_magic('rep', '7')
for line in lines:
    match LAST_TWO_INTS_RE.search(line):
        case regex.Match() as m:
            print(m[0])
            
get_ipython().run_line_magic('rep', '9-11')
last_two_ints = []
for line in lines:
    match LAST_TWO_INTS_RE.search(line):
        case regex.Match() as m:
            last_two_ints.append(m[0])
            
last_two_ints
[tuple(s.split()) for s in last_two_ints]
coordinate_str = [tuple(s.split()) for s in last_two_ints]
coordinates = [(int(x), int(y)) for x, y in coordinate_str]
coordinates
s = ''
for x, y in coordinates:
    s += f'<use href="#point" x="{x}" y="{y}" class="hand-calc"/>\n'
    
s
print(s)
pyperclip.copy(s)
s = pyperclip.paste()
s
print(s)
lines = s.splitlines9)
lines = s.splitlines()
lines = [line.strip() for line in s.splitlines()]
lines
get_ipython().run_line_magic('pwd', '')
get_ipython().run_line_magic('whos', '')
from pathlib import Path
lines = Path('all_types_in_jupyter_lab_session.txt').read_lines().splitlines()
lines = Path('all_types_in_jupyter_lab_session.txt').read_text().splitlines()
lines
lines[34:]
lines[0][34:]
lines[0][33:]
lines[0][57:]
VARIABLE, TYPE, DATA_INFO=slice(0,34),slice(34,57),slice(57,None)
[{'variable': line[VARIABLE], 'type': line[TYPE], 'data_info': line[DATA_INFO]} for line in lines[2:]][:5]
VARIABLE, TYPE, DATA_INFO=slice(0,34),slice(34,56),slice(56,None)
[{'variable': line[VARIABLE], 'type': line[TYPE], 'data_info': line[DATA_INFO]} for line in lines[2:]][:5]
VARIABLE, TYPE, DATA_INFO=slice(0,33),slice(33,56),slice(56,None)
[{'variable': line[VARIABLE], 'type': line[TYPE], 'data_info': line[DATA_INFO]} for line in lines[2:]][:5]
[{'variable': line[VARIABLE].strip(), 'type': line[TYPE].strip(), 'data_info': line[DATA_INFO].strip()} for line in lines[2:]][:5]
get_ipython().run_line_magic('whos', '')
import json
with open('all_types_in_jupyter_lab_session.json', mode='w') as fp:
    ...
    
types_in_jupyter_lab_session = [{'variable': line[VARIABLE].strip(), 'type': line[TYPE].strip(), 'data_info': line[DATA_INFO].strip()} for line in lines[2:]]
with open('all_types_in_jupyter_lab_session.json', mode='w') as fp:
    json.dump(types_in_jupyter_lab_session, fp, indent=2)
    
from itertools import groupby
types_in_jupyter_lab_session.sort(key=lambda t:(t['type'], t['variable']))
[(key, list(values)) for key, value in groupby(types_in_jupyter_lab_session, key=lambda t:t['type'])]
values_grouped_by_type = [(key, list(values)) for key, values in groupby(types_in_jupyter_lab_session, key=lambda t:t['type'])]
values_grouped_by_type
for _, values in values_grouped_by_type:
    for value in values:
        del value['type']
        
values_grouped_by_type
import pyyaml
get_ipython().run_line_magic('pip', 'install pyyaml')
import pyyaml
import yaml
yaml.dump(values_grouped_by_type)
print(yaml.dump(values_grouped_by_type))
values_grouped_by_type
values_grouped_by_type_dict = {key:values for key, values in values_grouped_by_type}
values_grouped_by_type_dict
yaml.dump(values_grouped_by_type_dict)
print(yaml.dump(values_grouped_by_type_dict))
class YamlfiedType(yaml.YAMLObject):
    yaml_tag = u'!YamlfiedType'
    
    def __init__(self, data_info, variable):
        self.data_info = data_info
        self.variable = variable
    def __repr__(self):
print(yaml.dump(values_grouped_by_type_dict))
with open('all_types_in_jupyter_lab_session.yaml', mode='w') as fp:
    yaml.dump(values_grouped_by_type_dict)
    
get_ipython().run_line_magic('cat', '"all_types_in_jupyter_lab_session.yaml"')
with open('all_types_in_jupyter_lab_session.yaml', mode='w') as fp:
    yaml.dump(values_grouped_by_type_dict, fp)
    
get_ipython().run_line_magic('cat', '"all_types_in_jupyter_lab_session.yaml"')
get_ipython().system('vimr all_types_in_jupyter_lab_session.yaml')
with open('all_types_in_jupyter_lab_session.yaml') as fp:
    all_types_renamed = yaml.load(fp)
    
with open('all_types_in_jupyter_lab_session.yaml', mode='w') as fp:
    contents = fp.read()
    
with open('all_types_in_jupyter_lab_session.yaml', mode='w') as fp:
    yaml.dump(values_grouped_by_type_dict, fp)
    
s = pyperclip.paste()
s
s = pyperclip.paste()
s
lines = s.splitlines()
lines
line = [line.split() for line in lines]
line
lines = line
[ [line[0]] + [int(s) for s in line[1:]] for line in lines]
lines = [ [line[0]] + [int(s) for s in line[1:]] for line in lines]
['\t'.join(line) for line in lines]
get_ipython().run_line_magic('rep', '100-102')
lines = s.splitlines()
lines
lines = [line.split() for line in lines]
get_ipython().run_line_magic('rep', '103 107')
lines
[line[1:] for line in lines]
['\t'.join(line) for line in lines]
['\t'.join(line[1:]) for line in lines]
'\n\n\n'.join(_)
'\n\n\n'.join(['\t'.join(line[1:]) for line in lines])
pyperclip.copy('\n\n\n'.join(['\t'.join(line[1:]) for line in lines]))
s = pyperclip.paste()
s
print(s)
lines = s.splitlines()
lines
lines = [line for line in lines if len(line) > 0]
lines
import io
with io.StringIO() as fp:
    for line in lines:
        print(f'<path d="{line}"/>', file=fp)
        
with io.StringIO() as fp:
    for line in lines:
        print(f'<path d="{line}"/>', file=fp)
    s = fp.getvalue()
    
s
print(s)
pyperclip.copy(s)
s = pyperclip.paste()
s
lines = s.splitlines()
lines
lines = ['\t'.join(line.split()) for line in lines]
lines
s = [line.split() for line in pyperclip.paste().splitlines()]
s
commands = [(line[0], [int(n) for n in line[1:]]) for line in s]
commands
commands = [(line[0], tuple(int(n) for n in line[1:])) for line in s]
commands
get_ipython().run_line_magic('whos', '')
from typing import NamedTupe
from typing import NamedTuple
class Point(NamedTuple):
    x: int
    y: int
    
from more_itertools import chunked, flatten
commands
reformatted_commands = []
for cmd, args in commands:
    print (cmd, list(chunked(args, 2)))
    
reformatted_commands = []
for cmd, args in commands:
    print (cmd, list(tuple(c) for c in chunked(args, 2)))
    
reformatted_commands = []
for cmd, args in commands:
    reformatted_commands.append((cmd, list(tuple(c) for c in chunked(args, 2))))
    
reformatted_commands
path_defs = reformatted_commands[0][1] + reformatted_commands[1][1]
path_defs
start_point = path_defs[-1][-1]
start_point
start_point = path_defs[-1]
start_point
path_defs = [reformatted_commands[0][1] + reformatted_commands[1][1]]
path_defs
command_dicts = []
for cmd, args in reformatted_commands:
    for arg in args:
        command_dicts.append({'command': cmd, 'args': [Point(**arg) for arg in args]})
        
command_dicts = []
for cmd, args in reformatted_commands:
    for arg in args:
        command_dicts.append({'command': cmd, 'args': [Point(*arg) for arg in args]})
        
command_dicts
command_dicts = []
for cmd, args in reformatted_commands:
    for arg in args:
        command_dicts.append({'command': cmd, 'args': [Point(*arg) for arg in args]})
        
command_dicts
command_dicts = []
for cmd, args in reformatted_commands:
    command_dicts.append({'command': cmd, 'args': [Point(*arg) for arg in args]})
    
command_dicts
def Point__add__(self, other):
    return Point(self.x + other.x, self.y + other.y)
    
Point.__add__ == Point__add__
Point.__add__ = Point__add__
from itertools import pairwise
for d1, d2 in command_dicts:
    print([d1[-1]] + [d1[-1] + d for d in d2])
    
command_dicts
list(pairwise(command_dicts))
command_dicts[0][args]
command_dicts[0]['args']
offset = command_dicts[0]['args']
command_dicts[1]
offset * 3
class Vector():
    def __init__(self, points: list):
        self.points = points
    def __add__(self, other):
        ...
        
get_ipython().run_line_magic('history', '150-170 n')
class Vector():
    def __init__(self, points: list):
        self.points = points
    def __add__(self, other):
        return [Point(p1+p2) for p1, p2 in  zip(self.points, other.points)]
        
