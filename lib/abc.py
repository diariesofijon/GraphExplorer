#!/usr/bin/env python
# pylint: disable=C0103,W0622,E0001
# pylint: disable=E0401

import abc
import collections.abc
from typing import (
    FrozenSet, Optional, Iterable, TypeVar, Set, Dict, Callable, List)


__all__ = ('AbstractElement', 'AbstractChain',
    'AbstractGraphMask','AbstractTree', 'AbstractLoader')

# TODO: Should I add typing or not

# TODO: Examine `__post_init__ ` for using dataclasses
# TODO: Examine `pickle` module for using pythonic dundermethods


# TODO: convert to the protocol
class AbstractChain(list):

    '''
        Listening of ids and other numerical order of indicators with widly
    usefull method for searching and slicing any indicator.
    '''

    # TODO: MAKE CHAIN UNIQUE PYTHONIC DATA STRUCTURE
    # ALSO KNOW AS GENRATOR AND ITERABLE, YAPE!!!!

    # TODO: HOW ARCHITECTURE HAVE TO LOOK LIKE -- READ BELOW
    # COMPOSITION IS BETTER THAN INHERITANCE!!!
    # POINT THAT -- CONVERT ALL THIS STUFF TO COMPOSTION LIKE DESIGNED IN
    # PYTHONIC lib.collections/lib.collections.abc libraries!!!!

    # @property
    # @abc.abstractmethod
    # def __buffer__(self):
    #     ''' memoryview(self) '''

    # @property
    # @abc.abstractmethod
    # def __realease_buffer__(self):
    #     ''' del memoryview(self) '''

    # @property
    # @abc.abstractmethod
    # def __copy__(self):
    #     ''' copy.copy(self) '''

    # @property
    # @abc.abstractmethod
    # def __deepcopy__(self, memo):
    #     ''' copy.deepcopy(self) '''

    # @property
    # @abc.abstractmethod
    # def __sizeof__(self):
    #     ''' sys.getsizeof(self) '''

    def start(self, index: int = 0):
        ''' First element of the chain from index '''
        return self[index]

    def end(self, index: int = -1):
        ''' Last element of the chain from index'''
        return self[len(self) - index]

    @abc.abstractmethod
    def filtered(self, func):
        '''
        returns duplicated collection of filtered by the function
        due pythonic filter
        '''

    def by_hash(self, key):
        return filter(lambda x: hash(x) == key, self)[0]

    def get_seed(self):
        yield from enumerate(self)

    @property
    @abc.abstractmethod
    def blank(self) -> bool:
        ''' Eximine can chain hold blank lines for meta data or can! '''


