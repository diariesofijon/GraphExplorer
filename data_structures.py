#!/usr/bin/env python
# pylint: disable=C0103,W0622,E1136
# pylint: disable=E0401

'''
    Loads graph from a file as a text through regexp
'''

# fix: find another way to find points of graph due pythonic RegExp
# import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional, List, Union, Iterable, FrozenSet, Dict

import config
from lib import drivers, base, abc, typing, shortcuts
from elements import RepresentativeElement


__all__ = (
    'StringByStringGraphMask', 'FrozenTree', 'VertexSearcingTree',
    'VertexInfo', 'EisenhoverMatrixConvertationMask',)

# https://www.javatpoint.com/bfs-vs-dfs#:~:text=DFS%20stands%20for%20Depth%20First,Last%20In%20First%20Out)%20principle


@dataclass
class VertexInfo:

    # TODO: LETS METACLASS IDICATE VERTEXTINFO DUPLICATES

    # tree: typing.Tree = field(default=None)
    start: typing.GE  = field()
    end: typing.GE    = field(default=None)
    depth: int        = field(default=0)
    edges: int        = field(default=0)
    story: Dict       = field(default_factory=lambda: defaultdict(dict))

    @property
    def maximum_vertex(self):
        return max(self.story.keys())

    def validation(self):
        ''' Have to explain why the Tree could not exists '''
        if not (self.tree and self.start and self.end):
            raise config.ValidationError
        if self.depth and self.start is self.end:
            raise config.ValidationError


@dataclass
class FrozenTree(base.BaseTree):

    element_class: typing.GE = RepresentativeElement
    loader: typing.Loader    = field(default_factory=drivers.TxtLoader())


@dataclass
class VertexSearcingTree(FrozenTree):

    ''' Frozen Tree '''

    left: VertexInfo  = field()
    right: VertexInfo = field()


@dataclass
class StringByStringGraphMask(base.BaseGraphMask):

    element_class: typing.GE = RepresentativeElement

    ''' Sensetive turn off '''

    def exclude_tree(self) -> typing.Tree:
        '''
        Find the sequence which can work like a tree. Raise
        Vaildation Error if it has no any tree variant
        '''
        ids = [el.id for el in self.tree_topic.walk()]
        return FrozenTree(self,
            element_ids=ids, element_class=self.element_class, top=self.tree_topic)


@dataclass
class EisenhoverMatrixConvertationMask(StringByStringGraphMask):

    loader: typing.Loader = field(default_factory=drivers.EisenhoverMatrixLoader)
    vertexes: Dict        = field(default_factory=lambda: defaultdict(dict))

    def exclude_tree(self, story: VertexInfo) -> typing.Tree:
        # TODO: tree's class have be located in the class fields versus
        # tree's instance have be initialized from this bound method?
        '''
        Find the sequence which can work like a tree. Raise
        Vaildation Error if it has no any tree variant
        '''
        ids = [el.id for el in self.tree_topic.walk()]
        return VertexSearcingTree(self, left=story, right=story,
            element_ids=ids, element_class=self.element_class, top=self.tree_topic)

    def get_orthodox_eisenhover_info(self, index: int) -> Dict:
        part: str = self.loader.get_part_by_id(index)
        executive_id: int = index - self.loader.ids_map[part]
        return {'part': part, 'executive_id': executive_id}

    def find_the_rigth_tree_by_vertex_size(self, count: int=5, recursion: bool=False):
        # But also the best count has two varients of the tree
        # the best tree has smallest count of edge
        story, edges_lengths = {count: self.tree_topic}, len(self)
        # TODO: THIRDLY: convert this for loop to recursion conception from another function interface!!!
        for element in self:
            # TODO: FOURTHLY: move it logic to the VertexInfo
            self.tree_topic = element
            tree, edges = self.dfs()
            if len(edges) < edges_lengths:
                edges_lengths, story[count] = len(edges), element
            tree = self.exclude_tree(left=story, right=story)
            yield len(tree), tree, story, shortcuts.is_bipartite(edges)
        if recursion and count:
            yield from self.find_the_rigth_tree_by_vertex_size(
                count=(count-1), recursion=recursion)

    def 
