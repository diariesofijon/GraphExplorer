#!/usr/bin/env python
# pylint: disable=C0103,W0622,E1136

'''
    Loads graph from a file as a text through regexp
'''

# fix: find another way to find points of graph due pythonic RegExp
# import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional, List, Union, Iterable, FrozenSet, Dict

import config
import drivers
from base import (
    StringRegularExpressionMaskAbstract, GE, GGE, GM, Tree,
    RepresentativeGraphElementAbstract, GraphTreeRepresintationMaskAbstract)


__all__ = (
    'RepresentativeGraphElementMask', 'StringByStringRegularExpressionMask')

# https://www.javatpoint.com/bfs-vs-dfs#:~:text=DFS%20stands%20for%20Depth%20First,Last%20In%20First%20Out)%20principle


@dataclass
class RepresentativeGraphElementMask(RepresentativeGraphElementAbstract):

    ''' Sensetive turn off '''

    id: str = ''
    part: str = ''
    grouped: str = ''
    body: str = ''
    graph: StringRegularExpressionMaskAbstract = None
    separater_key: str = 'NODE'

    def __str__(self):
        return f'{self.part} id: {self.id} = {self.grouped} - {self.body}'

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return self.id # TODO: have to use hasheable function instead

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

    def _separeter(self):
        return config.SEPARATES.get(self.separater_key, self.graph.separeter)

@dataclass
class VertexInfo:

    # TODO: LETS METACLASS IDICATE VERTEXTINFO DUPLICATES

    graph: Tree = None
    start: RepresentativeGraphElementMask = None
    end: RepresentativeGraphElementMask = None
    depth: int = 0

    def validation(self):
        ''' Have to explain why the Tree could not exists '''
        if not (self.graph and self.start and self.end):
            raise config.ValidationError
        if self.depth and self.start is self.end:
            raise config.ValidationError


