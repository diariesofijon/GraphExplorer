#!/usr/bin/env python
# pylint: disable=C0103,C0114

import sys

import graph_engine
import base


def walk(graph: base.GM, index: int =0):
    ''' Walking down through the graph'''
    next_element = graph[index]
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

def take_choice(element: base.GE, index: int):
    ''' Returns next element '''
    if index not in {1, 2, 3, 4}:
        raise ValueError('Index ' + str(index) + ' is out of range')
    next_element = None
    if index in {1, 3}:
        index = 0 if index == 1 else -1
        next_element = element.children[index]
    else:
        index = 0 if index == 2 else -1
        next_element = element.parent[index]
    return next_element

def show_pretty_graph(graph: base.GM, index: int =1):
    ''' Pretty printing of all graph '''
    print('\n\n\n')
    print(index)
    # starting walking from the first element
    walk(graph)

def main():
    ''' Converting list of links to a graph '''

    # TODO: make clear console interface
    srg = graph_engine.StringByStringRegularExpressionMask()

    with open('output.txt', 'w', encoding='utf8') as file:
        file.write(str(srg))

    show_pretty_graph(srg, 3)

if __name__ == '__main__':
    print('input the graph')
    print('\n\n\n')
    main()
