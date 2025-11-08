#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
