import inspect

from operator import itemgetter

import regex

import more_bezier_calcs as mbc

FUNCTION_NAME_RE = regex.compile('(?<=def\s+)\w+(?=\()')

def get_function_name(line):
    match FUNCTION_NAME_RE.search(line):
        case regex.Match() as m:
            return m[0]

CLASS_NAME_RE = regex.compile(r'(?<=class\s+)\w+(?=\()')

def get_class_name(line):
    match CLASS_NAME_RE.search(line):
        case regex.Match() as m:
            return m[0]

with open('more_bezier_calcs.py') as fp:
    lines = [s.rstrip() for s in fp]
    
function_lines = [(i, line) for i, line in enumerate(lines) 
                  if line.startswith('def')]

function_names = [(i, get_function_name(line)) for i, line in function_lines]

class_lines = [(i, line) for i, line in enumerate(lines) 
               if line.startswith('class')]

class_names = [(i, get_class_name(line)) for i, line in class_lines]

import_statements = [(i, line) for i, line in enumerate(lines) 
                     if regex.search('import', line)]

import_statements.sort(key=itemgetter(1))

import more_bezier_calcs

class_sources = [inspect.getsource(eval(f'more_bezier_calcs.{class_name}'))
                 for _, class_name in class_names]

function_sources = [inspect.getsource(eval(f'more_bezier_calcs.{function_name}'))
             for _, function_name in function_names]

with open('explore_more_bezier_calcs_py.py', mode='w') as fp:

    for _, stmt in import_statements:
        print(stmt, file=fp)

    print(file=fp)

    for source in class_sources:
        print(source, file=fp)
        print(file=fp)

    for source in function_sources:
        print(source, file=fp)
