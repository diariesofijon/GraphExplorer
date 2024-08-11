#!/usr/bin/env python
# pylint: disable=C0103,W0622,E0001
# pylint: disable=E0401

'''
    Abstract classes for graph exploring
'''

import abc
from dataclasses import dataclass, field
from typing import FrozenSet, Tuple, List, Optional, Dict, Iterable, Callable

import config
from lib import shortcuts, abc, drivers, typing


__all__ = ('BaseTree', 'BaseElement', 'BaseGraphMask')


@dataclass
class BaseElement(abc.AbstractElement):

    ''' Base Element from the Graph '''

    id: str = ''
    part: str = ''
    grouped: str = ''
    body: str = ''
    graph: typing.GM = None
    separater_key: str = 'NODE'

    def __str__(self):
        return f'{self.part} id: {self.id} = {self.grouped} - {self.body}'

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return self.id # TODO: have to use hasheable function instead

    @property
    def children(self) -> typing.Chain:
        ''' Nodes that linked on the node '''
        param: Callable = lambda el: self in el.parents
        return self.graph.loader.chain_type([*self.graph]).filtered(param)

    @property
    def parents(self) -> typing.Chain:
        ''' Nodes that have pointed by the node '''
        _parents = self.graph.loader.chain_type()
        splited_by_body = self.body.split(')')
        for group in splited_by_body[0:len(splited_by_body)-1]:
            part, ids = group.lstrip(',').strip().split('(')
            part = list(self.graph.loader.ids_map.keys())[int(part)-1]
            for index in shortcuts.get_ids(ids.split(',')):
                index = int(index)
                _parents.append(self.graph[index])
        return _parents

    # PRIVATE

    def _separeter(self):
        return config.SEPARATES.get(self.separater_key, self.graph.separeter)



class BaseLoader(abc.AbstractLoader):

    file_path: str = 'example'
    separeter: str = config.SEPARATES.get('NODE')
    element_class: typing.GE = BaseElement

    _ids: FrozenSet = frozenset({})
    _map: Dict = {}

    def __init__(self, etype: Optional[typing.GE] = None):
        if etype:
            self.element_class: typing.GE = etype
        self.loads_from(self.file_path)

    def __len__(self):
        return len(self.ids)

    @property
    def map(self):
        if not self._map:
            for idx, element in enumerate(self.whole_chain):
                self._map[idx+1] = element
        return self._map

    @property
    def ids(self):
        if not self._ids:
            self._ids = frozenset(map(int, self.map.keys()))
        return self._ids

    def loads_from(self, path: str, mode: str='r', starts: int= 0):
        with open(path, mode, encoding=config.ENCODING) as file:
            self.cached_context: str = file.read()
        return self.cached_context[starts:]

    @property
    def whole_chain(self) -> Iterable:
        self.loads_from(self.file_path)
        separeted: Iterable = self.cached_context.split(self.separeter)
        yield from self.mapping_fuction(self.chain_mapping_fuction, separeted)

    def convert_element(self, tmp: str) -> typing.GGE:
        ''' Engine convertor '''
        match len((splited:=tmp.split(':'))):
            case 0:
                grouped, body = 'splited', 'splited'
            case 1:
                grouped, body = splited, splited
            case _:
                grouped, body = splited
        return self.element_class(
            id=self._last_index, grouped=grouped, body=body, graph=self)

    # TODO: explain the idea in docs
    def mapping_fuction(self, func: Callable, sequence: Iterable):
        yield from map(func, sequence)

    # TODO: explain the idea in docs
    def chain_mapping_fuction(self, *args, **kwargs):
        return self.convert_element(*args, **kwargs)


