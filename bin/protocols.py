#!/usr/bin/env python

from typing import Protocol, runtime_checkable, Iterable


@runtime_checkable
class RepresintationProtocol(Protocol):
    pass


@runtime_checkable
class InfoProtocol(Protocol):

    @property
    def counted_protocol(self) -> Protocol:
        ...


@runtime_checkable
class GraphInfoProtocol(InfoProtocol):

    @property
    def top(self) -> RepresintationProtocol:
        ...

    @property
    def depth(self) -> int:
        ...


@runtime_checkable
class VertexProtocol(GraphInfoProtocol):

    @property
    def last(self) -> RepresintationProtocol:
        ...

    @property
    def edges(self) -> Iterable[RepresintationProtocol]:
        ...

    @property
    def story(self) -> dict:
        ...

    @property
    def maximum_vertex(self) -> int:
        ...

    def choose_graph(self, depth: int):
        ...
