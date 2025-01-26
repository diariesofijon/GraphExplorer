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
from bin import metaclasses
from lib import drivers, base, abc, typing, shortcuts, enums
from elements import RepresentativeElement


__all__ = (
    'StringByStringGraphMask', 'FrozenTree', 'VertexSearcingTree',
    'EisenhoverMatrixConvertationMask',)

# https://www.javatpoint.com/bfs-vs-dfs#:~:text=DFS%20stands%20for%20Depth%20First,Last%20In%20First%20Out)%20principle


@dataclass
class FrozenTree(base.BaseTree):

    __metaclasses__ = metaclasses.MetaFrozenTree

    element_class: typing.GE = RepresentativeElement


@dataclass
class VertexSearcingTree(FrozenTree):

    ''' Frozen Tree '''
    # TODO: move to the bin/metaclasses.py through the enum.py

    story: enums.VertexInfo = field(default=None)


@dataclass
class StringByStringGraphMask(base.BaseGraphMask):

    __metaclasses__ = metaclasses.MetaRepresentativeGraph

    element_class: typing.GE = RepresentativeElement
    loader: typing.Loader    = field(default_factory=drivers.TxtLoader)

    ''' Sensetive turn off '''

    def exclude_tree(self) -> typing.Tree:
        '''
        Find the sequence which can work like a tree. Raise
        Vaildation Error if it has no any tree variant
        '''
        return FrozenTree(self, element_ids=self._ids, top=self.tree_topic)


@dataclass
class EisenhoverMatrixConvertationMask(StringByStringGraphMask):

    loader_class: typing.Loader = drivers.EisenhoverMatrixLoader
    story: enums.VertexInfo     = field(default=None)

    def __init__(self, *args, **kwargs):
        self._vertex = enums.VertexInfo(
                top=self.tree_topic,
                last=self.dfs()[1][0::-1],
                depth=len(self))
        self.vertexes[self] = self._vertex
        super().__init__(*args, **kwargs)

    def exclude_tree(self, story: enums.VertexInfo) -> typing.Tree:
        # TODO: tree's class have be located in the class fields versus
        # tree's instance have be initialized from this bound method?
        '''
        Find the sequence which can work like a tree. Raise
        Vaildation Error if it has no any tree variant
        '''
        return VertexSearcingTree(self, story=story,
            element_ids=self._ids, top=self.tree_topic)

    def get_orthodox_eisenhover_info(self, index: int) -> Dict:
        part: str = self.loader.get_part_by_id(index)
        executive_id: int = index - self.loader.ids_map[part]
        return {'part': part, 'executive_id': executive_id}

    def find_the_rigth_tree_by_vertex_size(self, count: int=5, recursion: bool=False):
        # But also the best count has two varients of the tree
        # the best tree has smallest count of edge
        story, edges_lengths = self.vertexes, len(self)
        # TODO: THIRDLY: convert this for loop to recursion conception from another function interface!!!
        for element in self:
            # TODO: FOURTHLY: move it logic to the VertexInfo
            self.tree_topic = element
            tree, edges = self.dfs()
            if len(edges) < edges_lengths:
                edges_lengths, story[count] = len(edges), element
            tree = self.exclude_tree(story=story)
            yield len(tree), tree, story, shortcuts.is_bipartite(edges)
        if recursion and count:
            yield from self.find_the_rigth_tree_by_vertex_size(
                count=(count-1), recursion=recursion)

    _main = None

    @property
    def main_variant(self):
        if self._main:
            return self._main
        return self

    @main_variant.setter
    def main_variant(self, graph):
        self._main = graph

    def setup_main_variant(self, vertex):
        vertex.story += self.vertex.story
        loader = drivers.MockLoader()
        loader.whole_chain = self.loader.whole_chain
        self.main_variant = EisenhoverMatrixConvertationMask(
            loader=drivers.MockLoader(), story=vertex, tree_topic=vertex.top)
        return self.main_variant

    def get_A_part_matrix(self):
        return self.dfs(vertex=self.story.story.values()[-1])[1]

    def get_B_part_matrix(self):
        return self.main_variant.story.story.edges

    def get_C_part_matrix(self):
        result = self.dfs(vertex=self.story.story.values()[-1])[0]
        for edge in result:
            if edge not in self.main_variant.story.story.edges:
                yield edge