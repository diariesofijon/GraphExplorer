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
from bin import metaclasses
from lib import shortcuts, abc, drivers, typing, chains


__all__ = ('BaseTree', 'BaseElement', 'BaseGraphMask')


def index_factory(return_type=str):

    _index = -1

    def mechanism():
        _index += 1
        return return_type(_index)

    return mechanism


@dataclass(frozen=True, kw_only=True, slots=True, unsafe_hash=True)
class BaseElement(abc.AbstractElement):

    ''' Base Element from the Graph '''

    __metaclass__    = metaclasses.MetaElement

    id: str          = field(hash=True, default_factory=index_factory())
    part: str        = field(default='')
    grouped: str     = field(default='')
    body: str        = field(default='')
    graph: typing.GM = field(hash=True, default=None)
    separater: str   = config.SEPARATES.get('NODE')
    chain_type       = chains.TxtChain

    def __str__(self):
        # TODO: it would be located in the Eisenhowever logic
        part = self.part if self.part else 'SIMPLE'
        return f'{part} id: {self.id} = {self.grouped} - {self.body}'\

    def __del__(self):
        '''
        Pythonic Element's Garbadge Collector
        '''
        for child in self.children:
            del child

    @property
    def children(self) -> typing.Chain:
        ''' Nodes that linked on the node '''
        param: Callable = lambda el: self in el.parents
        return self.graph.loader.chain_type([*self.graph]).filtered(param)

    @property
    def parents(self) -> typing.Chain:
        ''' Nodes that have pointed by the node '''
        # parents = self.graph.loader.chain_type([])
        # for _, ids in shortcuts.simplest_txt_element(self.body):
        #     ids = shortcuts.get_ids(ids) if isinstance(ids, str) else ids
        #     parents += [self.graph[int(i)] for i in ids]
        # return parents
        _parents = self.graph.loader.chain_type([])
        splited_by_body = self.body.split(')')
        for group in splited_by_body[0:len(splited_by_body)-1]:
            _, ids = group.lstrip(',').strip().split('(')
            for index in shortcuts.get_ids(ids.split(',')):
                index = int(index)
                _parents.append(self.graph[index])
        return _parents


class BaseLoader(abc.AbstractLoader):

    __metaclass__    = metaclasses.MetaLoader

    file_path: str           = 'example'
    separeter: str           = config.SEPARATES.get('NODE')
    element_class: typing.GE = BaseElement

    _ids: FrozenSet  = {}
    _map: Dict       = {}
    _last_index: int = 0

    def __init__(self, graph: typing.GM, etype: Optional[typing.GE] = None):
        self.instance_graph: typing.GM = graph
        if etype:
            self.element_class: typing.GE = etype
        if self.instance_graph.element_class is not self.element_class:
            raise config.ElementClassHasNotDefined
        self.loads_from(self.file_path)

    def __len__(self):
        return len(self.ids)

    def __del__(self):
        '''
        Pythonic Loader's Garbadge Collector
        Don't use when it is not pythonic dataclass
        '''
        # del self.file_path
        # del self.separeter
        # del self.element_class
        # del self._ids
        # del self._map
        # del self.cached_context
        pass

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
        separeted: Iterable = self.cached_context.split(self.separeter)
        yield from self.mapping_fuction(self.chain_mapping_fuction, separeted)

    def convert_element(self, tmp: str) -> typing.GGE:
        ''' Engine convertor '''
        grouped, body = shortcuts.separete_from_text_element(tmp)
        self._last_index += 1
        return self.element_class(graph=self.instance_graph,
            id=self._last_index, grouped=grouped, body=body)

    # TODO: explain the idea in docs
    def mapping_fuction(self, func: Callable, sequence: Iterable):
        yield from map(func, sequence)

    # TODO: explain the idea in docs
    def chain_mapping_fuction(self, *args, **kwargs):
        return self.convert_element(*args, **kwargs)


