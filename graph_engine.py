#!/usr/bin/env python
# pylint: disable=C0103,W0622,E1136

'''
    Loads graph from a file as a text through regexp
'''

# fix: find another way to find points of graph due pythonic RegExp
# import re
from dataclasses import dataclass, field
from typing import Optional, List, Union, Iterable, Dict

import config
from base import (
    StringRegularExpressionMaskAbstract, GE, GGE,
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
    # TODO: REMOVE OPTIONAL
    graph: Optional[StringRegularExpressionMaskAbstract] = None
    separater_key: str = ''

    def __str__(self):
        return f'{self.part} id: {self.id} = {self.grouped} - {self.body}'

    def __repr__(self):
        return self.__str__()

    # TODO: move all show logic to new console or graphic interface in MIXIN
    # inheretince way
    def show_children(self):
        ''' Texted view of children of the elemenet '''
        return self._separeter().join(str(child) for child in self.children)

    def show_parents(self):
        ''' Texted view of parents of the elemenet '''
        return self._separeter().join(str(parent) for parent in self.parents)

    def walk(self, left: bool = True, chain: Optional[List] = None):
        '''
        Walking down through the graph to the deep to see how grap was changed
        '''
        if chain:
            index = chain.pop()
        else:
            return self
        next_el = self.children[index] if left else self.children.end(index)
        yield next_el
        # fix: make deep searching algorithm based on this property
        yield from next_el.walk(left=left, chain=chain)

    def _separeter(self):
        return config.SEPARATES.get(self.separater_key, self.graph.separeter)


@dataclass()
class StringByStringRegularExpressionMask(StringRegularExpressionMaskAbstract):

    ''' Sensetive turn off '''

    element_mask: Optional[str] = r'.+(?P<id>\D+)\..?(?P<grouped>.+): (?P<body>.*)\n'
    node_mask: Optional[str] = r'(?P<id>\D+)\((?P<children_list>.*)\)'
    part_mask: Optional[str] = r'.*(?P<id>\S+\D+\).\n'
    tmp: Optional[str] = None
    separeter: str = config.SEPARATES.get('NODE')
    file: str = config.FILE_DATA_LOADER_PATH
    last_part: str = 'A1.'
    element_class: GE = RepresentativeGraphElementMask

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.tmp:
            with open(self.file, 'r', encoding='utf8') as file:
                self.tmp: str = file.read()
        # TODO: it worth but i have to load self.ids_map
        for _ in self:
            continue

    def __iter__(self) -> GGE:
        return iter(self._get_formated_links())

    def __len__(self) -> int:
        return len(list(self._get_formated_links()))

    def __str__(self) -> str:
        return self.separeter.join(str(tmp) for tmp in iter(self))

    def __repr__(self) -> str:
        return self.__str__()

    def __getitem__(self, key: int, pythonic_list: bool = True) -> GE:
        if pythonic_list:
            return tuple(self)[key]
        for part, _id in self.ids_map:
            if key <= _id:
                return self.get_element(part, key)
            key -= _id
            continue
        raise IndexError()

    def __contains__(self, element: GE) -> bool:
        try:
            element = self.get_element(element.part, element.id)
        except IndexError:
            return False
        return isinstance(element, self.element_class)

    def _get_formated_links(self):
        for link in self.tmp.split(self.separeter):
            if (tmp := link.strip()).endswith('.'):
                self.last_part = tmp
                continue
            if not tmp:
                # ATTENTION: ignore blank line
                continue
            yield from self._convert_element(tmp, self.last_part)

    def get_elements(self, part: str =None, id: Union[str, int] =None) -> GE:
        if not id and not part:
            raise IndexError()
        if not part:
            # fix: it would be good idea if we can search only by id???
            raise IndexError('Part has not defined when id was passed')
        if id and part:
            yield from (el for el in self if el.part == part and el.id == id)

    def get_element(self, part: str =None, id: Union[str, int] =None) -> GE:
        # TODO: refactor the idea of methods get_element and get_elements
        absolute_id = id
        for key, value in self.ids_map.items():
            if key == part:
                break
            absolute_id += value
        # TODO: sequence of keis have to start from zero indstead of one
        return self[absolute_id-1]

    @property
    def dfs_depth(self) -> int:
        ''' The deepth of the graph '''
        # fix: make deep searching algorithm based on this property
        return len(self)-1

    @property
    def longest_chain(self) -> Iterable[int]:
        ''' The logest chain to iterate through the DFS algorithm '''
        return [0 for _ in range(self.dfs_depth)]
