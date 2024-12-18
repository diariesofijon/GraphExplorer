#!/usr/bin/env python

'''
Enums helps us collect all valided data structures to use it as pairs or any
bigger collection.
'''

from enum import Enum
from collections import defaultdict
from dataclasses import dataclass, field

from lib import typing

# TODO: convert to the protocol
@dataclass
class VertexInfo(Enum):

    # TODO: LETS METACLASS IDICATE VERTEXTINFO DUPLICATES

    # tree: typing.Tree = field(default=None)
    start: typing.GE  = field(hash=True)
    end: typing.GE    = field(hash=True)
    depth: int        = field(default=0)
    edges: int        = field(default=0)
    story: dict       = field(default_factory=lambda: defaultdict({}))

    @property
    def maximum_vertex(self):
        return max(self.story.keys())

    # def validation(self):
    #     ''' Have to explain why the Tree could not exists '''
    #     if not (self.tree and self.start and self.end):
    #         raise config.ValidationError
    #     if self.depth and self.start is self.end:
    #         raise config.ValidationError
