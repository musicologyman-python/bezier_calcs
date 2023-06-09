from functools import partial
from io import StringIO
from lxml import etree
import regex

def format_element(e, level=0, indent=2, indentchar=' '):
    leader = level * indent * indentchar
    tag_name = regex.sub(r'{.*}', '', e.tag)
    with StringIO() as fp:
        first_line = f'{leader}<{tag_name}'
        fp.write(first_line)
        if e.attrib:
            fp.write(' ')
            attributes = list(e.attrib.items())
            fp.write('{0}="{1}"'.format(*attributes[0]))    
            match len(attributes):
                case 1:
                    fp.write('>\n')
                case 2:
                for key, value in attributes[1:]
        

        


def main():
    docroot = etree.parse('svg/notes_only.svg').getroot()
    nsmap = docroot.nsmap
    g = docroot.findall('g', nsmap)



if __name__ == '__main__':
    main()
