#!/usr/bin/env python

'''
Enums helps us collect all valided data structures to use it as pairs or any
bigger collection.
'''

from enum import Enum, unique
from collections import defaultdict
from dataclasses import dataclass, field

from lib import typing, chains


@unique
@dataclass
class VertexInfo(Enum):

    top: typing.GE  = field(hash=True)
    last: typing.GE = field(hash=True)
    depth: int      = field(default=0)
    edges: list     = field(
        default_factory=lambda: chains.EisenhowerMatrixChain())
    story: dict     = field(default_factory=lambda: defaultdict({}))

    @property
    def maximum_vertex(self) -> int:
        return max(self.story.keys())

    # def validation(self):
    #     ''' Have to explain why the Tree could not exists '''
    #     if not (self.tree and self.top and self.last):
    #         raise config.ValidationError
    #     if self.depth and self.top is self.last:
    #         raise config.ValidationError

    def choose_graph(self, depth=1):
        '''
        Find the best variant of the Tree or of the Graph that can be instanced
        from the result and based on O(log[n]) algorithm.
        '''
        pair, length, last_graph = (self, self), len(self.edges), None
        for graph, vertex in self.story.items():
            if graph is last_graph:
                continue
            last_graph = graph
            if length < len(vertex.edges):
                length, pair = len(vertex.edges), (vertex, pair[0])
            depth -= 1
            if not depth:
                break
        return pair
