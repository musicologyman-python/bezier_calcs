import abc
import inspect
import io
import json
import typing

from dataclasses import dataclass, field
from functools import partial
from itertools import chain, pairwise

import lxml.etree as etree
import pyperclip
import regex

from IPython.core.display import HTML
from more_itertools import chunked
from sympy import *
from toolz import curried
from toolz.functoolz import compose_left, curry, pipe

NSMAP = { None: 'http://www.w3.org/2000/svg', 
         'xlink': 'http://www.w3.org/1999/xlink' }

COMMAND_RE = regex.compile(r'''(?ix)(?P<command>[clmsvz])
                               (\s+(?P<arg>-?\d+(\.d+)?))*''')

@dataclass
class Point():
    x: float
    y: float
    
    def to_matrix(self):
        return Matrix([ self.x, self.y ])
    
    def __add__(self, other):
        match other:
            case Point():
                return Point(self.x + other.x, self.y + other.y)
            case _:
                raise TypeError
                
    def __sub__(self, other):
        match other:
            case Point():
                return Point(self.x - other.x, self.y - other.y)
            case _:
                raise TypeError
                
    def __str__(self):
        return f'{self.x}, {self.y}'


@dataclass(frozen=True)
class MoveTo():
    p: Point
    
    def __str__(self):
        return f'M {self.p}'


@dataclass(frozen=True)
class AbstractCubicBezier(abc.ABC):
    p0: Point
    p1: Point
    p2: Point
    p3: Point
 
    @property
    def points(self):
        return [self.p0, self.p1, self.p2, self.p3]


@dataclass(frozen=True)
class CubicBezierAbs(AbstractCubicBezier):
    
    def to_rel(self):
        return CubicBezierRel(MoveTo(self.p0), 
                              self.p1 - self.p0, 
                              self.p2 - self.p0, 
                              self.p3 - self.p0)
    
    def __str__(self):
        return f'C {self.p1} {self.p2} {self.p3}'


@dataclass(frozen=True, init=False)
class CubicBezierRel(AbstractCubicBezier):
    
    def __init__(self, move_to, p1, p2, p3):
        match move_to:
            case Point() as p:
                super().__init__(p, p1, p2, p3)
            case MoveTo():
                super().__init__(move_to.p, p1, p2, p3)
            case CubicBezierAbs() as b:
                super().__init__(b.p3, p1, p2, p3)
        
    def to_abs(self):
        return CubicBezierAbs(self.p0, 
                              self.p1 + self.p0, 
                              self.p2 + self.p0, 
                              self.p3 + self.p0)
        
    def __str__(self):
        return f'c {self.p1} {self.p2} {self.p3}'


@dataclass(frozen=True)
class ShorthandCubicBezierRel(CubicBezierRel):
    
    def __init__(self, previous_bezier, p2, p3):
        super().__init__(previous_bezier.p3,
                              previous_bezier.p3 - previous_bezier.p2,
                              p2,
                              p3)
    
    def __str__(self):
        return f's {self.p2} {self.p3}'


class ClosePath():
    
    def __str__(self):
        return 'z'
    
    def __repr__(self):
        return f'{self.__class__.__name__}()'


