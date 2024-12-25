#!/usr/bin/env python

from typing import Protocol, runtime_checkable, Iterable

from lib import typing


@runtime_checkable
class InfoProtocol(Protocol):

    @property
    def counted_protocol(self) -> Protocol:
        ...


@runtime_checkable
class GraphInfoProtocol(InfoProtocol):

    @property
    def top(self) -> typing.GE:
        ...

    @property
    def depth(self) -> int:
        ...


@runtime_checkable
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
