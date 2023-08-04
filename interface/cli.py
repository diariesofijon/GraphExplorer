#!/usr/bin/env python
# pylint: disable=C0103,C0114

import sys

import data_structures
import base

def walk(graph: base.GM):
    ''' Walking down through the graph'''
    for element in graph.tree_topic.walk(graph.exlude_tree().longest_chain):
        print(f'current element {next_element} with index {index}')
        print('type 1 - to get next left, \
                2 - to get previous left,\
                3 - to get next right,    \
                4 - to get previous right,\
                5 - to get out of walking')
        index_type = int(input())
        if index_type == 5:
            print('Have a nice day!')
            sys.exit(0)
        print(element.show_children())
        next_element = take_choice(element, index_type)
    print('chain is ended')

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
        next_element = element.parents[index]
    return next_element

def show_pretty_graph(graph: base.GM, index: int =1):
    ''' Pretty printing of all graph '''
    print('\n\n\n')
    print(index)
    # starting walking from the first element
    walk(graph)
