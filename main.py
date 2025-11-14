#!/usr/bin/env python
# -*- coding: utf-8 -*-
#pylint: disable=C0103,C0114
# pylint: disable=E0401

'''
    TODO: make DFS step by step
        1. function bounded method for the graph which fitler by tree belonging
            1. Make test for the trees and graph of minimum of the 80% coverage
            2. Proof the conception of the Enums of VertexInfo
            3. Proof the conception that Graph related to the EMatrix 
                due same methods
            4. makes works separetly as clear function 
                find_the_rigth_tree_by_vertex_size, get_orthodox_Eisenhower_info
        2. function bounded method for the graph which filter by tree absent
            1. integration test for show_graph_image_slice
            2. How graph can be stored
            3. How it can be stored as a matrix
        3. function that sort graphs elements by the matrix' s part belonging
            1. Proof the bounded method which would convert the graph
            2. Test coverage
            3. use as step by step in cli
        4. matrix data
            1. makes pythonic object or use something else
            2. like 4 matrix separetly by used BaseElement related to the 
                father's Graph
        5. visualistaion
            1. which it could be?
            2. what should it do
            3. how to full fill evernote and trello
            4. how to compater due the plans
'''

import sys

from data_structures import EisenhowerMatrixConvertationMask
from interfaces.cli import CliGraphWalking
import config
import lib


if __name__ == '__main__':
    print('='*9, 'PROGRAM   CREATED', '='*9)
    mask = EisenhowerMatrixConvertationMask()
    print('='*9, 'MASK      CREATED', '='*9)
    interface = CliGraphWalking(mask)
    print('='*9, 'INTREFACE CREATED', '='*9)
    # TODO: cut it bellow when issuses will be closed
    # print(interface.graph)
    # print(interface)
    interface.show_graph_image_slice()
    with open(interface.file_path, 'w', encoding='utf8') as file:
        file.write(str(interface.graph))
    # interface.a_parth_matrix()
