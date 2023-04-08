#!/usr/bin/env python

import re
from xml.etree import ElementTree
from dataclasses import dataclass


@dataclass
class StringRepresentationGraph:

    element_mask: str = r'(?P<id>\D+)\..?(?P<grouped>\S+): (?P<body>.*)\n'
    node_mask: str = r'(?P<id>\D+)\((?P<children_list>.*)\)'
    part_mask: str = r'.*(?P<id>\S+\D+\).\n'
    tmp: str = ''

    def to_pythonic(self):
        return [links for links in self._get_formated_links()]

    def __str__(self):
        return self.tmp

    def _get_formated_links(self):
        parts = iter(self._parts())
        for link in self._links():
            if int(link.group("id")) == 1:
                part = next(parts)
            yield {
                f'{part.group("id")} - {link.group("id")} - {link.group("grouped")} ':
                self._link_children(link.group('body'))}

    def _parts(self):
        for part in re.findall(self.part_mask, self.tmp):
            yield part

    def _links(self):
         for link in re.findall(self.element_mask, self.tmp):
             yield link

    def _link_children(self, link: str):
        for child in re.findall(self.node_mask, link):
            return {child.group('id'): child.group('children_list')}


class RepresetativeGraphElement(ElementTree.Element):

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
