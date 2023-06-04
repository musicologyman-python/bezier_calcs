# coding: utf-8
from pathlib import Path
lines = Path('svg/notes_only_formatted.svg').read_text().split_lines()
lines = Path('svg/notes_only_formatted.svg').read_text().splitlines()
lines
def list_lines(lines, from=0, to=-1):
    for i, line in enumerate(lines[slice(from, to)]):
        print(f'{i:>4} {line}')
def list_lines(lines, start_line=0, end_line=-1):
    for i, line in enumerate(lines[slice(start_line, end_line)]):
        print(f'{i:>4} {line}')
        
get_ipython().run_line_magic('whos', '')
list_lines(lines)
lines[-1]
lines[slice(70, None)]
def list_lines(lines, start_line=0, end_line=None):
    for i, line in enumerate(lines[slice(start_line, end_line)]):
        print(f'{i:>4} {line}')
        
list_lines(lines)
list_lines(lines, 49, 51)
def list_lines(lines, start_line=0, end_line=None):
    for i, line in enumerate(lines[slice(start_line, end_line)], start=start_line):
        print(f'{i:>4} {line}')
        
list_lines(lines, 49, 51)
import enum
def get_path_elements(lines: list[str]):
    line: str
    PathState = enum.Enum('State', 'NOT_IN_PATH', 'IN_PATH')
    state = PathState.NOT_IN_PATH
    for i, line in enumerate(lines):
        match state:
            case NOT_IN_PATH:
                path_element_start_index = line.index('<path')
                if path_start_element_index > -1:
                    state = PathState.IN_PATH 
