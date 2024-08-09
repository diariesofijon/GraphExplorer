#!/usr/bin/env python
# pylint: disable=C0103,W0622,E0001
# pylint: disable=E0401

'''
    Abstract classes for graph exploring
'''

import abc
from dataclasses import dataclass, field
from typing import FrozenSet, Tuple, List, Optional

import config
from lib import shortcuts, abc, drivers, typing


__all__ = ('BaseTree', 'BaseElement', 'BaseGraphMask')


@dataclass
class BaseGraphMask(abc.AbstractGraphMask):

    ''' Sensetive turn on '''

    tmp: Optional[str] = None
    separeter: str = config.SEPARATES.get('NODE')
    file: str = config.FILE_DATA_LOADER_PATH
    element_class: typing.GE = BaseElement
    loader_class: drivers.AbstractLoader = drivers.TxtLoader
    loader_class: abc.AbstractLoader = drivers.BaseLoader
    loader: abc.AbstractLoader = field(default=drivers.BaseLoader)

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

    # TODO: refactor it
    _topic = None

    @property
    def tree_topic(self) -> typing.GE:
        ''' Highest element in the biggest tree of the graph '''
        if not self._topic:
            self._topic = list(self)[0]
        return self._topic # TODO: make magic algortihm which return the top of the biggest tree

    @tree_topic.setter
    def tree_topic(self, element: typing.GE) -> typing.GE:
        ''' Highest element in the biggest tree of the graph '''
        # if isinstance(element, RepresentativeGraphElementMask):
        #     self._topic = element
        # raise config.ValidationError
        self._topic = element

    def exlude_tree(self) -> typing.Tree:
        '''
        Find the sequence which can work like a tree. Raise
        Vaildation Error if it has no any tree variant
        '''
        ids = {el.id for el in self.tree_topic.walk()}
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
class BaseTree(abc.AbstractGraphMask):

    ''' Base Tree '''

    _sliced_graph: typing.GM = None
    # TODO: find the way of searching elements by a hash
    element_ids: FrozenSet[int] = None

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
    def depth(self) -> int:
        ''' The deepth of the graph '''
        # fix: make deep searching algorithm based on this property
        return self.dfs()[0]

    def dfs(self):
        maxdepth, visited, queue = 0, [], []
        visited.append(self.tree_topic)
        queue.append((self.tree_topic,1))
        while queue:
            x, depth = queue.pop(0)
            maxdepth = max(maxdepth, depth)
            # for child in self[x.id].children: # TODO: why have i chosen this variant
            for child in x.children:
                if child not in visited:
                    visited.append(child)
                    queue.append((child,depth+1))
        return queue, visited


@dataclass
class BaseElement(abc.AbstractElement):

    ''' Base Element from the Graph '''

    id: str = ''
    part: str = ''
    grouped: str = ''
    body: str = ''
    graph: abc.AbstractGraphMask = None
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
        param = lambda el: self in el.parents
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
