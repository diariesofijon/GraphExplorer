#!/usr/bin/env python
# pylint: disable=C0103

import sys
from pprint import pprint
from typing import Optional

import graph_engine


def walk(
        graph: graph_engine.StringByStringRegularExpressionMask, 
        index: Optional[int]=None):
    index_from = int(index) if index else 1
    next_element = graph[index_from]
    for element in next_element.walk():
        print('type 1 - to get next left, \
                2 - to get previous right,\
                3 - to get next right,    \
                4 - to get previous right,\
                5 - to get out of walking')
        index_type = int(input())
        if index_type == 5:
            print('Have a nice day!')
            sys.exit(0)
        print(element.show_children())
        next_element = take_choice(element, index_type)

def take_choice(
        element: graph_engine.RepresentativeGraphElementMask, index: int):
    if index not in (1,2,3,4):
        raise ValueError('Index ' + str(index) + ' is out of range')
    next_element = None
    if index == 1 or index == 3:
        index = 0 if index == 1 else -1
        next_element = element.children[index]
    else:
        index = 0 if index == 2 else -1
        next_element = element.parent[index]
    return next_element

def show_pretty_graph(
        graph: graph_engine.StringByStringRegularExpressionMask, 
        index: Optional[int]=None):
    index = int(index) if index else 1
    print('\n\n\n')
    print(index)
    # starting walking from the first element
    walk(graph, index)

def main():
    ''' Converting list of links to a graph '''
    index = None
    if len(sys.argv) and sys.argv[0] == '-from_console':
        index = 1
        srg = graph_engine.StringByStringRegularExpressionMask(tmp=input())
    elif (len(sys.argv)-1) and (file := sys.argv[1]) and sys.argv[1].endswith('.txt'):
        index = 2
        srg = graph_engine.StringByStringRegularExpressionMask(file=file)
    else:
        index = 3
        srg = graph_engine.StringByStringRegularExpressionMask()

    with open('output.txt', 'w') as file:
        print(srg.tmp)
        file.write(str(srg))

    show_pretty_graph(srg)

if __name__ == '__main__':
    print('input the graph')
    print('\n\n\n')
    main()
