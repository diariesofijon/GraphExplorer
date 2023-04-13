#!/usr/bin/env python

import re
from xml.etree import ElementTree
from dataclasses import dataclass
from typing import Optional


__all__ = ('RepresentativeGraphElement', 'StringRepresentationGraph')



@dataclass
class StringRepresentationGraph:

    element_mask: str = r'.+(?P<id>\D+)\..?(?P<grouped>.+): (?P<body>.*)\n'
    node_mask: str = r'(?P<id>\D+)\((?P<children_list>.*)\)'
    part_mask: str = r'.*(?P<id>\S+\D+\).\n'
    tmp: str = ''
    separeter: str = '\n'

    def __iter__(self):
        return iter(self._get_formated_links())

    def __str__(self):
        return self.separeter.join(str(tmp) for tmp in iter(self))
        
    def get_elements(self, part=None, id=None):
        if id and not part:
            raise Indexerror('Part has not defined when id was passed')
        elif id and part:
            for element in filter(el.starswith(part) for el in iter(self)):
                if element.id == id:
                    yield element
                continue
        raise Indexerror('Unknown id or part')
        
    def get_element(self, part=None, id=None) -> RepresentativeGraphElement:
        return self.get_elements(part, id)[0]

    def _get_formated_links(self):
        last_part = 'A1.'
        
        for link in self.tmp.split('\n'):
            if (tmp := link.strip()).endswith('.'):
                last_part = tmp
                continue
            yield from self._convert_element(tmp, last_part)
    
    @staticmethod
    def _get_ids(name):
            if len(tmp := name.split('-')) == 2:
                return list(range(int(tmp[0]), int(tmp[1])+1))
            return [int(name)]

    @staticmethod
    def _convert_element(tmp, last_part):
        ids, tmp = tmp.split('.')
        for id in StringRepresentationGraph._get_ids(ids):
            grouped, body = tmp.split(':')
            data = RepresentativeGraphElement(
                id=id, grouped=grouped, part=last_part, body=body)
            yield data


@dataclass
class RepresentativeGraphElement:
    
    id: str = ''
    part: str = ''
    grouped: str = ''
    body: str = ''
    graph: Optional[StringRepresentationGraph] = None
    
    def __str__(self):
        return f'{self.part} id: {self.id} = {self.grouped} - {self.body}'
    
    def children(self):
        if self.graph:
            return list(*self.graph.get_elements(
                part=self.part, id=self.id))
        return []
        
    
    @classmethod
    def load(cls, file=None, string=None, part=None, id=None):
        if file:
            with open(file, 'r') as file:
                return StringRepresentationGraph(tmp=file).get_element(part, id)
        elif string:
            return StringRepresentationGraph(tmp=string).get_element(part, id)
        else:
            raise Indexerror('Unexpected behavior')


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
