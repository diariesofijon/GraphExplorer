#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0103,W0622,E0001
# pylint: disable=E0401

'''
    Key conceptions of classes for graph exploring
'''

import sys
from dataclasses import dataclass, field
from typing import FrozenSet, Tuple, List, Optional, Dict, Iterable, Callable
from copy import copy, deepcopy

import config
from bin import metaclasses, protocols
from lib import shortcuts, abc, drivers, typing, chains


__all__ = ('BaseLoader',
    'BaseTree', 'BaseElement', 'BaseGraphMask', 'BasicTextFormatter')


def index_factory(return_type=int, index = -1):

    def mechanism():
        index += 1
        return return_type(index)

    return mechanism

class BasicTextFormatter(abc.AbstractTextFormatter):

    def get_kwargs_element(self, text: str) -> Dict:
        return {
            'id':		  None,
            'globals':	  None,
            'body':		  None,
            'graph':	  None,
            'separeter':  None,
            'chain_type': None,}

    def mask(self, kind: bool) -> protocols.MaskProtocol:
        if kind:
            return masks.NodeWhitelistMask()
        return maks.NoMaks()

    def format(self, text: str) -> str:
        lines = text.splitlines()
        cleaned = []
        for ln in lines:
            ln2 = ln.strip()
            if not ln2:
                continue
            if ln2.startswith("#"):  # treat as comment
                continue
            ln2 = ln2.replace(" -> ", "->")  # normalize arrow spacing
            cleaned.append(ln2)
        return "\n".join(cleaned)


@dataclass(frozen=True, kw_only=True, slots=True, unsafe_hash=True)
class BaseElement(abc.AbstractElement):

    ''' Base Element from the Graph '''

    __metaclass__    = metaclasses.MetaElement

    id: str          = field(hash=True, default_factory=index_factory())
    globals: dict    = field(default_factory=lambda:dict())
    part: str        = field(default='')
    grouped: str     = field(default='')
    body: str        = field(default='')
    graph: typing.GM = field(hash=True, default=None)
    separater: str   = config.SEPARATES.get('NODE')
    chain_type       = chains.TxtChain
    formatter_type   = BasicTextFormatter

    def __str__(self):
        # TODO: it would be located in the Eisenhowever logic
        part = self.part if self.part else 'SIMPLE'
        return f'{part} id: {self.id} = {self.grouped} - {self.body}'\

    def __del__(self):
        '''
        Pythonic Element's Garbadge Collector
        '''
        del self.globals
        for child in self.children:
            del child

    @property
    def children_index(self):
        return f'children-{repr(self)}-{self.id}'

    @property
    def parents_index(self):
        return f'parents-{repr(self)}-{self.id}'

    @property
    def children(self) -> typing.Chain:
        ''' Nodes that linked on the node '''
        if not self.globals.get(self.children_index):
            param: Callable = lambda el: self in el.parents
            self.globals[self.children_index] = \
            self.chain_type([*self.graph]).filtered(param)
        return self.globals[self.children_index]

    @property
    def parents(self) -> typing.Chain:
        ''' Nodes that have pointed by the node '''
        if (_parents := self.globals.get(self.parents_index)):
            return _parents
        _parents = self.chain_type([])
        for index in formatter_type().format(self.body):
            _parents.append(self.graph[int(index)])
        return _parents


@dataclass
class BaseLoader(abc.AbstractLoader):

    __metaclass__    = metaclasses.MetaLoader

    file_path: str              = 'example'
    separeter: str              = config.SEPARATES.get('NODE')
    element_class: typing.GE    = BaseElement
    formatter: typing.Formatter = field(default_factory=BasicTextFormatter)

    _ids: FrozenSet  = field(default_factory=dict)
    _map: Dict       = field(default_factory=dict)
    _last_index: int = 0

    def __post_init__(self, graph: typing.GM, etype: Optional[typing.GE] = None):
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
        del self.self.instance_graph
        del self.cached_context
    
    def __sizeof__(self):
        return sum(sys.getsizeof(self.cached_context),
                   sys.getsizeof(self._ids,
                   sys.getsizeof(self._map),
                   sys.getsizeof(self._last_index),
                   sys.getsizeof(dir(self.formatter))
    
    # TODO: #33 makes test and docs, benchmarks for
    # each __copy__, __deepcopy__, __buffer__, __release_buffer__
    def __copy__(self):
        loader = type(self)(self.graph)
        return loader
    
    def __deepcopy__(self):
        return copy(self)

    def __buffer__(self, flag: int, /):
        sep     = bytearray(self.separeter, config.ENCODING)
        name    = bytearray(self.__name__)
        content = bytearray(self.cached_context)
        return name + sep + content
    
    def __release_buffer__(self, buffer: bytearray, /):
        info: str = release(buffer)
        if not info.startswith(self.__name__):
            raise BufferError
        content: str = info.split(self.separeter)[0::-1]
        loader = type(self)(type(self.graph)())
        loader.cached_context = content
        return loader

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
        # TODO: #29 makes it works strictly when it turn any composed api
        grouped, body = self.format(tmp)
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

    def __sizeof__(self) -> int:
        return sum(sys.getsizeof(self._visited),
                   sys.getsizeof(self._queue),
                   sys.getsizeof(self.file),
                   sys.getsizeof(self.separeter))

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
        # TODO: #32 make docs for all dunders please
        return element in self.loader.map.items()

    def __del__(self):
         '''
         Pythonic Graph's Garbadge Collector
         '''
         del self.file
         del self.separeter
         del self.element_class
         if self._loader:
             del self._loader
             del self._visited
             del self._queue
             del self._topic

    def __copy__(self):
        '''
            Copy only pointer on the graphs mask.
        '''
        return type(self)(*self)

    def __deepcopy__(self):
        '''
            Clearly copy all masked needed data pointed as a graph sructure. Has no side effects.
        '''
        graph = copy(self)
        graph.file     = deepcopy(graph.file)
        graph.separeter = deepcopy(graph.separeter)
        # TODO: make works as field without private fileds
        graph._loader = None
        graph.dfs()
        return graph

    def __buffer__(self, flags: int, /):
        '''
            Can replicated from each self and works faster the copy(...) or deepcopy(...)
        '''
        chain = bytearray(*self, config.ENCODING)
        name  = bytearray(self.__name__, config.ENCODING)
        sep   = bytearray(self.separeter, config.ENCODING)
        by    = bytearray(self.loader.__name__, config.ENCODING)
        return name + sep + by + sep + chain
        # may be could be better
        # return bytearray((key for key in(
        #     str(*self),self.__name__, 
        #     self.loader.__name__)).join(self.separeter), config.ENCODING)

    def __release_buffer__(self, buffer: bytearray, /):
        converted = release(buffer)
        for cls in mro(self):
            if converted.startswith(cls.__name__):
                _, by, chain = converted.split(cls.separeter)
                if not cls.loader.__name__ == by:
                    raise ValueError(by + ' is not loader')
                return cls(*release(chain))

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

    def add_edge(self, parents, children, data=None):
        print('Realize add_edge, please')


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