class AbstractLoader(abc.ABC):

    # @property
    # @abc.abstractmethod
    # def __buffer__(self):
    #     ''' memoryview(self) '''

    # @property
    # @abc.abstractmethod
    # def __realease_buffer__(self):
    #     ''' del memoryview(self) '''

    # @property
    # @abc.abstractmethod
    # def __copy__(self):
    #     ''' copy.copy(self) '''

    # @property
    # @abc.abstractmethod
    # def __deepcopy__(self, memo):
    #     ''' copy.deepcopy(self) '''

    # @property
    # @abc.abstractmethod
    # def __sizeof__(self):
    #     ''' sys.getsizeof(self) '''

    cached_context: str = ''

    @property
    @abc.abstractmethod
    def whole_chain(self) -> Iterable:
        pass

    @property
    @abc.abstractmethod
    def element_class(self):
        pass

    @property
    @abc.abstractmethod
    def ids(self) -> FrozenSet:
        pass

    @property
    @abc.abstractmethod
    def map(self) -> Dict:
        pass

    @abc.abstractmethod
    def loads_from(self, path: str, type: str, mode: str='r', starts: int= 0):
        pass

    @abc.abstractmethod
    def convert_element(self, tmp: str):
    	pass

    @abc.abstractmethod
    def chain_mapping_fuction(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def mapping_fuction(self, func: Callable, sequence: Iterable):
        pass

    @abc.abstractmethod
    def __del__(self):
        '''
        Pythonic Loader's Garbadge Collector
        '''


class AbstractTree(collections.abc.Mapping):

    ''' Iterable tree representation of a graph '''

    # TODO: step by step
    # make clear and useful interface for trees +
    # explain available the way in singleton  pattern or not. Whe it frozen by
    # definition. + clearly explain where it properties that listed bellow have
    # to be used make the graph easier to use and move functionability due it
    # take down new documentation of the graph’s functionality

    # have to explaning augmenting path through the first to the end

    # @property
    # @abc.abstractmethod
    # def _sliced_graph(self):
    #     ''' Private link on a graph  '''

    # @property
    # @abc.abstractmethod
    # def __buffer__(self):
    #     ''' memoryview(self) '''

    # @property
    # @abc.abstractmethod
    # def __realease_buffer__(self):
    #     ''' del memoryview(self) '''

    # @property
    # @abc.abstractmethod
    # def __copy__(self):
    #     ''' copy.copy(self) '''

    # @property
    # @abc.abstractmethod
    # def __deepcopy__(self, memo):
    #     ''' copy.deepcopy(self) '''

    # @property
    # @abc.abstractmethod
    # def __sizeof__(self):
    #     ''' sys.getsizeof(self) '''

    @property
    @abc.abstractmethod
    def element_ids(self) -> Iterable[int]:
        ''' Frozen set of all trees ids'''

    @property
    @abc.abstractmethod
    def longest_chain(self) -> Iterable[int]:
        ''' The chain of the longes_road '''

    @property
    @abc.abstractmethod
    def depth(self) -> int:
        ''' The number that is the length of the longes road '''

    @abc.abstractmethod
    def dfs(self):
        ''' DFS as generator '''

    @abc.abstractmethod
    def top(self):
        ''' DFS as generator '''

    @abc.abstractmethod
    def bfs(self):
        ''' BFS as generator '''

    # @abc.abstractmethod
    # def chain(self):
    #     ''' clear generator by all of the available tree components '''

    # @abc.abstractmethod
    # def topological_sort(self):
    #     ''' Topological sequence '''

    @abc.abstractmethod
    def __del__(self):
        '''
        Pythonic Tree's Garbadge Collector
        '''


class AbstractGraphMask(collections.abc.Collection):

    ''' Base image of engine to convert text to a graph '''

    @abc.abstractmethod
    def __repr__(self):
        ''' Unique pythonic representation '''

    @abc.abstractmethod
    def __str__(self):
        ''' Unique string representation '''

    # @property
    # @abc.abstractmethod
    # def __buffer__(self):
    #     ''' memoryview(self) '''

    # @property
    # @abc.abstractmethod
    # def __realease_buffer__(self):
    #     ''' del memoryview(self) '''

    # @property
    # @abc.abstractmethod
    # def __copy__(self):
    #     ''' copy.copy(self) '''

    # @property
    # @abc.abstractmethod
    # def __deepcopy__(self, memo):
    #     ''' copy.deepcopy(self) '''

    # @property
    # @abc.abstractmethod
    # def __sizeof__(self):
    #     ''' sys.getsizeof(self) '''

    @property
    @abc.abstractmethod
    def separeter(self) -> Optional[str]:
        '''
        The symbol that used to separaing each node of the text
        representation of the graph
        '''

    @property
    @abc.abstractmethod
    def file(self) -> str:
        ''' Which file from engine have to load text of the graph '''

    # @property
    # @abc.abstractmethod
    # def loader(self):
    #     ''' The way which defined who would load data '''

    @property
    @abc.abstractmethod
    def element_class(self):
        ''' Pythonic class to implement each node to valid form '''

    @abc.abstractmethod
    def exclude_tree(self):
        '''
        Find the sequence which can work like a tree. Raise
        Vaildation Error if it has no any tree variant
        '''

    @property
    @abc.abstractmethod
    def tree_topic(self):
        ''' Highest element in the biggest tree of the graph '''

    @property
    def is_bipartite(self) -> bool:
        ''' Check if a graph is bipartite '''
        # TODO: in first time it doesn't matter
        return False

    @abc.abstractmethod
    def __del__(self):
        '''
        Pythonic Graph's Garbadge Collector
        '''


class AbstractElement(collections.abc.Hashable):

    ''' Base image of engine to realize each element of the graph '''

    # private pythonic proxy method for
    # RepresentativeGraphElementAbstract.children
    # _children: Optional[List[int]] = None
    # _parents: Optional[List[int]] = None
    # TODO: IMPLEMENT PYTHONIC COLLECTION ABSTRACTION
    # TODO: MAKE IT SINGLETONE

    @abc.abstractmethod
    def __hash__(self):
        ''' Have works due unique id charcter '''

    @abc.abstractmethod
    def __repr__(self) -> str:
        ''' Unique pythonic representation '''

    @abc.abstractmethod
    def __str__(self) -> str:
        ''' Unique string representation '''

    # @property
    # @abc.abstractmethod
    # def __buffer__(self):
    #     ''' memoryview(self) '''

    # @property
    # @abc.abstractmethod
    # def __realease_buffer__(self):
    #     ''' del memoryview(self) '''

    # @property
    # @abc.abstractmethod
    # def __copy__(self):
    #     ''' copy.copy(self) '''

    # @property
    # @abc.abstractmethod
    # def __deepcopy__(self, memo):
    #     ''' copy.deepcopy(self) '''

    # @property
    # @abc.abstractmethod
    # def __sizeof__(self):
    #     ''' sys.getsizeof(self) '''

    @property
    @abc.abstractmethod
    def id(self) -> str:
        ''' Id key of the node '''

    @property
    @abc.abstractmethod
    def part(self) -> str:
        ''' Part indetity of the node '''

    @property
    @abc.abstractmethod
    def grouped(self) -> str:
        ''' Other info about the node in the Eisenhower matrix '''

    @property
    @abc.abstractmethod
    def body(self) -> str:
        ''' The node's body contains info about parent's ids'''

    @property
    @abc.abstractmethod
    def graph(self):
        ''' Graph that contains the node '''

    @property
    @abc.abstractmethod
    def children(self):
        ''' Nodes that linked on the node '''

    @property
    @abc.abstractmethod
    def parents(self):
        ''' Nodes that have pointed by the node '''

    @abc.abstractmethod
    def __del__(self):
        '''
        Pythonic Element's Garbadge Collector
        '''
