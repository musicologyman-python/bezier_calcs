#%%
from collections.abc import Iterable, Mapping
import dataclasses
import functools
import io
from itertools import chain
import logging
from pathlib import Path
from pprint import pprint
from typing import Any

from more_itertools import flatten
import regex

#%%

def read_path_def_strings(filename='path_defs.txt') -> list[str]:
    ''' read a file containing one path definition per line
    '''
    return Path('path_defs.txt').read_text().splitlines()

#%%
@dataclasses.dataclass
class Point():
    ''' A class representing a point on a Cartesian plane
    '''
    x: int
    y: int

    def __rmul(self: 'Point', other: int) -> 'Point':
        ''' Corresponds to scalar multiplication
        '''
        return Point(self.x * other, self.y * other)

    def __add__(self: 'Point', other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self: 'Point', other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y)
    
    def __repr__(self):
        return f'{self.__class__.__name__}(x={self.x}, y={self.y})'
    

class PathDefCommand():
    ''' Represents one instruction in the `d` attribute of an SVG `path` element.
    '''
    def __init__(self, command: str, args: list[Point]):
        self.command = command
        self.args = args
        
    def __repr__(self):
        return f'{self.__class__.__name__}(command="{self.command}", ' \
               f'args={self.args})'
    
    def __str__(self):
        return self.__repr__()


def arglist_to_points(arglist: Iterable[str]) -> list[Point]:
    """ Convert a string of integers to a Point
    >>> argstring_to_points('-45 0 -69 -34 -69 -88')
    [Point(x=-45, y=0), Point(x=-69, y=-34), Point(x=-69, y=-88)
    """
    args = [int(arg) for arg in arglist]
    return [Point(args[i], args[i+1]) for i in range(0, len(args), 2)]

def create_path_def_command(path_def_dict: Mapping[str, list[str]]) -> PathDefCommand:
    command : str = path_def_dict['command'][0]
    arglist: list[str] = path_def_dict['args']
    match command:
        case 'h':
            command = 'l'
            args = [Point(x=int(arglist[0]), y=0)]
        case 'v':
            command = 'l'
            args = [Point(x=0, y=int(arglist[0]))]
        case _:
            args: list[Point] = arglist_to_points(arglist)
    return PathDefCommand(command = command, args=args)


#%%

COMMAND_RE = regex.compile(r'''(?ix)(?P<command>[clmsvz])
                               (\s+(?P<args>-?\d+(\.d+)?))*''')

def parse_path_def(path_def: str) -> list[PathDefCommand]:
    return [create_path_def_command(m.capturesdict())
                                 for m in COMMAND_RE.finditer(path_def)]
 
def parse_path_defs(path_defs: Iterable[str]) -> list[list[PathDefCommand]]:
    return [parse_path_def(pd) for pd in path_defs]
    
parsed_path_defs = parse_path_defs(read_path_def_strings())

pprint(parsed_path_defs)

# %%
     
def to_command_string(parsed_path_def: list[PathDefCommand]) -> str:
    with io.StringIO() as fp:
        for path_def in parsed_path_def:
            fp.write(f'{path_def.command} ')
            for arg in path_def.args:
                fp.write(f' {arg.x} {arg.y}')
            fp.write('\n')
        return fp.getvalue()
     
for ppd in parsed_path_defs:
    print(to_command_string(ppd)) 

# %%

def relative_to_absolute(rel_path_def: Iterable[PathDefCommand]) -> Iterable[PathDefCommand]:
    offset = Point(x=0, y=0)
    next_tangent = Point(x=0, y=0)
    pdc: PathDefCommand
    for pdc in rel_path_def:
        match pdc.command:
            case 'M':
                yield pdc
            case 'z':
                yield pdc 
            case 'c':
                next_pdc = PathDefCommand(
                    command = pdc.command.upper(),
                    args=[offset + arg for arg in pdc.args]
                )
                next_tangent = next_pdc.args[-1] - next_pdc.args[-2]
                yield next_pdc
            case 'l':
                yield PathDefCommand(
                    command = pdc.command.upper(),
                    args=[offset + arg for arg in pdc.args]
                )
            case 's':
                next_pdc = PathDefCommand(
                    command = 'C',
                    args = [offset + next_tangent, 
                            offset + pdc.args[0], 
                            offset + pdc.args[1]]
                ) 
                next_tangent = next_pdc.args[-1] - next_pdc.args[-2]
                yield next_pdc
            case _:
                logging.debug(f'The command {pdc.command}was not handled')

        if pdc.args:
            offset = offset + pdc.args[-1]
# %%

absolute_path_defs = [list(relative_to_absolute(parsed_path_def))
                     for parsed_path_def in parsed_path_defs]

pprint(absolute_path_defs)
# %%
for apd in absolute_path_defs:
    print(to_command_string(apd))
# %%
def find_extrema(path_defs: Iterable[PathDefCommand]) -> Any:
    pdc: PathDefCommand
    all_points = list(flatten([pdc.args for pdc in path_defs]))
    return {
        "min_x" : min([p.x for p in all_points]),
        "max_x" : max([p.x for p in all_points]),
        "min_y" : min([p.y for p in all_points]),
        "max_y" : max([p.y for p in all_points])
    }
   

for apd in absolute_path_defs:
    pprint(find_extrema(apd))
# %%

with open('absolute_curves.xml', mode='w') as fp:
    printf = functools.partial(print, file=fp)
    printf('<xml>')
    for rpd in parsed_path_defs:
        printf(f'<path d="{to_command_string(rpd).strip()}" class="relative"/>')
        
    for apd in absolute_path_defs:
        printf(f'<path d="{to_command_string(apd).strip()}" class="absolute"/>')
    printf('</xml>')

    