from pprint import pprint
from lxml import etree

# with open('absolute_curves.xml', encoding='utf-8') as fp:
#     lines = [line.strip() for line in fp]

# relative_paths = lines[:82]
# absolute_paths = lines[84:]

docroot = etree.parse('absolute_curves.xml').getroot()
relative_paths = [etree.tostring(path).decode('utf-8') 
                  for path in docroot.findall('.//path[@class="relative"]')]
absolute_paths = [etree.tostring(path).decode('utf-8') 
                  for path in docroot.findall('.//path[@class="absolute"]')]

def get_paths(paths):
    split_indexes = [i for i, p in enumerate(paths) if p=='']
    previous_index = 0
    for idx in split_indexes:
        yield ' '.join(paths[slice(previous_index, idx)])
        previous_index = idx + 1

    yield ' '.join(paths[slice(previous_index, None)])

with open('extrema.txt', encoding='utf-8') as fp:
    lines = [line.strip() for line in fp]

import json

extrema = [json.loads(line) for line in lines]

all_paths = list(zip(get_paths(relative_paths), get_paths(absolute_paths), extrema))

pprint(all_paths)

import string

svg_template = string.Template('''<html>
    <head>
        <title>SVG Template</title>
        <style>
            path.relative {fill: none; stroke: blue;}
            path.absolute {fill: none; stroke: black;}
        </style>
    </head>
    <body>
        <svg width="1500" height="700">
            <g transform="$left_transform">
            $left_content
            </g>
            <g transform="$right_transform">
            $right_content
            </g>
        </svg>
    </body>
</html>''')

def get_min_coordinate(min_val):
    if min_val > 0:
        return min_val // 100 
    else:
        return -(abs(min_val) // 100 + 100)

def get_max_coordinate(max_val):
    if max_val > 0:
        return max_val // 100 + 100
    else:
        return -(abs(max_val) // 100)



for i, (relpaths, abspaths, extrema) in enumerate(all_paths, start=1):
    #calculate transform attribute
    min_x = get_min_coordinate(extrema['min_x'])
    max_x = get_max_coordinate(extrema['max_x'])
    min_y = get_min_coordinate(extrema['min_y'])
    max_y = get_max_coordinate(extrema['max_y'])

    x_translation = abs(min_x) + 50
    y_translation = abs(min_y) + 50

    x_extent = x_translation + max_x + 25

#    left_transform = f"translate({x_translation}, {y_translation})"

#    right_transform = f"translate({x_extent}, {y_translation})"

    left_transform = 'translate(25, 25)'
    right_transform = 'translate(650, 25)'

    doc_content = svg_template.substitute({'left_transform': left_transform,
                                          'left_content': relpaths,
                                          'right_transform': right_transform,
                                          'right_content': abspaths})

    with open(f'template_{i:02}.html', mode='w') as fp:
        fp.write(doc_content)

    



