#!/usr/bin/env python

from xml.etree import ElementTree

d = {'red': 0, 'green': 0, 'blue': 0}

def getchildren(root, level=1):
    if root.attrib["color"] == 'red': d['red'] += level
    elif root.attrib['color'] == 'green': d['green'] += level
    else: d['blue'] += level
    level += 1
    for element in root: getchildren(element, level)

def iterateDeep(node, right=True):
    index = -1 if right and (len(node) > 1) else 0
    yield node.attrib.get('color', 'nothing')
    if len(node):
        yield from iterateDeep(node[index], right=right)

def iterateWide(tree):

    def iterateFromLastChild(node):
        if len(node):
            for child in node:
                yield from iterateWide(child)
        yield node.attrib.get('color', 'nothing')

    return iter([*reversed([*iterateFromLastChild(tree)])])


xml_string = input()

root = ElementTree.fromstring(xml_string)

getchildren(root)

print(d['red'], d['green'], d['blue'])

for color in iterateDeep(root):
    print(color)

print()

for color in iterateDeep(root, right=False):
    print(color)

print()
print()
print()

for color in iterateWide(root):
    print(color)