class CoordinatePair(typing.NamedTuple):
    x: int
    y: int
    
    def __str__(self):
        return f'x = {self.x:>4}, y = {self.y:>4}'
    
    def __add__(self, other):
        return CoordinatePair(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return CoordinatePair(self.x - other.x, self.y - other.y)


class SimpleCommand():
    
    def __init__(self, command, coordinates: list[CoordinatePair]):
        
        match command:
            case list() as l:
                self.command = l[0]
            case _:
                self.command = command
                
        self.coordinates = coordinates
    
    def __str__(self):
        with io.StringIO() as sp:
            prints = partial(print, file=sp)
            prints(self.command, end='     ')
            if self.coordinates:
                for coordinate in self.coordinates:
                    prints(coordinate)
                    prints('      ', end='')
            return sp.getvalue()
        
    def __repr__(self):
        with io.StringIO() as sp:
            prints = partial(print, end='', file=sp)
            prints(f'{self.__class__.__name__}(command="{self.command}", ')
            prints('coordinates=[')
            coordinates_str = ', '.join([f'{pair!r}' for pair 
                                         in self.coordinates])
            prints(f'{coordinates_str}]')
            return sp.getvalue()


def get_element_string(e):
    return etree.tostring(e, pretty_print=True).decode('utf-8')

print_element = compose_left(get_element_string, print)

def parse_path_def(path_def):
    for m in COMMAND_RE.finditer(path_def):
        d = m.capturesdict()
        command = d['command'][0]
        args = d['arg']
        if args:
            yield {'command': command,
                    'args': pipe(args, 
                                 curried.map(float),
                                 lambda seq: chunked(seq, 2),
                                 curried.map(tuple),
                                 list)}
        else:
            yield {'command': command}

def print_path_attribute(e, leader=' '*4, level=1):
    with io.StringIO() as sp:
        prints = curry(print, file=sp)
        prints(f'{leader}<path', end=' ')
        if 'transform' in e.attrib:
            prints(f'transform=', end='')
            prints(f'"{transform}"')
            prints(f'{leader * (level + 1)}d="', end='')
        return sp.getvalue()

def read_templates(filename='./svg/notes_only_formatted.svg'):
    root = etree.parse(filename).getroot()
    return root.findall('.//defs/g', NSMAP)

def print_templates(templates):   
    for template in templates:
        print_element(template)

def get_path_def(template):
    return template.find('path', NSMAP).attrib['d']

def get_commands_from_templates(templates):
    path_def = templates[0].find('path', NSMAP).attrib['d']
    return parse_path_def(path_def)

get_path_defs = compose_left(read_templates, curried.map(get_path_def), list)

get_commands = compose_left(read_templates, get_commands_from_templates, list)

bernstein_polynomial = sympify('binomial(n, k) * t**k * (1 - t)**(n - k)')

cubic_bernstein_polynomial = bernstein_polynomial.subs({'n': 3})

def get_cubic_bernstein_polynomial(k):
    return cubic_bernstein_polynomial.subs({'k': k})

def get_points(p0, control_points):
    yield p0
    for p in control_points:
        yield p0 + p

def get_points(p0, control_points):
    yield p0
    for p in control_points:
        yield p0 + p

def make_typed_commands(command_dicts):
    previous_command = None
    for d in command_dicts:
        match d['command']:
            case 'M':
                move_to = MoveTo(d['args'][0])
                previous_command = move_to
                yield move_to
            case 'c':
                rel_bezier = CubicBezierRel(previous_command, *d['args'])
                abs_bezier = rel_bezier.to_abs()
                previous_command = abs_bezier
                yield abs_bezier
            case 's':
                rel_bezier = ShorthandCubicBezierRel(previous_command, *d['args'])
                abs_bezier = rel_bezier.to_abs()
                yield abs_bezier
            case 'z':
                previous_command = None
                yield ClosePath()

def parse_attr_dict(attr_dict):
    with io.StringIO() as sp:
        for key, value in attr_dict.items():
            print(f' {key}="{value}"', end='', file=sp)
        return sp.getvalue()

def line(x1, y1, x2, y2, attr={}):
    
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" ' \
           f'y2="{y2}"{parse_attr_dict(attr)}/>'

def horizontal_line(x1, x2, y, attr={}):
    return line(x1, y, x2, y, attr=attr)

def vertical_line(x, y1, y2, attr={}):
    return line(x, y1, x, y2, attr=attr)

def get_grid_lines(min_x, min_y, max_x, max_y, incr, start_offset=-25):
    for y in range(min_x, max_x+incr, incr):
        yield horizontal_line(min_x+start_offset, max_x, y)
    for x in range(min_y, max_y+incr, incr):
        yield vertical_line(x, min_y+start_offset, max_y)

def get_axes(min_x, min_y, max_x, max_y):
    attr = {'class': 'axis'}
    if min_x <= 0 and max_x >= 0:
        yield horizontal_line(min_x, max_x, 0, attr)
    if min_y <= 0 and max_y >= 0:
        yield vertical_line(0, min_y, max_y, attr)

def svg(content, viewbox='"0 0 700 600"'):
    return f'''<svg viewbox={viewbox}>
               <g transform="translate(25, 25)">
               <rect width="700" height="600" class="bounding-rectangle" 
                stroke="#000" stroke-width="1" fill="#fff"/>
                {content}</g></svg>'''

def reformat_path_def(path_def, leader_size=30):
    leader = ' ' * leader_size
    return '\n'.join(f'{leader}{m[0]}' for m in RAW_CMD_RE.finditer(path_def))

def parse_coordinates(coordinate_str):
    if not s:
        return
    return CoordinatePair(*(int(s) for s in coordinate_str.split()))

def parse_command(capturesdict):
    return SimpleCommand(command=capturesdict['command'][0], 
                         coordinates=[parse_coordinates(c) for c 
                                      in capturesdict['coordinates']])

def get_simple_commands(s):
    for m in CMD_WITH_PAIRED_ARGS_RE.finditer(s):
        d = m.capturesdict()
        parsed_command = parse_command(d)
        yield parsed_command

def get_abs_cubic_beziers(commands):
    for cmd in commands:
        match cmd.command:
            case 'M':
                start_point = cmd.coordinates[0]
            case 'c':
                control_points = \
                    [start_point] + \
                    [start_point + coordinate for coordinate in cmd.coordinates]
                start_point = control_points[-1]
                previous_bezier = control_points
                yield control_points
            case 's':
                control_points = [start_point] \
                               + [(previous_bezier[2] - start_point)] \
                               + [start_point + coordinate 
                                  for coordinate in cmd.coordinates]
                start_point = control_points[-1]
                previous_bezier = control_points
                yield control_points
            case 'z':
                start_point = []
                previous_bezier = []

def get_paths_from_control_points(control_points):
    s = f'M {control_points} C '
    for cp in control_points[1:4]:
        s += f'{cp} '
    return s

def get_members(t):
    for m, n in inspect.getmembers(t):
        print(m)
        match n:
            case list() as l:
                for p in l:
                    print(f'     {p}')
            case dict() as d:
                for k, v in d.items():
                    print(f'     {k}: {v}')
            case _:
                print(f'     {n}')

