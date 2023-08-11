#!/usr/bin/env python
# pylint: disable=C0103,W0622,E1136

'''
    Loads graph from a file as a text through regexp
'''

# fix: find another way to find points of graph due pythonic RegExp
# import re
from dataclasses import dataclass
from typing import Optional, List, Union, Iterable, FrozenSet, Callable, Tuple

import config
from base import (
    StringRegularExpressionMaskAbstract, GE, GGE, GM, Tree, _Chain,
    RepresentativeGraphElementAbstract, GraphTreeRepresintationMaskAbstract)


__all__ = (
    'RepresentativeGraphElementMask', 'StringByStringRegularExpressionMask')


@dataclass
class RepresentativeGraphElementMask(RepresentativeGraphElementAbstract):

    ''' Sensetive turn off '''

    id: str = ''
    part: str = ''
    grouped: str = ''
    body: str = ''
    graph: StringRegularExpressionMaskAbstract = None
    separater_key: str = 'NODE'

    def __str__(self):
        return f'{self.part} id: {self.id} = {self.grouped} - {self.body}'

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return self.id # TODO: have to use hasheable function instead

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
            index, next_el = chain.pop()
        else:
            return self
        if not left: # TODO: find optimal routing
            next_el = self.children.end(index)
        yield next_el
        # fix: make deep searching algorithm based on this property
        yield from next_el.walk(left=left, chain=chain)

    def _separeter(self):
        return config.SEPARATES.get(self.separater_key, self.graph.separeter)


# @dataclass TODO: where I have to use dataclasses
class GraphTreeRepresentationMask(GraphTreeRepresintationMaskAbstract):

    ''' Frozen Tree '''

    _sliced_graph: GM = None
    # TODO: find the way of searching elements by a hash
    element_ids: FrozenSet[int] = None
    longest_chain: List[Tuple] = []
    
    def __init__(self, _sliced_graph=None, top=None, ids=None, chain=[]):
        self._sliced_graph: GM = _sliced_graph
        # TODO: find the way of searching elements by a hash
        self.element_ids: FrozenSet[int] = None
        self.longest_chain: List[Tuple] = []
        self.top = top
        self.depth = self.dfs()

    def __iter__(self) -> GGE:
        return iter(self._sliced_graph[_id] for _id in self.element_ids)

    def __len__(self) -> int:
        return len(list(self._sliced_graph[_id] for _id in self.element_ids))

    def __str__(self) -> str:
        return str(self._sliced_graph + ' Tree')

    def __repr__(self) -> str:
        return self.__str__()

    def __getitem__(self, key: int, pythonic_list: bool = True) -> GE:
        if key not in self.element_ids:
            raise config.OutFromTreeError
        return self._sliced_graph[key]

    def __contains__(self, element: GE) -> bool:
        return element.id in self.element_ids

    def dfs(self) -> int:
        ''' The deepth of the graph '''
        # fix: make deep searching algorithm based on this property
        # TODO: should to work in the composition way
        visited, queue, mdepth = [], [], 0
        visited.append(self.top)
        queue.append((self.top,1))
        while queue:
            x, depth = queue.pop(0)
            mdepth = max(mdepth, depth)
            for index, child in enumerate(x.children):
                if child not in visited:
                    visited.append(child)
                    queue.append((child,depth+1))
                    self.longest_chain += (index, child)
        return mdepth

    # @property
    # def longest_chain(self) -> Iterable[int]:
    #     ''' The logest chain to iterate through the DFS algorithm '''
    #     return self._longest_chain

    # def dfs(self) -> GGE:
    #     # TODO: should to work in the composition way
    #     visited, queue, self._depth = [], [], 0
    #     visited.append(self._top)
    #     queue.append((self._top,1))
    #     while queue:
    #         x, depth = queue.pop(0)
    #         self._depth = max(self._depth, depth)
    #         for index, child in enumerate(x.children):
    #             if child not in visited:
    #                 visited.append(child)
    #                 queue.append((child,depth+1))
    #     return self._depth, _Chain(map(lambda x: x.id, visited))

@dataclass
class StringByStringRegularExpressionMask(StringRegularExpressionMaskAbstract):

    ''' Sensetive turn off '''

    # TODO: move it to an another class like composition
    # element_mask: Optional[str] = r'.+(?P<id>\D+)\..?(?P<grouped>.+): (?P<body>.*)\n'
    # node_mask: Optional[str] = r'(?P<id>\D+)\((?P<children_list>.*)\)'
    # part_mask: Optional[str] = r'.*(?P<id>\S+\D+\).\n'
    tmp: Optional[str] = None
    separeter: str = config.SEPARATES.get('NODE')
    file: str = config.FILE_DATA_LOADER_PATH
    last_part: str = 'A1.'
    element_class: GE = RepresentativeGraphElementMask
    _tree: Optional[Tree] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.tmp:
            with open(self.file, 'r', encoding='utf8') as file:
                self.tmp: str = file.read()

        # TODO: it worth but i have to load self.ids_map
        for _ in self:
            continue
        
        _tree = self.exclude_tree(self[0])
        for index, element in enumerate(self):
            if not index: continue
            if _tree.depth < (b:=self.exclude_tree(element)).depth:
                _tree = b
            print(_tree.depth)
        self.tree_topic = _tree

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
            return [el for el in self][key]
        for part, _id in self.ids_map.items():
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
        for key, value in self.ids_map.items():
            if key == part:
                break
            id += (value - 1)
        # TODO: sequence of keis have to start from zero indstead of one
        return self[id]

    def exclude_tree(self, element: GE) -> Tree:
        '''
        Find the sequence which can work like a tree. Raise
        Vaildation Error if it has no any tree variant
        '''
        if (t:=type(element)) is not self.element_class:
            raise TypeError(f'{t} is not a element class')
        return GraphTreeRepresentationMask(self, element)

    # def _try_another_topic(self) -> Callable:
    #     topics = set()
    #     trees = set()
    #     def tmp():
    #         topics += self.tree_topic
    #         trees += self._last_tree
    #         _all = [_id for _id in self]
    #         return filtered(lambda x: x not in self.last_tree.element_ids, _all)[0]
    
    # def try_another_topic(self) -> GE:
    #     get_id = self._try_another_topic()
    #     return self[get_id()]
    
    # def set_another_topic(self):
    #     self.tree_topic = try_another_topic()
