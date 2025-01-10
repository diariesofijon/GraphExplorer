#!/usr/bin/env python

from typing import Protocol, Iterable, Tuple, List
# , runtime_checkable TODO: LET IT WOULD BE WORK CORRECTLY WI INSPECT.SIGNATURE
from lib import typing


__all__ = ('InfoProtocol', 'GraphInfoProtocol', 'VertexProtocol',
    'GraphsDunderMethodsMixinProtocol', 'GraphProtocol', 'TreeProtocol')


# @runtime_checkable TODO: LET IT WOULD BE WORK CORRECTLY WI INSPECT.SIGNATURE
class InfoProtocol(Protocol):

    @property
    def counted_protocol(self) -> Protocol:
        ...


# @runtime_checkable TODO: LET IT WOULD BE WORK CORRECTLY WI INSPECT.SIGNATURE
class GraphInfoProtocol(InfoProtocol):

    @property
    def top(self) -> typing.GE:
        ...

    @property
    def depth(self) -> int:
        ...


# @runtime_checkable TODO: LET IT WOULD BE WORK CORRECTLY WI INSPECT.SIGNATURE
class VertexProtocol(GraphInfoProtocol):

    @property
    def last(self) -> typing.GE:
        ...

    @property
    def edges(self) -> Iterable[typing.GE]:
        ...

    @property
    def story(self) -> dict:
        ...

    @property
    def maximum_vertex(self) -> int:
        ...

    def choose_graph(self, depth: int):
        ...


class GraphsDunderMethodsMixinProtocol(Protocol):

    def __iter__(self) -> typing.GGE:
        ...

    def __len__(self) -> int:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    def __getitem__(self, key: int) -> typing.GE:
        ...

    def __contains__(self, element: typing.GE) -> bool:
        ...

    def __del__(self):
        ...


# @runtime_checkable TODO: LET IT WOULD BE WORK CORRECTLY WI INSPECT.SIGNATURE
def GraphProtocol(Protocol):

    def is_bipartite(self) -> bool:
        ...

    def loader(self) -> typing.Loader:
        ...

    def dfs(self, vertex: int) -> Tuple[List]:
        ...

    def bfs(self, node: typing.GE, visited: List) -> Tuple[List]:
        ...


# @runtime_checkable TODO: LET IT WOULD BE WORK CORRECTLY WI INSPECT.SIGNATURE
class TreeProtocol(Protocol):

    def graph(self) -> GraphProtocol:
        ...

    def element_ids(self) -> List[int]:
        ...

    def top(self) -> typing.GE:
        ...

    def longest_chain(self) -> Iterable:
        ...

    def depth(self) -> int:
        ...

    def dfs(self) -> Tuple[List]:
        '''
        Best case performance for a depth-first algorithm is O(1),
        while worst case performance is O(N). In another words The time
        complexity of the DFS algorithm is O(V+E), where V is the number
        of vertices and E is the number of edges in the graph.
        '''
        ...

    def bfs(self, node: typing.GE, visited: List) -> Tuple[List]:
        ...
