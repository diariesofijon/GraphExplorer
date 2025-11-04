#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0114

import sys

import data_structures
from interfaces import represintation, templates
import config
import lib


def legacy_walk(graph: lib.typing.GM, *args, **kwargs):
    ''' Walking down through the graph'''
    for element in graph.tree_topic.walk(graph.exclude_tree().longest_chain):
        with represintation.pretty_print_element(element, **kwargs) as nel:
            print(element.show_children())
            print(f'you had choose {nel.id}')
    else:
        print('chain is empty')
    print('chain is ended')

def show_pretty_graph(graph: lib.typing.GM, index: int =1):
    ''' Pretty printing of all graph '''
    print('\n\n\n')
    print(index)
    # starting walking from the first element
    legacy_walk(graph)


class CliGraphWalking(represintation.BaseGraphWalkingInterface):

    repr_type = int
    file_path = config.FILE_DATA_CONTAINER_NAME

    def show_graph_image_slice(self):
        maximum = typed if (typed:=int(input('times:'))) else 5
        for depth, vertex in self.defined_maximum_vertex_chain_index(maximum):
            vertex_pprint = templates.VertexPrinter(depth, vertex)
            vertex_pprint.print_status()
            vertex_pprint.print_choice_prompt()
        else:
            if int(input("Should we continue: 0 - no, 1 - yes ")):
                self.show_graph_image_slice()
        print('bye-bye')

    def choose_graph(self):
        depth = int(input('Inter the depth: '))
        pair = self.graph.story.choose_graph(depth=depth)
        print('Choose the main graph from two expected: ')
        print('FIRST GRAPH:\n', pair[0])
        print('SECOND GRAPH:\n', pair[1])
        index = 0 if input('is first (yes/no)') == 'no' else 1
        main = self.graph.setup_main_variant(pair[index])
        print(main, '\n\n----------------------------------------')
        with open(config.FILE_DATA_CONTAINER_NAME, 'w') as txt:
            txt.write(str(main))
        # TODO: make graph loaded from FILE_DATA_CONTAINER_NAME and show
        # how it would be look as matrix eisenhower

    def walk(self):
        ''' Walking down through the graph'''
        print('\n\n\n')
        legacy_walk(self.graph)

    def a_parth_matrix(self):
        print('\n\n\n')
        top = self.graph[56]#self.graph.tree_topic
        print(''' Walking down through the graph #{top.id}, {top} alongside ''')
        for index, element in self.graph.exclude_tree(top).longest_chain:
            kwargs = {'prefix': '-'*42, 'postfix': f'{element} is {index}',
            'sufix': '------------------END------------------------'}
            with represintation.pretty_print_element(element, **kwargs) as nel:
                print(element.show_children())
                print(f'you had choose {nel.id}')

    def __del__(self):
        print('Have a nice day!')
        # TODO: resole the issuses to make it works
        # https://github.com/python/cpython/issues/86369
        # https://github.com/python/cpython/issues/70976
        # with open(self.file_path, 'w', encoding='utf8') as file:
        #     file.write(str(self.graph))
        sys.exit(0)
