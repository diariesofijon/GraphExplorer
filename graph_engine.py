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
        return self._get_formated_links(as_string=True)

    def __str__(self):
        return self.separeter.join(iter(self))

    #def _get_formated_links(self):
    #    print('STARTING FORMATING')
    #    parts = iter(self._parts())
    #    for index, link in enumerate(self._links()):
    #        print('THIS LINK IS', index)
    #        if int(link.get("id")) == 1:
    #            print('NEW PART AT THEN', index, 'index')
    #            part = next(parts)
    #        yield {
    #            f'{part.get("id")} - {link.get("id")} - {link.get("grouped")} ':
    #            self._link_children(link.get('body'))}

    #def _parts(self):
    #    for part in re.findall(self.part_mask, self.tmp):
    #        yield part

    def _get_formated_links(self, as_string=False):
        print('STARTING FOR CYCLE FOR LINKS')
        from pprint import pprint
        #pprint(re.findall(self.element_mask, self.tmp))
        #for link in re.findall(self.element_mask, self.tmp):
        #    yield link
        last_part = 'A1.'
        for link in self.tmp.split('\n'):
            tmp = link.strip()
            if tmp.endswith('.'):
                last_part = tmp
                continue
            tmp = tmp.split('.')
            id = tmp[0]
            tmp = tmp[1].split(':')
            grouped = tmp[0]
            body = tmp[1] if (len(tmp) - 1) else ''
            data = RepresentativeGraphElement(
                id=id, grouped=grouped, part=last_part,
                body=self._link_children(body))
            if as_string:
                data = str(data)
            yield data

    def _link_children(self, body: str):
        #for child in re.findall(self.node_mask, link):
        #    return {child.group('id'): child.group('children_list')}
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
