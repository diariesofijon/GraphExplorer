#!/usr/bin/env python
#pylint: disable=C0103,C0114

'''
    TODO: make DFS step by step
        1. function as bound method for the graph which fitler them by tree belonging
        2. function as bound method for the graph which filter them by tree absent
        3. function that sort elements of the graph by the matrix' s part belonging
        4. matrix data
        5. visualistaion
'''

import sys
import abc
from dataclasses import dataclass
from typing import Optional

from data_structures import StringByStringRegularExpressionMask
from base import GM, GE


# TODO: make cool architecture console interface
class AbstractGraphWalkingInterface(abc.ABC):
    pass


@dataclass
class CliGraphWalking(AbstractGraphWalkingInterface):

    graph: Optional[GM] = None
    repr_type: type = int
    file_path: str = 'output.txt'
    # TODO: make clear console interface


    def choice(self, element: GE, index: int):
        ''' Returns next element '''
        if index in {1, 3}:
            index = 0 if index == 1 else -1
            return element.children[index]
        if index in {2, 4}:
            index = 0 if index == 2 else -1
            return element.parents[index]
        raise ValueError(f'Index {str(index)} is out of range')

    def walk(self):
        ''' Walking down through the graph'''
        print('\n\n\n')
        if (index := self.repr_type(input())) not in {1,2,3,4}:
            raise TypeError(ValueError(f'Index {str(index)} have invalid type'))
        # print('CHAIN', graph.exclude_tree().longest_chain)
        def iterate(el=self.graph.tree_topic):
            print(f'current element {el} with index {el.id}' + \
                'type 1 - to get next left, 2 - to get previous left,\
                3 - to get next right, 4 - to get previous right,\
                5 - to get out of walking')
            tree = self.graph.exclude_tree(self.graph.tree_topic)
            for element in el.walk(chain=tree.longest_chain):
                print(element)
                print(element.show_children())
                # iterate(self.choice(element, index))
            # for element
        iterate()
        print('chain is ended')

    def a_parth_matrix(self):
        print('\n\n\n')
        print(''' Walking down through the graph alongside ''')
        top = self.graph[56]#self.graph.tree_topic
        print(top.id, top)
        tree = self.graph.exclude_tree(top)
        for index, element in tree.longest_chain:
            print('------------------------------------------')
            print(element, 'is', index)
            print(element.show_children())
        print('------------------END------------------------')

    def __del__(self):
        print('Have a nice day!')
        # TODO: resole the issuses to make it works
        # https://github.com/python/cpython/issues/86369
        # https://github.com/python/cpython/issues/70976
        # with open(self.file_path, 'w', encoding='utf8') as file:
        #     file.write(str(self.graph))
        sys.exit(0)


if __name__ == '__main__':
    interface = CliGraphWalking(StringByStringRegularExpressionMask())
    # TODO: cut it bellow when issuses will be closed
    print(interface.graph)
    print(interface)
    with open(interface.file_path, 'w', encoding='utf8') as file:
        file.write(str(interface.graph))
    interface.a_parth_matrix()
