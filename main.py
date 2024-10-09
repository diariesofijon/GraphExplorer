#!/usr/bin/env python
#pylint: disable=C0103,C0114
# pylint: disable=E0401

'''
    TODO: make DFS step by step
        1. function bounded method for the graph which fitler by tree belonging
        2. function bounded method for the graph which filter by tree absent
        3. function that sort graphs elements by the matrix' s part belonging
        4. matrix data
        5. visualistaion
'''

import sys
import abc
from dataclasses import dataclass, field
from typing import Optional

from data_structures import EisenhoverMatrixConvertationMask
import config
import lib


# TODO: make cool architecture console interface
class AbstractGraphWalkingInterface(abc.ABC):

    vertexes = {}
    _tree = None

    @property
    @abc.abstractmethod
    def graph(self) -> lib.typing.GM:
        ''' StringRegularExpressionMaskAbstract '''

    @property
    def tree(self):
        if self._tree:
            return self._tree
        return self.graph.exclude_tree()

    def defined_maximum_vertex_chain_index(self, maximum=5):
        self.graph.defined_maximum_vertex: int = maximum
        for vertex_info in self.tree.find_the_rigth_tree_by_vertex_size():
            self.vertexes[vertex_info[0]] = {
                'size': vertex_info[0],
                'left': vertex_info[2],
                'right': vertex_info[3]}
            yield vertex_info[1], self.vertexes[vertex_info[1]]


@dataclass
class CliGraphWalking(AbstractGraphWalkingInterface):

    graph: lib.typing.GM = field()
    repr_type: type      = int
    file_path: str       = config.FILE_DATA_CONTAINER_NAME
    # TODO: make clear console interface


    def choice(self, element: lib.typing.GE, index: int):
        ''' Returns next element '''
        if index in {1, 3}:
            index = 0 if index == 1 else -1
            return element.children[index]
        if index in {2, 4}:
            index = 0 if index == 2 else -1
            return element.parents[index]
        raise ValueError(f'Index {str(index)} is out of range')

    def show_graph_image_slice(self):
        maximum = typed if (typed:=int(input('times:'))) else 5
        for depth, vertex in self.defined_maximum_vertex_chain_index(maximum):
            print('Depth is ', depth)
            print('Size is ', vertex['size'])
            print('vertex left is ')
            print(vertex['left'])
            print('vertex right is ')
            print(vertex['right'])
            if vertex['size'] == 2:
                print(depth, " is the best")
                choice = input("Should we continue: 0 - no, 1 - yes ")
                if int(choice):
                    break
                else:
                    print('CHOSE THE BEST TOPIC') # LET IT BE IN THE CODE
                    if int(input('left is 0 or right is 1')):
                        print(vertex['right'])
                    else:
                        print(vertex['left'])
        else:
            if int(input("Should we continue: 0 - no, 1 - yes ")):
                self.show_graph_image_slice()
        print('bye-bye')


    def walk(self):
        ''' Walking down through the graph'''
        print('\n\n\n')
        if (index := self.repr_type(input())) not in {1,2,3,4}:
            raise TypeError(ValueError(f'{str(index)} have invalid type'))
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
    interface = CliGraphWalking(EisenhoverMatrixConvertationMask())
    # TODO: cut it bellow when issuses will be closed
    print(interface.graph)
    print(interface)
    with open(interface.file_path, 'w', encoding='utf8') as file:
        file.write(str(interface.graph))
    # interface.a_parth_matrix()
    interface.show_graph_image_slice()
