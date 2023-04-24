#!/usr/bin/env python

import re
from xml.etree import ElementTree
from dataclasses import dataclass, field
from typing import Optional

import base


__all__ = ('RepresentativeGraphElement', 'StringRepresentationGraph')


@dataclass
class RepresentativeGraphElementMask(base.RepresentativeGraphElementAbstract):

    ''' Sensetive turn off '''

    id: str = ''
    part: str = ''
    grouped: str = ''
    body: str = ''
    graph: Optional[base.StringRegularExpressionMaskAbstract] = None

    def __str__(self):
        return f'{self.part} id: {self.id} = {self.grouped} - {self.body}'

    def show_children(self, pretty=True):
        return '\n'.join((child for child in self.children))

    def show_parents(self, pretty=True):
        return '\n'.join((parent for parent in self.parents))

    def walk(self, left=True):
        first = element.children[0]
        last = element.children[-1]
        if left:
            yield first
        yield last


@dataclass
class StringByStringRegularExpressionMask(base.StringRegularExpressionMaskAbstract):

    element_mask: Optional[str] = r'.+(?P<id>\D+)\..?(?P<grouped>.+): (?P<body>.*)\n'
    node_mask: Optional[str] = r'(?P<id>\D+)\((?P<children_list>.*)\)'
    part_mask: Optional[str] = r'.*(?P<id>\S+\D+\).\n'
    tmp: Optional[str] = None
    separeter: Optional[str] = '\n'
    file: str = 'graph_links.txt'
    last_part: str = 'A1.'
    element_class = RepresentativeGraphElementMask

    def __iter__(self):
        return iter(self._get_formated_links())

    def __str__(self):
        return self.separeter.join(str(tmp) for tmp in iter(self))

    def _get_formated_links(self):        
        for link in self.tmp.split(self.separeter):
            if (tmp := link.strip()).endswith('.'):
                self.last_part = tmp
                continue
            yield from self._convert_element(tmp, self.last_part)

    def get_elements(self, part=None, id=None):
        if id and not part:
            raise Indexerror('Part has not defined when id was passed')
        elif id and part:
            for element in filter(el.starswith(part) for el in iter(self)):
                if element.id == id:
                    yield element
                continue
        raise Indexerror('Unknown id or part')

    def get_element(self, part=None, id=None) -> base.RepresentativeGraphElementAbstract:
        return self.get_elements(part, id)[0]


class XmlGraphElementMixin(ElementTree.Element):

    def getchildren(self, level=1):
        if self.attrib["color"] == 'red': d['red'] += level
        elif self.attrib['color'] == 'green': d['green'] += level
        else: d['blue'] += level
        level += 1
        for element in self: getchildren(element, level)

    def iterateDeep(self, right=True):
        index = -1 if right and (len(self) > 1) else 0
        yield self.attrib.get('color', 'nothing')
        if len(self):
            yield from iterateDeep(self[index], right=right)

    def iterateWide(self):

        def iterateFromLastChild(node):
            if len(node):
                for child in node:
                    yield from iterateWide(child)
            yield node.attrib.get('color', 'nothing')

        return iter([*reversed([*iterateFromLastChild(self)])])

def get_test_xml_data(file='./graph_example.xml'):
    try:
        with open(file, 'r') as xml:
            return xml
    except Exception as e:
        return input()


if __name__ == '__main__':
    xml_string = get_test_xml_data()

    root = ElementTree.fromstring(xml_string)
    root = RepresetativeGraphElement(root, root.attrib)

    root.getchildren()

    print(d['red'], d['green'], d['blue'])

    for color in root.iterateDeep():
        print(color)

    print()

    for color in root.iterateDeep(right=False):
        print(color)

    print()
    print()
    print()

    for color in root.iterateWide():
        print(color)