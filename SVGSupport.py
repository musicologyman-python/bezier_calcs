import abc
from typing import NamedTuple
import regex
from more_itertools import chunked

COMMAND_RE = regex.compile(r'(?P<command>[Mc])\s*((?P<args>-?\d+)\s*)+')

class Point(NamedTuple):
    x: float
    y: float

    def __add__(self, other):
        match other:
            case Point():
                return Point(self.x + other.x, self.y + other.y)
            case _:
                raise TypeError()
    
    def __str__(self):
        return f'{self.x} {self.y}'

    
class MoveToAbs(NamedTuple):
    p: Point

    def __str__(self):
        return f'M {self.p}'


class CubicBezierRel(NamedTuple):
    p1: Point
    p2: Point
    p3: Point

    def __str__(self):
        return f'c {self.p1} {self.p2} {self.p3}'


class CubicBezierAbs(NamedTuple):
    p1: Point
    p2: Point
    p3: Point

    def __str__(self):
        return f'C {self.p1} {self.p2} {self.p3}'


def cubic_bezier_abs_to_rel(point, abs_cubic_bezier):
    return CubicBezierRel(
        abs_cubic_bezier.p1 - point,
        abs_cubic_bezier.p2 - point,
        abs_cubic_bezier.p3 - point)

def cubic_bezier_rel_to_abs(point, rel_cubic_bezier):
    return CubicBezierAbs(
        rel_cubic_bezier.p1 + point,
        rel_cubic_bezier.p2 + point,
        rel_cubic_bezier.p3 + point)

def get_move_to_abs(args):
    return MoveToAbs(Point(*args))

def get_cubic_bezier_rel(args):
    points = [Point(*chunk) for chunk in chunked(args, 2)]
    return CubicBezierRel(*points)

def get_command(captures: dict):
    command = captures['command'][0]
    args = [int(arg) for arg in captures['args']]
    match command:
        case 'M':
            yield get_move_to_abs(args)
        case 'c':
            yield get_cubic_bezier_rel(args)

def commands_from_string(s):
    for m in COMMAND_RE.finditer(s):
        if m:
            yield (get_command(m.capturesdict()))



