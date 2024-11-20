#!/usr/bin/env python

from enum import Enume


class VertexInfo(Enum):

    # TODO: LETS METACLASS IDICATE VERTEXTINFO DUPLICATES

    # tree: typing.Tree = field(default=None)
    start: typing.GE  = field(hash=True)
    end: typing.GE    = field(hash=True)
    depth: int        = field(default=0)
    edges: int        = field(default=0)
    story: Dict       = field(default_factory=lambda: defaultdict({}))

    @property
    def maximum_vertex(self):
        return max(self.story.keys())

    # def validation(self):
    #     ''' Have to explain why the Tree could not exists '''
    #     if not (self.tree and self.start and self.end):
    #         raise config.ValidationError
    #     if self.depth and self.start is self.end:
    #         raise config.ValidationError