@dataclass
class BaseGraphMask(abc.AbstractGraphMask):

    ''' Sensetive turn on '''

    __metaclass__    = metaclasses.MetaGraph

    separeter: str             = config.SEPARATES.get('NODE')
    file: str                  = config.FILE_DATA_LOADER_PATH
    element_class: typing.GE   = BaseElement
    loader_class: typing.Loader= BaseLoader

    _visited: List[typing.GE] = field(default=None)
    _queue:   List[typing.GE] = field(default=None)

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

    def __del__(self):
        '''
        Pythonic Graph's Garbadge Collector
        '''
        # del self.file
        # del self.separeter
        # del self.element_class
        # del self.loader
        # del self._visited
        # del self._queue
        # del self._topic
        pass

    _loader = None

    @property
    def loader(self):
        if not self._loader:
            self._loader = self.loader_class(
                graph=self,etype=self.element_class)
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

    @property
    def _ids(self) -> List[int]:
        '''
        Simplified id's list constructed by BFS algorithm
        '''
        return [el.id for el in self.tree_topic.walk()]

    def exclude_tree(self) -> typing.Tree:
        '''
        Find the sequence which can work like a tree. Raise
        Vaildation Error if it has no any tree variant
        '''
        return BaseTree(self, element_ids=self._ids,
            element_class=self.element_class, top=self.tree_topic)

    def dfs(self, vertex: int = -1) -> Tuple[List]:
        '''
        Best case performance for a depth-first algorithm is O(1),
        while worst case performance is O(N). In another words The time
        complexity of the DFS algorithm is O(V+E), where V is the number
        of vertices and E is the number of edges in the graph.
        '''
        # TODO: should to work in the composition way
        maxdepth, visited, queue = 0, [self.tree_topic], [(self.tree_topic,1)]
        while queue:
            x, depth = queue.pop(0)
            # TODO: take down documentation about the idea why should we use already defined maxdepth
            maxdepth = max(maxdepth, depth)
            if depth > vertex > -1: # TODO: take down docs about negative vertex conceptions
                break
            # for child in self[x.id].children: # TODO: why have i chosen this variant
            for child in x.children:
                if child not in visited:
                    visited += child
                    queue += (child,depth+1)
        return queue, visited

    def bfs(self, node: Optional[typing.GE]=None, visited: Optional[List]=None):
        '''#function for BFS'''
        if node is None and visited is None: # should work with visited
            node = self.top                  # because graph should use it too
        if not self._visited or not self._queue:
            self._visited, self._queue = [node], [node]
        elif visited:
            self._visited, self._queue = visited, [node]
        while self._queue: # Creating loop to visit each node
            last = self._queue.pop(0) # logged it to understand how it works
            for neighbour in last.children:
                if neighbour not in self._visited:
                    self._visited += neighbour
                    self._queue += neighbour

        return self._visited, self._queue


@dataclass
class BaseTree(abc.AbstractTree):

    ''' Base Tree '''

    __metaclass__    = metaclasses.MetaTree

    element_ids: List[int]    = field(hash=True, default_factory=list)
    element_class: typing.GE  = BaseElement
    top: typing.GE            = field(hash=True, default=None)

    _visited: List[typing.GE] = field(default_factory=list)
    _queue:   List[typing.GE] = field(default_factory=list)

    def __iter__(self) -> typing.GGE:
        return iter(self[_id] for _id in self.element_ids)

    def __len__(self) -> int:
        return len(list(self[_id] for _id in self.element_ids))

    def __str__(self) -> str:
        return str(self._sliced_graph + ' Tree')

    def __getitem__(self, key: int) -> typing.GE:
        # TODO: would it be work with logarithmic complexity
        if key == self.top.id:
            return self.top
        if key in self.element_ids:
            smaller = filter(lambda x: x <= key, self.element_ids)
            smaller = filter(lambda x: x in smaller, self.bfs()[0])
            return filter(lambda x: x.id == key, smaller)[0]
        raise config.OutFromTreeError

    def __contains__(self, element: typing.GE) -> bool:
        return element.id in self.element_ids

    @property
    def longest_chain(self) -> Iterable:
        yield from self.dfs()[0]

    @property
    def depth(self) -> int:
        ''' The deepth of the graph '''
        # fix: make deep searching algorithm based on this property
        return len(self.longest_chain)

    def dfs(self):
        '''
        Best case performance for a depth-first algorithm is O(1),
        while worst case performance is O(N). In another words The time
        complexity of the DFS algorithm is O(V+E), where V is the number
        of vertices and E is the number of edges in the graph.
        '''
        maxdepth, visited, queue = 0, [self.top], [(self.top,1)]
        while queue:
            x, depth = queue.pop(0)
            maxdepth = max(maxdepth, depth)
            for child in x.children:
                if child not in visited and child.id in self.element_ids:
                    visited += child
                    queue += (child,depth+1)
        return queue, visited

    def bfs(self, node: Optional[typing.GE]=None, visited: Optional[List]=None):
        '''#function for BFS'''
        if node is None and visited is None: # should work with visited
            node = self.top                  # because graph should use it too
        if not self._visited or not self._queue:
            self._visited, self._queue = [node], [node]
        elif visited:
            self._visited, self._queue = visited, [node]
        while self._queue: # Creating loop to visit each node
            last = self._queue.pop(0) # logged it to understand how it works
            for neighbour in last.children:
                if neighbour not in self._visited:
                    self._visited += neighbour
                    self._queue += neighbour

        return self._visited, self._queue
