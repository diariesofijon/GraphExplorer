#!/usr/bin/env python

'''
    There are pull of scripts contains representation of any varitant of
data visualisation wich can be affordably used in any useful place in the code.
'''

import sys
import os

from contextlib import ContextDecorator, AbstractContextManager

from bin import protocols as p
import lib

# TODO: declare protocol to exclude useful info from origin source data
# TODO: RegExp Conception future planning

class pretty_print_element(AbstractContextManager):

    def __init__(self,
        element:p.AbstractElement, prefix:str='', sufix:str='', postfix=''):
        self.element = element
        self.prefix, self.postfix, self.sufix = prefix, postfix, sufix

    def take_choice(self, index: int):
        ''' Returns next element '''
        if index not in {1, 2, 3, 4}:
            raise ValueError('Index ' + str(index) + ' is out of range')
        if index in {1, 3}:
            index = 0 if index == 1 else -1
            return self.element.children[index]
        index = 0 if index == 2 else -1
        return self.element.parents[index]

    @property
    def next_element(self):
        if (index:= int(input('chose id: '))) == 5:
            print('Have a nice day!')
            sys.exit(0)
        return self.take_choice(index)

    def __enter__(self):
        if self.prefix:
            print(self.prefix)
        print(f'current element {self.element} with index {self.element.id}')
        print('type 1 - to get next left, \
                2 - to get previous left,\
                3 - to get next right,    \
                4 - to get previous right,\
                5 - to get out of walking')
        if self.postfix:
            print(self.postfix)
        return self.next_element

    def __exit__(self, exc_type, exc, exc_tb):
        # TODO: add logging system
        if self.sufix:
            print(self.sufix)
        if isinstance(exc, ValueError):
            print('You have to reimage data you typed into the input boxes!')
        return False

class BaseGraphWalkingInterface():

    vertexes = {}
    _tree = None

    def __init__(self, graph: lib.typing.GM):
        self.graph = graph

    @property
    def tree(self):
        if self._tree:
            return self._tree
        return self.graph.exclude_tree(story=self.graph.vertexes)

    def defined_maximum_vertex_chain_index(self, maximum=5):
        self.graph.defined_maximum_vertex: int = maximum
        for vertex_info in self.graph.find_the_rigth_tree_by_vertex_size():
            self.vertexes[vertex_info[0]] = {
                'size': vertex_info[0],
                'left': vertex_info[2],
                'right': vertex_info[3]}
            yield vertex_info[1], self.vertexes[vertex_info[1]]
