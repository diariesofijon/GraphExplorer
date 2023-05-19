#!/usr/bin/env python
# pylint: disable=C0103,W0622

'''
    Loads graph from a file
'''

# fix: find another way to find points of graph due pythonic RegExp
# import re
from dataclasses import dataclass
from typing import Optional, List, Union, Iterable

import config
from base import (
    StringRegularExpressionMaskAbstract, GE,
    RepresentativeGraphElementAbstract)


__all__ = (
    'RepresentativeGraphElementMask', 'StringByStringRegularExpressionMask')


@dataclass
class RepresentativeGraphElementMask(RepresentativeGraphElementAbstract):

    ''' Sensetive turn off '''

    id: str = ''
    part: str = ''
    grouped: str = ''
    body: str = ''
    graph: Optional[StringRegularExpressionMaskAbstract] = None
    separater_key: str = ''

    def __str__(self):
        return f'{self.part} id: {self.id} = {self.grouped} - {self.body}'

    def __repr__(self):
        return self.__str__()

    def show_children(self):
        ''' Texted view of children of the elemenet '''
        return self._separeter.join(child for child in self.children)

    def show_parents(self):
        ''' Texted view of parents of the elemenet '''
        return self._separeter.join(parent for parent in self.parents)

    def walk(self, l: bool = True, c: Optional[List] = None):
        ''' Walking down through the graph to the deep '''
        yield (next_el := self.children[(i:=c.pop())] if l else self.children.end(i))
        # fix: make deep searching algorithm based on this property
        yield from next_el.walk(l=l, c=c)

    @property
    def _separeter(self):
        return config.SEPARATES.get(self.separater_key, self.graph.separeter)


@dataclass
class StringByStringRegularExpressionMask(StringRegularExpressionMaskAbstract):

    ''' Sensetive turn off '''

    element_mask: Optional[str] = r'.+(?P<id>\D+)\..?(?P<grouped>.+): (?P<body>.*)\n'
    node_mask: Optional[str] = r'(?P<id>\D+)\((?P<children_list>.*)\)'
    part_mask: Optional[str] = r'.*(?P<id>\S+\D+\).\n'
    tmp: Optional[str] = None
    separeter: str = '\n'
    file: str = 'graph_links.txt'
    last_part: str = 'A1.'
    element_class = RepresentativeGraphElementMask

    def __iter__(self):
        return iter(self._get_formated_links())

    def __str__(self):
        return self.separeter.join(str(tmp) for tmp in iter(self))

    def _get_formated_links(self):
        for link in self.tmp.split(self.separeter):
            if (tmp := link.strip()).endswith('.'):
                self.last_part = tmp
                continue
            yield from self._convert_element(tmp, self.last_part)

    def get_element(self, part: str =None, id: Union[str, int] =None) -> GE:
        if id and not part:
            # fix: it would be good idea if we can search only by id???
            raise IndexError('Part has not defined when id was passed')
        if id and part:
            yield from (el for el in self if el.starswith(part) and el.id == id)
        raise IndexError('Unknown id or part')

    def get_elements(self, part: str =None, id: Union[str, int] =None) -> GE:
        return self.get_elements(part, id)[0]

    @property
    def depth_range(self) -> int:
        return len(self) # fix: make deep searching algorithm based on this property

    @property
    def longes_cain(self) -> Iterable:
        return [0 for _ in range(self.depth_range)]