@dataclass
class GraphTreeRepresentationMask(GraphTreeRepresintationMaskAbstract):

    ''' Frozen Tree '''

    _sliced_graph: GM = None
    # TODO: find the way of searching elements by a hash
    element_ids: FrozenSet[int] = None
    defined_maximum_vertex: int = 5
    trees_validated_vertex_left: VertexInfo = None
    trees_validated_vertex_right: VertexInfo = None
    _vertex_searching_story: defaultdict[dict] = field(default_factory=lambda: defaultdict(dict))
    dfs_by_vertexs_searching: defaultdict[dict] = field(default_factory=lambda: defaultdict(dict))


    def __iter__(self) -> GGE:
        return iter(self[_id] for _id in self.element_ids)

    def __len__(self) -> int:
        return len(list(self[_id] for _id in self.element_ids))

    def __str__(self) -> str:
        return str(self._sliced_graph + ' Tree')

    def __repr__(self) -> str:
        return self.__str__()

    def __getitem__(self, key: int) -> GE:
        if key not in self.element_ids:
            raise config.OutFromTreeError
        return self._sliced_graph[key]

    def __contains__(self, element: GE) -> bool:
        return element.id in self.element_ids

    @property
    def vertex_searching_story(self) -> Dict:
        if not self._vertex_searching_story:
            self._vertex_searching_story = \
            {index: 0 for index in range(self.defined_maximum_vertex+1)}
        return self._vertex_searching_story

    @property
    def depth(self) -> int:
        ''' The deepth of the graph '''
        # fix: make deep searching algorithm based on this property
        return self.bfs()[0]

    @property
    def longest_chain(self) -> Iterable[int]:
        ''' The logest chain to iterate through the DFS algorithm '''
        return self.bfs()

    def dfs_from_it(self) -> GGE:
        self._sliced_graph.tree_topic = self
        return self._sliced_graph.dfs(vertex=self.defined_maximum_vertex)

    def bfs(self) -> GGE:
        # TODO: let's make something similart with dfs has done
        pass

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
class StringByStringRegularExpressionMask(StringRegularExpressionMaskAbstract):

    ''' Sensetive turn off '''

    # TODO: move it to an another class like composition
    # element_mask: Optional[str] = r'.+(?P<id>\D+)\..?(?P<grouped>.+): (?P<body>.*)\n'
    # node_mask: Optional[str] = r'(?P<id>\D+)\((?P<children_list>.*)\)'
    # part_mask: Optional[str] = r'.*(?P<id>\S+\D+\).\n'
    tmp: Optional[str] = None
    separeter: str = config.SEPARATES.get('NODE')
    file: str = config.FILE_DATA_LOADER_PATH
    loader_class: drivers.AbstractLoader = drivers.EisenhoverMatrixLoader
    element_class: GE = RepresentativeGraphElementMask

    def __iter__(self) -> GGE:
        return iter(self._get_formated_links())

    def __len__(self) -> int:
        return len(list(self._get_formated_links()))

    def __str__(self) -> str:
        return self.separeter.join(str(tmp) for tmp in iter(self))

    def __repr__(self) -> str:
        return self.__str__()

    def __getitem__(self, key: int) -> GE:
        # TODO: place awqay the validation
        # don't forget that it question about error arised in the same place that
        # have be corrected instead of doing in another way like done bellow
        if isinstance(key, RepresentativeGraphElementMask):
            key = key.id
        # TODO: It have be removed from logic because it have work unrelated to the data
        last_part = 'A1.'
        for part in self.ids_map:
            if len(self.ids_map[last_part]) > key:
                last_part = part
        return self.get_element(part=last_part, id=key)


    def __contains__(self, element: GE) -> bool:
        try:
            element = self.get_element(element.part, element.id)
        except IndexError:
            return False
        return isinstance(element, self.element_class)

    def _get_formated_links(self):
        for link in self.tmp.split(self.separeter):
            if (tmp := link.strip()).endswith('.'):
                self._last_part = tmp
                continue
            if not tmp:
                # ATTENTION: ignore blank line
                continue
            yield from self._convert_element(tmp, self._last_part)

    def get_elements(self, part: str =None, id: Union[str, int] =None) -> GE:
        if not id and not part:
            raise IndexError()
        if not part:
            # fix: it would be good idea if we can search only by id???
            raise IndexError('Part has not defined when id was passed')
        if id and part:
            yield from (el for el in self if el.part == part and el.id == id)

    def get_element(self, part: str =None, id: Union[str, int] =None) -> GE:
        # TODO: refactor the idea of methods get_element and get_elements
        for element in self.ids_map[part]:
            # TODO: trouble with int has not solved just converted in ty exctention
            # TODO: it has not work due exclude_tree ids_map has defrent logic
            try:
                if element.id == id:
                    return element
            except:
                return element
        # TODO: add the explanation of the trouble
        raise IndexError()

    # TODO: refactor it
    _topic = None

    @property
    def tree_topic(self) -> GE:
        ''' Highest element in the biggest tree of the graph '''
        if not self._topic:
            self._topic = list(self)[0]
        return self._topic # TODO: make magic algortihm which return the top of the biggest tree

    @tree_topic.setter
    def tree_topic(self, element: GE) -> GE:
        ''' Highest element in the biggest tree of the graph '''
        # if isinstance(element, RepresentativeGraphElementMask):
        #     self._topic = element
        # raise config.ValidationError
        self._topic = element

    def exlude_tree(self) -> Tree:
        '''
        Find the sequence which can work like a tree. Raise
        Vaildation Error if it has no any tree variant
        '''
        print(type(self.tree_topic))
        print(self.tree_topic)
        ids = {el.id for el in self.tree_topic.walk()}
        return GraphTreeRepresentationMask(self, ids)

    def dfs(self, vertex = 5) -> GGE:
        # TODO: should to work in the composition way
        # maxdepth = 0
        visited = []
        queue = []
        visited.append(self.tree_topic)
        queue.append((self.tree_topic,1))
        while queue:
            x, depth = queue.pop(0)
            # TODO: take down documentation about the idea why should we use already defined maxdepth
            # maxdepth = max(maxdepth, deptsh)
            # print(x)
            if depth > vertex:
                break
            for child in self[x].children:
                if child not in visited:
                    visited.append(child)
                    queue.append((child,depth+1))
        return queue, visited
