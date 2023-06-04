import sys

from toolz.functoolz import compose_left, curry, pipe
from lxml import etree

def get_xml_root(filename="./svg/notes_only_formatted.svg"):
    tree = etree.parse(filename)
    return tree.getroot()

def build_xml_getter(root):
    NSMAP = root.nsmap
    def xml_getter(element, xpath: str):
        return element.findall(xpath, NSMAP)
    return xml_getter

find_all = build_xml_getter(get_xml_root())

def get_note_defs():
    root = get_xml_root()
    return (e for e in find_all(root, './/defs/g') 
            if e.attrib['id'].startswith('note'))

def get_element_string(element):
    etree.tostring(element, pretty_print=True)
    
print_element = compose_left(get_element_string, 
                             curry(print, file=sys.stdout))

def main():
    
    note_defs = get_note_defs()
    for note_def in note_defs:
        print_element(note_def)

if __name__ == '__main__':
    main()