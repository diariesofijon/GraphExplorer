#!/usr/bin/env python
# pylint: disable=C0103

'''
    Abstract classes for graphj exploring
'''

# hot fix: add finding elements of graph in text by pythonic regexp
# import re
from dataclasses import dataclass
from typing import Optional


__all__ = (
    'StringRegularExpressionMaskAbstract', 'RepresentativeGraphElementAbstract')


@dataclass
class StringRegularExpressionMaskAbstract:

    ''' Base image of engine to convert text to a graph '''

    def __repr__(self):
        ''' Unique pythonic representation '''
        raise NotImplementedError(f'Have to definded in {self.__class__.__name__}.')

    def __str__(self):
        ''' Unique string representation '''
        raise NotImplementedError(f'Have to definded in {self.__class__.__name__}.')


    def __new__(cls, *args, **kwargs):
        ''' to fix: Defenition of the graph have attrib or similart to dataclass default values '''
        if not cls.tmp and not kwargs.get('tmp', ''):
            with open(cls.file, 'r') as file:
                cls.tmp = file.read()
        return super().__new__(cls, *args, **kwargs)

    @property
    def element_mask(self) -> Optional[str]:
        ''' RegExp for finding each element of the node '''
        raise NotImplementedError(f'Have to definded in {self.__class__.__name__}.')

    @property
    def node_mask(self) -> Optional[str]:
        ''' RegExp for finding eahc node of the graph'''
        raise NotImplementedError(f'Have to definded in {self.__class__.__name__}.')

    @property
    def part_mask(self) -> Optional[str]:
        ''' RegExp for finding part of each node '''
        raise NotImplementedError(f'Have to definded in {self.__class__.__name__}.')

    @property
    def tmp(self) -> Optional[str]:
        ''' String of full texted graph '''
        raise NotImplementedError(f'Have to definded in {self.__class__.__name__}.')

    @property
    def separeter(self) -> Optional[str]:
        ''' The symbol that used to separaing each node of the text representation of the graph '''
        raise NotImplementedError(f'Have to definded in {self.__class__.__name__}.')

    @property
    def file(self) -> str:
        ''' Which file from engine have to load text of the graph '''
        raise NotImplementedError(f'Have to definded in {self.__class__.__name__}.')

    @property
    def last_part(self) -> str:
        ''' String iteration flag indecate what node have a part '''
        raise NotImplementedError(f'Have to definded in {self.__class__.__name__}.')

    @property
    def element_class(self):
        ''' Pythonic class to implement each node to valid form '''
        raise NotImplementedError(f'Have to definded in {self.__class__.__name__}.')

    def get_elements(self, part=None, id=None):
        ''' Method that return node by part or id '''
        raise NotImplementedError(f'Have to definded in {self.__class__.__name__}.')

    def get_element(self, part=None, id=None):
        ''' Method that return filterd nodes by part or id '''
        raise NotImplementedError(f'Have to definded in {self.__class__.__name__}.')

    def _get_formated_links(self):
        ''' Private method that list all nodes '''
        raise NotImplementedError(f'Have to definded in {self.__class__.__name__}.')

    @staticmethod
    def _get_ids(name):
        ''' Clear function that implement name to ids '''
        if len(tmp := name.split('-')) == 2:
            return list(range(int(tmp[0]), int(tmp[1])+1))
        return [int(name)]

    def _convert_element(self, tmp, last_part):
        ''' Engien convertor '''
        if  len((splited := tmp.split('.'))) == 1:
            splited = splited, ''
        ids, tmp = splited
        for id in self._get_ids(ids):
            grouped, body = tmp.split(':')
            data = self.element_class(
                id=id, grouped=grouped, part=last_part, body=body)
            yield data


@dataclass
class RepresentativeGraphElementAbstract:

    ''' Base image of engine to realize each element of the graph '''

    # private pythonic proxy method for RepresentativeGraphElementAbstract.children
    _children: list = None

    def __repr__(self):
        ''' Unique pythonic representation '''
        raise NotImplementedErorr

    def __str__(self):
        ''' Unique string representation '''
        raise NotImplementedErorr

    @property
    def id(self) -> str:
        ''' Id key of the node '''
        raise NotImplementedErorr

    @property
    def part(self) -> str:
        ''' Part indetity of the node '''
        raise NotImplementedErorr

    @property
    def grouped(self) -> str:
        ''' Other info about the node '''
        raise NotImplementedErorr

    @property
    def body(self) -> str:
        ''' Body of the node '''
        raise NotImplementedErorr

    @property
    def graph(self):
        ''' Graph that contains the node '''
        raise NotImplementedErorr

    @property
    def children(self):
        ''' Nodes that linked on the node '''
        if self._children is None:
            self._children = list(*self.graph.get_elements(
                part=self.part, id=self.id))
        return self._children

    @property
    def parents(self):
        ''' Nodes that have pointed by the node '''
        for element in self.graph:
            for child in element.children:
                if int(child.id) == int(self.id):
                    yield element
                    break

    # hot fix what do it do
    # def load(self, string=None, part=None, id=None):
    #     '''   '''
    #     if file:
    #         with open(self.graph.file, 'r') as file:
    #             return self.graph.get_element(part, id)
    #     elif string:
    #         return self.graph.get_element(part, id)
    #     else:
    #         raise Indexerror('Unexpected behavior')
