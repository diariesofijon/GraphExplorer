#!/usr/bin/env python
# pylint: disable=C0103,W0622,E0001

'''
    Abstract classes for graph exploring
'''

# hot fix: add finding elements of graph in text by pythonic regexp
# import re
import abc
import collections.abc
# TODO: IMPLEMENT PYTHONIC COLLECTION ABSTRACTION
from dataclasses import dataclass, field
from typing import Optional, TypeVar, List, Iterable, Union, Dict, FrozenSet, Set


__all__ = (
    'StringRegularExpressionMaskAbstract', 'GE', 'GGE', 'GM', 'Chain', 'Tree',
    'RepresentativeGraphElementAbstract', 'GraphTreeRepresintationMaskAbstract')

# types
# TODO: move all types to anatother file
GE = TypeVar('GE', bound='RepresentativeGraphElementAbstract')
# TODO: Dependevice injection from graph mask to pythonic graph
GM = TypeVar('GM', bound='StringRegularExpressionMaskAbstract')
# Graph = TypeVar('Graph', bound='...')
GGE = Iterable[GE]
Chain = TypeVar('Chain', bound='_Chain')
Tree = TypeVar('Tree', bound='GraphTreeRepresintationMaskAbstract')
NumericalSequence = Set[int]
ChainNumericals = Set[NumericalSequence]

class _Chain(list):

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

    def start(self, index: int = 0):
        ''' First element of the chain from index '''
        return self[index]

    def end(self, index: int = -1):
        ''' Last element of the chain from index'''
        return self[len(self) - index]

    def filtered(self, func):
        ''' returns duplicated collection of filtered by the function due pythonic filter '''
        return _Chain(filter(func, self))

    # def by_hash(self, key):
    #     return filter(lambda x: hash(x) == key, self)[0]

    def get_seed(self):
        for index, element in enumerate(self):
            yield (index, element)

class GraphTreeRepresintationMaskAbstract(collections.abc.Mapping):

    ''' Iterable tree representation of a graph '''

    # TODO: step by step
    # make clear and useful interface for trees +
    # explain available the way in singleton  pattern or not. Whe it frozen by definition. +
    # clearly explain where it properties that listed bellow have to be used
    # make the graph easier to use and move functionability due it
    # take down new documentation of the graph’s functionality

    # have to explaning augmenting path through the first to the end

    @property
    @abc.abstractmethod
    def _sliced_graph(self) -> GM:
        ''' Private link on a graph  '''

    @property
    @abc.abstractmethod
    def element_ids(self) -> FrozenSet[int]:
        ''' Frozen set of all trees ids'''

    # @property
    # @abc.abstractmethod
    # def longest_chain(self) -> Iterable[int]:
    #     ''' The chain of the longes_road '''

    # @property
    # @abc.abstractmethod
    # def depth(self) -> int:
    #     ''' The number that is the length of the longes road '''

    # @abc.abstractmethod
    # def dfs(self):
    #     ''' DFS as generator '''

    # @abc.abstractmethod
    # def bfs(self) -> GGE:
    #     ''' BFS as generator '''

    # @abc.abstractmethod
    # def chain(self) -> GGE:
    #     ''' clear generator by all of the available tree components '''

    # @abc.abstractmethod
    # def topological_sort(self) -> GGE:
    #     ''' Topological sequence '''


