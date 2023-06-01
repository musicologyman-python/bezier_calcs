#%%

# pyright: reportMissingModuleSource=false

from typing import NamedTuple, Union
import regex
from more_itertools import chunked

#%%
_COMMAND_RE = regex.compile(r'(?P<command>[Mc])\s*((?P<args>-?\d+)\s*)+')

class Point(NamedTuple):
    """An ordered pair representing a point in an svg image."""
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
    """Represents the absolute moveto command (\"M\") in an SVG path."""
    p: Point

    def __str__(self):
        """Returns the representation of a MoveToAbs object as it appears in
        an SVG path element.
        """
        return f'M {self.p}'


class CubicBezierRel(NamedTuple):
    p1: Point
    p2: Point
    p3: Point
    
    def to_absolute(self, move_to: Union[Point,MoveToAbs]):
        match move_to:
            case MoveToAbs():
                p0 = move_to
            case Point():
                p0 = move_to
        
        return CubicBezierAbs( self.p1 + p0, self.p2 + p0, self.p3 + p0)
    
    def __str__(self):
        return f'c {self.p1} {self.p2} {self.p3}'


class CubicBezierAbs(NamedTuple):
    p1: Point
    p2: Point
    p3: Point

    def to_relative(self, move_to: Union[Point, MoveToAbs]):
        match move_to:
            case MoveToAbs():
                p0 = move_to
            case Point():
                p0 = move_to
        
        return CubicBezierRel(self.p1 - p0, self.p2 - p0, self.p3 - p0)    
    
    def __str__(self):
        return f'C {self.p1} {self.p2} {self.p3}'


def cubic_bezier_abs_to_rel(point: Point, 
                            abs_cubic_bezier: CubicBezierAbs):
    return CubicBezierRel(
        abs_cubic_bezier.p1 - point,
        abs_cubic_bezier.p2 - point,
        abs_cubic_bezier.p3 - point)

def cubic_bezier_rel_to_abs(point: Point, 
                            rel_cubic_bezier: CubicBezierRel):
    return CubicBezierAbs(
        rel_cubic_bezier.p1 + point,
        rel_cubic_bezier.p2 + point,
        rel_cubic_bezier.p3 + point)

def get_move_to_abs(args: list[float]):
    return MoveToAbs(Point(*args))

def get_cubic_bezier_rel(args: list[float]):
    points = [Point(*chunk) for chunk in chunked(args, 2)]
    return CubicBezierRel(*points)

def parse_path_command(captures: dict):
    """ From a dictionary (typically resulting from a call to the 
    regex.Match.capturesdict()), return the corresponding objects
    representing the path.
    """
    command = captures['command'][0]
    args: list[float] = [float(arg) for arg in captures['args']]
    match command:
        case 'M':
            yield get_move_to_abs(args)
        case 'c':
            yield get_cubic_bezier_rel(args)

def commands_from_string(s: str):
    """ Parses a string representing an SVG path and returns a generator
    containing the python objects for each command in the path statement 
    """
    for m in _COMMAND_RE.finditer(s):
        if m:
            yield (parse_path_command(m.capturesdict()))



