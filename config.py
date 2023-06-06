#!/usr/bin/env python
# pylint: disable=C0103
# pylint: disable=W0622
# pylint: disable=E0602
# pylint: disable=E0001

'''
        This file contains all settings of the project like constans,
    dictionaries, list and variables. All of data are strictly designed due
    idea of keeping easear to change behavior of anythings deal of the module
    in theruntime.
'''

import os.path
import abc

# TODO: make logger settings and add pythonic logger into the project!!!!

SEPARATES = {
    'NODE': '\n',
}

ABSOLUTE_PATH = os.path.abspath('.')

LOADS_DATA_FROM_DATABASE = False

LOADS_DATA_FROM_THE_FILE = not LOADS_DATA_FROM_DATABASE

FILE_DATA_LOADER_NAME = 'graph_links.txt'

FILE_DATA_CONTAINER_NAME = 'output.txt'

FILE_DATA_LOADER_PATH = f'{ABSOLUTE_PATH}/{FILE_DATA_LOADER_NAME}'

FILE_DATA_CONTAINER_PATH = f'{ABSOLUTE_PATH}/{FILE_DATA_CONTAINER_NAME}'


class ConfigError(abc.ABC, Exception):

    ''' Abstract class of config exception '''

    @property
    @abc.abstractmethod
    def to_do_message(self) -> str:
        ''' Explain what engineer have to do when it arised '''

    @property
    @abc.abstractmethod
    def constant_undefined(self) -> str:
        ''' Which constant has not defined '''

    @property
    @abc.abstractmethod
    def traceback_message(self) -> str:
        ''' Contains traceback information '''

    def __init__(self, *args, **kwargs)  :
        last_traceback = f'{self.traceback_message}: '
        last_traceback += ' - '.join(
            [self.constant_undefined, self.to_do_message])
        last_traceback += '.'
        super().__init__(self, last_traceback, *args, **kwargs)

class UndefinedConstant(ConfigError):

    ''' Undefined Constant abstract class '''

    traceback_message: str = 'Undefined constant'

class GraphLinksFileNameHasNotDefined(UndefinedConstant):

    ''' Explain how to define path which from shoud loud the data '''

    to_do_message: str = 'Define in configs files path which from \
        shoud loud the data'
    constant_undefined: str = 'config.FILE_DATA_LOADER_NAME'


class OutPutLinksFileNameHasNotDefined(UndefinedConstant):

    ''' Explain how to define path which from shoud loud the data '''

    to_do_message: str = 'Define in configs files path that required \
        to place the data'
    constant_undefined: str = 'config.FILE_DATA_CONTAINER_NAME'

class ValidationError(ConfigError):

    ''' Explain how to convert one data structure to an antoher '''

    traceback_message: str = 'Validation Error'

# TODO: make classes for graphs, trees and matrixs

class OutFromTreeError(ValidationError):

    ''' Explain how which is element have to ignore '''

    to_do_message: str = 'You have use element which are out of the tree'
    constant_undefined: str = 'data_structures.Tree'
