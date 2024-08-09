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
from lib import drivers, base, abc, typing


__all__ = ('RepresentativeElement', 'StringByStringGraphMask')

# https://www.javatpoint.com/bfs-vs-dfs#:~:text=DFS%20stands%20for%20Depth%20First,Last%20In%20First%20Out)%20principle


@dataclass
class RepresentativeElement(base.BaseElement):

    ''' Sensetive turn off '''


    # TODO: move all show logic to new console or graphic interface in MIXIN
    # inheretince way
    def show_children(self):
        ''' Texted view of children of the elemenet '''
        return self._separeter().join(str(child) for child in self.children)

    def show_parents(self):
        ''' Texted view of parents of the elemenet '''
        return self._separeter().join(str(parent) for parent in self.parents)

    def walk(self, left: bool = True, chain: Optional[List] = None):
        '''
        Walking down through the graph to the deep to see how grap was changed
        '''
        if chain:
            index = chain.pop()
        else:
            # TODO: that's arise trouble because self is not iterable
            return self
        next_el = self.children[index] if left else self.children.end(index)
        yield next_el
        # fix: make deep searching algorithm based on this property
        yield from next_el.walk(left=left, chain=chain)

@dataclass
class VertexInfo:

    # TODO: LETS METACLASS IDICATE VERTEXTINFO DUPLICATES

    tree: typing.Tree = field(default=None)
    start: typing.GE  = field(default=None)
    end: typing.GE    = field(default=None)
    depth: int            = field(default=0)

    def validation(self):
        ''' Have to explain why the Tree could not exists '''
        if not (self.tree and self.start and self.end):
            raise config.ValidationError
        if self.depth and self.start is self.end:
            raise config.ValidationError


@dataclass
class FrozenTree(base.BaseTree):
    pass

@dataclass
class VertexSearcingTree(FrozenTree):

    ''' Frozen Tree '''

    defined_maximum_vertex: int = 5
    trees_validated_vertex_left: VertexInfo = None
    trees_validated_vertex_right: VertexInfo = None
    _vertex_searching_story: defaultdict[dict] = field(default_factory=lambda: defaultdict(dict))
    dfs_by_vertexs_searching: defaultdict[dict] = field(default_factory=lambda: defaultdict(dict))

    @property
    def vertex_searching_story(self) -> Dict:
        if not self._vertex_searching_story:
            self._vertex_searching_story = \
            {index: 0 for index in range(self.defined_maximum_vertex+1)}
        return self._vertex_searching_story

    def dfs_from_it(self) -> typing.GGE:
        self._sliced_graph.tree_topic = self
        return self._sliced_graph.dfs(vertex=self.defined_maximum_vertex)

    def find_the_rigth_tree_by_vertex_size(self, count=None, top=None):
        if not top:
            top = self._sliced_graph.tree_topic
        if not count:
            count = self.defined_maximum_vertex
        self.defined_maximum_vertex = count
        self._sliced_graph.tree_topic = top
        # TODO: FIRSTLY: change the concpetion of the fucntion and dfs for better and really usefull UX
        # TODO: FIRSTLY: _vertex_searching_story should be included in the logic of the conception
        for depth in self.vertex_searching_story.keys():
            self.defined_maximum_vertex = depth
            # But also the best count has two varients of the tree
            topic_of_best_tree_left = {count: top}
            topic_of_best_tree_right = {count: top}
            edges_lengths = len(self._sliced_graph) # the best tree has smallest count of edges\
            for element in self._sliced_graph:
                self._sliced_graph.tree_topic = element
                self._sliced_graph.tree_topic = top
                trees_elements, edges = self.dfs_from_it()
                size = len(trees_elements)
                if len(edges) < edges_lengths:
                    edges_lengths = len(edges)
                    topic_of_best_tree_right[count] = topic_of_best_tree_left[count]
                    topic_of_best_tree_left[count] = element
                yield size, depth, topic_of_best_tree_left, topic_of_best_tree_right
        self.defined_maximum_vertex = count
        self._sliced_graph.tree_topic = top


@dataclass
class StringByStringGraphMask(base.BaseGraphMask):

    ''' Sensetive turn off '''

    def exlude_tree(self) -> typing.Tree:
        '''
        Find the sequence which can work like a tree. Raise
        Vaildation Error if it has no any tree variant
        '''
        ids = {el.id for el in self.tree_topic.walk()}
        return VertexSearcingTree(self, ids)


class EisenhoverMatrixConvertationMask(StringByStringGraphMask):

    loader_class: typing.Loader = drivers.EisenhoverMatrixLoader

    def get_orthodox_eisenhover_info(self, index: int):
        part = self.loader.get_part_by_id(index)
        executive_id = index - self.loader.ids_map[part]
        return {'part': part, 'executive_id': executive_id}