@dataclass
class StringRegularExpressionMaskAbstract(collections.abc.Collection):

    ''' Base image of engine to convert text to a graph '''
    # TODO: IMPLEMENT PYTHONIC COLLECTION ABSTRACTION

    @abc.abstractmethod
    def __repr__(self):
        ''' Unique pythonic representation '''

    @abc.abstractmethod
    def __str__(self):
        ''' Unique string representation '''

    # def __new__(cls, *args, **kwargs):
    #     '''
    #     to fix: Defenition of the graph have attrib or similart to
    #     dataclass default values
    #     '''
    #     if not cls.tmp and not kwargs.get('tmp', ''):
    #         with open(cls.file, 'r', encoding='utf8') as file:
    #             cls.tmp = file.read()
    #     return super().__new__(cls, *args, **kwargs)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(self, *args, **kwargs)
    #     print('self.tmp 1 ', self.tmp)
    #     if not self.tmp:
    #         print('self.tmp 2 ', self.tmp)
    #         with open(self.file, 'r', encoding='utf8') as file:
    #             print('self.tmp 3 ', self.tmp)
    #             self.tmp: str = file.read()

    # @property
    # @abc.abstractmethod
    # def element_mask(self) -> Optional[str]:
    #     ''' RegExp for finding each element of the node '''

    # @property
    # @abc.abstractmethod
    # def node_mask(self) -> Optional[str]:
    #     ''' RegExp for finding eahc node of the graph'''

    # @property
    # @abc.abstractmethod
    # def part_mask(self) -> Optional[str]:
    #     ''' RegExp for finding part of each node '''

    @property
    @abc.abstractmethod
    def tmp(self) -> Optional[str]:
        ''' String of full texted graph '''

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

    @property
    @abc.abstractmethod
    def _last_part(self) -> str:
        ''' String iteration flag indecate what node have a part '''

    @property
    @abc.abstractmethod
    def element_class(self) -> GE:
        ''' Pythonic class to implement each node to valid form '''

    # TODO: Can't instantiate abstract class ... with abstract method ids_map
    # TODO: it has not work due exclude_tree ids_map has defrent logic
    # TODO: let's try makes it hardcode
    ids_map: Dict[str, list] = field(default_factory=lambda:{'A1.': [0]})

    @abc.abstractmethod
    def get_elements(self, part: str =None, id: Union[str, int] =None) -> GGE:
        ''' Method that return node by part or id '''

    @abc.abstractmethod
    def get_element(self, part: str =None, id: Union[str, int] =None) -> GE:
        ''' Method that return filterd nodes by part or id '''

    @abc.abstractmethod
    def _get_formated_links(self) -> Iterable[str]:
        ''' Private method that list all nodes '''

    # @abc.abstractmethod
    # def exclude_tree(self) -> Tree:
    #     '''
    #     Find the sequence which can work like a tree. Raise
    #     Vaildation Error if it has no any tree variant
    #     '''

    # @property
    # @abc.abstractmethod
    # def tree_topic(self) -> GE:
    #     ''' Highest element in the biggest tree of the graph '''

    @property
    def is_bipartite(self) -> bool:
        ''' Check if a graph is bipartite '''
        # TODO: in first time it doesn't matter
        return False

    @staticmethod
    def _get_ids(name: str) -> List[int]:
        ''' Clear function that implement name to ids '''
        if len((tmp := name.split('-'))) == 2:
            return list(range(int(tmp[0]), int(tmp[1])+1))
        return [int(name)]

    def _convert_element(self, tmp: str, last_part: GE) -> GGE:
        ''' Engine convertor '''
        if len((splited := tmp.split('.'))) == 1:
            splited = splited[0], ''
        ids, tmp = splited
        match len((splited:=tmp.split(':'))):
            case 0:
                grouped, body = 'splited', 'splited'
            case 1:
                grouped, body = splited, splited
            case _:
                grouped, body = splited
        for id in self._get_ids(ids):
            data = self.element_class(
                id=id, grouped=grouped, part=last_part, body=body, graph=self)
            # TODO: just refactro it
            tmp = (self.ids_map.get(last_part, []) + [data])
            self.ids_map[last_part] = tmp
            yield data


@dataclass
class RepresentativeGraphElementAbstract(collections.abc.Hashable):

    ''' Base image of engine to realize each element of the graph '''

    # private pythonic proxy method for
    # RepresentativeGraphElementAbstract.children
    # _children: Optional[List[int]] = None
    # _parents: Optional[List[int]] = None
    # TODO: IMPLEMENT PYTHONIC COLLECTION ABSTRACTION
    # TODO: MAKE IT SINGLETONE

    # TODO: should it be abstract method?
    def __hash__(self):
        return self.id

    @abc.abstractmethod
    def __repr__(self) -> str:
        ''' Unique pythonic representation '''

    @abc.abstractmethod
    def __str__(self) -> str:
        ''' Unique string representation '''

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
    def graph(self) -> GM:
        ''' Graph that contains the node '''

    @property
    def children(self) -> Chain:
        ''' Nodes that linked on the node '''
        return _Chain([*self.graph]).filtered(lambda el: self in el.parents)

    @property
    def parents(self) -> Chain:
        ''' Nodes that have pointed by the node '''
        _parents = _Chain()
        # TODO: FIND MORE BEATIFUL SOLUTION INSTEAD OF [0:len(_)-1]
        for group in (_:=self.body.split(')'))[0:len(_)-1]:
            part, ids = group.lstrip(',').strip().split('(')
            part = list(self.graph.ids_map.keys())[int(part)-1]
            for g in ids.split(','):
                for _id in self.graph._get_ids(g):
                    _id = int(_id)
                    _parents.append(self.graph.get_element(part=part, id=_id))
        return _parents



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
