#!/usr/bin/env python

import re
from xml.etree import ElementTree
from dataclasses import dataclass

@dataclass
class RepresentativeGraphElement:
    
    id: str = ''
    part: str = ''
    grouped: str = ''
    body: str = ''
    
    def __str__(self):
        return f'{self.part} id: {self.id} = {self.grouped} - {self.body}'


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

    def _get_formated_links(self):
        last_part = 'A1.'
        
        for link in self.tmp.split('\n'):
            if (tmp := link.strip()).endswith('.'):
                last_part = tmp
                continue
            yield from self._convert_string(tmp, last_part)

    @staticmethod
    def _link_children(body: str):
        return body
        result = []
        for child in body.split(','):
            try:
                part = child.split('(')[0]
                links = child.split('(')[1].strip(')')
            except IndexError as ie:
                result = body
                break
            result.append({'part': part, 'links': links})
        return result
    
    @staticmethod
    def _get_ids(name):
            if len(tmp := name.split('-')) == 2:
                return list(range(int(tmp[0]), int(tmp[1])+1))
            return [int(name)]
    
    @staticmethod
    def _convert_string(tmp, last_part):
        ids, tmp = tmp.split('.')
        for id in StringRepresentationGraph._get_ids(ids):
            grouped, body = tmp.split(':')
            data = RepresentativeGraphElement(
                id=id, grouped=grouped, part=last_part,
                body=StringRepresentationGraph._link_children(body))
            yield data


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
