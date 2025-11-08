#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Protocol, Tuple, List, Dict, FrozenSet, Callable, Union
# , runtime_checkable TODO: LET IT WOULD BE WORK CORRECTLY WI INSPECT.SIGNATURE
from lib import typing


__all__ = ('InfoProtocol', 'GraphInfoProtocol', 'VertexProtocol',
    'GraphsDunderMethodsMixinProtocol', 'GraphProtocol', 'TreeProtocol',
    'ProtocoLoader', 'LoaderDetector',)


# --- Loader Protocols ---
# TODO: CHANGE THE NAME IN THE RIGHT WAY
class ProtocolLoader(Protocol):

    """
    Contract for all loaders (TXT, JSON, YAML, XML, etc.).
    Each loader should define supported extensions and implement the full
    loading + mapping API.
    """

    extensions: List[str]

    def loads_from(self, path: str, type: str, mode: str, starts: int) -> Iterable:
        ...

    @property
    def whole_chain(self) -> Iterable:
        ...

    @property
    def element_class(self):
        ...

    @property
    def chain_type(self):
        ...

    @property
    def ids(self) -> FrozenSet:
        ...

    @property
    def map(self) -> Dict:
        ...

    def convert_element(self, tmp: str):
        ...

    def chain_mapping_fuction(self, *args, **kwargs):
        ...

    def mapping_fuction(self, func: Callable, sequence: Iterable):
        ...


class LoaderDetector(Protocol):

    """
    Protocol for factories (FactoryLoader, MetaFactoryLoader).
    Responsible for picking the correct loader based on file extension.
    """

    def detect_loader(self, path: str) -> ProtocolLoader: 
        ...

    # FIXME: DON'T USE object literal use the same protocol
    def load(self, path: str, type: str = "r", mode: str = "r", starts: int = 0) -> object: 
        ...


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


# @runtime_checkable TODO: #24 LET IT WOULD BE WORK CORRECTLY WI INSPECT.SIGNATURE
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

class MaskProtocol(Protocol):


    def allow_node(self, node: str) -> bool:
        ...

    def allow_edge(self, u: str, v: str) -> bool:
        ...