@dataclass
class BaseGraphMask(abc.AbstractGraphMask):

    ''' Sensetive turn on '''

    tmp: Optional[str] = None
    separeter: str = config.SEPARATES.get('NODE')
    file: str = config.FILE_DATA_LOADER_PATH
    element_class: typing.GE = BaseElement
    loader_class: typing.Loader = BaseLoader
    # loader: typing.Loader = field(default=BaseLoader())

    def __iter__(self) -> typing.GGE:
        return iter(self.loader.whole_chain)

    def __len__(self) -> int:
        return len(list(self.loader.whole_chain))

    def __str__(self) -> str:
        return self.separeter.join(str(tmp) for tmp in iter(self))

    def __repr__(self) -> str:
        return self.__str__()

    def __getitem__(self, key: int) -> typing.GE:
        # TODO: place awqay the validation
        # don't forget that it question about error arised in the same place that
        # have be corrected instead of doing in another way like done bellow
        # if isinstance(key, RepresentativeGraphElementMask):
        #     key = key.id # may be trouble araised only in dfs
        # TODO: It have be removed from logic because it have work unrelated to the data
        return self.loader.map[key]

    def __contains__(self, element: typing.GE) -> bool:
        # LEGACY BEFORE LOADER CONCEPTION
        # try:
        #     element = self.get_element(element.part, element.id)
        # except IndexError:
        #     return False
        # return isinstance(element, self.element_class)
        return element in self.loader.map.items()

    _loader: Optional[typing.Loader] = None

    @property
    def loader(self) -> typing.Loader:
        if not self._loader:
            self._loader: typing.Loader = self.loader_class()
        return self._loader

    # TODO: refactor it
    _topic = None

    @property
    def tree_topic(self) -> typing.GE:
        ''' Highest element in the biggest tree of the graph '''
        if not self._topic:
            self._topic: typing.GE = list(self)[0]
        return self._topic # TODO: make magic algortihm which return the top of the biggest tree

    @tree_topic.setter
    def tree_topic(self, element: typing.GE) -> typing.GE:
        ''' Highest element in the biggest tree of the graph '''
        # if isinstance(element, RepresentativeGraphElementMask):
        #     self._topic = element
        # raise config.ValidationError
        self._topic: typing.GE = element

    def exclude_tree(self) -> typing.Tree:
        '''
        Find the sequence which can work like a tree. Raise
        Vaildation Error if it has no any tree variant
        '''
        ids = [el.id for el in self.tree_topic.walk()]
        return BaseTree(self, ids)

    def dfs(self, vertex: int = -1) -> Tuple[List]:
        # TODO: should to work in the composition way
        maxdepth, visited, queue = 0, [], []
        visited.append(self.tree_topic)
        queue.append((self.tree_topic,1))
        while queue:
            x, depth = queue.pop(0)
            if depth > vertex > -1: # TODO: take down docs about negative vertex conceptions
                break
            else:
                # TODO: take down documentation about the idea why should we use already defined maxdepth
                maxdepth = max(maxdepth, depth)
            # for child in self[x.id].children: # TODO: why have i chosen this variant
            for child in x.children:
                if child not in visited:
                    visited.append(child)
                    queue.append((child,depth+1))
        return queue, visited


@dataclass
class BaseTree(abc.AbstractTree):

    ''' Base Tree '''

    _sliced_graph: typing.GM = None
    # TODO: find the way of searching elements by a hash
    element_ids: Optional[List[int]] = None
    element_class: typing.GE = BaseElement

    def __iter__(self) -> typing.GGE:
        return iter(self[_id] for _id in self.element_ids)

    def __len__(self) -> int:
        return len(list(self[_id] for _id in self.element_ids))

    def __str__(self) -> str:
        return str(self._sliced_graph + ' Tree')

    def __repr__(self) -> str:
        return self.__str__()

    def __getitem__(self, key: int) -> typing.GE:
        if key not in self.element_ids:
            raise config.OutFromTreeError
        return self._sliced_graph[key]

    def __contains__(self, element: typing.GE) -> bool:
        return element.id in self.element_ids

    @property
    def longest_chain(self) -> Iterable:
        _, visited = self.dfs()
        yield from visited

    @property
    def depth(self) -> int:
        ''' The deepth of the graph '''
        # fix: make deep searching algorithm based on this property
        return len(self.longest_chain)

    @property
    def top(self) -> typing.GE:
        return self.element_ids[0]

    def dfs(self):
        maxdepth, visited, queue = 0, [], []
        visited.append(self.top)
        queue.append((self.top,1))
        while queue:
            x, depth = queue.pop(0)
            maxdepth = max(maxdepth, depth)
            # for child in self[x.id].children: # TODO: why have i chosen this variant
            for child in x.children:
                if child not in visited:
                    visited.append(child)
                    queue.append((child,depth+1))
        return queue, visited
