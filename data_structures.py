#!/usr/bin/env python
# pylint: disable=C0103,W0622,E1136

'''
    Loads graph from a file as a text through regexp
'''

# fix: find another way to find points of graph due pythonic RegExp
# import re
from dataclasses import dataclass
from typing import Optional, List, Union, Iterable, FrozenSet

import config
from base import (
    StringRegularExpressionMaskAbstract, GE, GGE, GM, Tree,
    RepresentativeGraphElementAbstract, GraphTreeRepresintationMaskAbstract)


__all__ = (
    'RepresentativeGraphElementMask', 'StringByStringRegularExpressionMask')

# https://www.javatpoint.com/bfs-vs-dfs#:~:text=DFS%20stands%20for%20Depth%20First,Last%20In%20First%20Out)%20principle

#Python program for Depth First Traversal
MAX = 5
class Vertex:
    def __init__(self, label):
        self.label = label
        self.visited = False
#stack variables
stack = []
top = -1
#graph variables
#array of vertices
lstVertices = [None] * MAX
#adjacency matrix
adjMatrix = [[0] * MAX for _ in range(MAX)]
#vertex count
vertexCount = 0
#stack functions
def push(item):
    global top
    top += 1
    stack.append(item)
def pop():
    global top
    item = stack[top]
    del stack[top]
    top -= 1
    return item
def peek():
    return stack[top]
def isStackEmpty():
    return top == -1
#graph functions
#add vertex to the vertex list
def addVertex(label):
    global vertexCount
    vertex = Vertex(label)
    lstVertices[vertexCount] = vertex
    vertexCount += 1
#add edge to edge array
def addEdge(start, end):
    adjMatrix[start][end] = 1
    adjMatrix[end][start] = 1
#Display the Vertex
def displayVertex(vertexIndex):
    print(lstVertices[vertexIndex].label, end=' ')
def getAdjUnvisitedVertex(vertexIndex):
    for i in range(vertexCount):
        if adjMatrix[vertexIndex][i] == 1 and not lstVertices[i].visited:
            return i
    return -1
def depthFirstSearch():
    lstVertices[0].visited = True
    displayVertex(0)
    push(0)
    while not isStackEmpty():
        unvisitedVertex = getAdjUnvisitedVertex(peek())
        if unvisitedVertex == -1:
            pop()
        else:
            lstVertices[unvisitedVertex].visited = True
            displayVertex(unvisitedVertex)
            push(unvisitedVertex)
    for i in range(vertexCount):
        lstVertices[i].visited = False
for i in range(MAX):
    for j in range(MAX):
        adjMatrix[i][j] = 0
addVertex('S')   # 0
addVertex('A')   # 1
addVertex('B')   # 2
addVertex('C')   # 3
addVertex('D')   # 4
addEdge(0, 1)    # S - A
addEdge(0, 2)    # S - B
addEdge(0, 3)    # S - C
addEdge(1, 4)    # A - D
addEdge(2, 4)    # B - D
addEdge(3, 4)    # C - D
print("Depth First Search:", end=' ')
depthFirstSearch()


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
            return self
        next_el = self.children[index] if left else self.children.end(index)
        yield next_el
        # fix: make deep searching algorithm based on this property
        yield from next_el.walk(left=left, chain=chain)

    def _separeter(self):
        return config.SEPARATES.get(self.separater_key, self.graph.separeter)

@dataclass
class GraphTreeRepresentationMask(GraphTreeRepresintationMaskAbstract):

    ''' Frozen Tree '''

    _sliced_graph: GM = None
    # TODO: find the way of searching elements by a hash
    element_ids: FrozenSet[int] = None

    def __iter__(self) -> GGE:
        return iter(self[_id] for _id in self.element_ids)

    def __len__(self) -> int:
        return len(list(self[_id] for _id in self.element_ids))

    def __str__(self) -> str:
        return str(self._sliced_graph + ' Tree')

    def __repr__(self) -> str:
        return self.__str__()

    def __getitem__(self, key: int, pythonic_list: bool = True) -> GE:
        if key not in self.element_ids:
            raise config.OutFromTreeError
        return self._sliced_graph[key]

    def __contains__(self, element: GE) -> bool:
        return element.id in self.element_ids

    @property
    def depth(self) -> int:
        ''' The deepth of the graph '''
        # fix: make deep searching algorithm based on this property
        return self.bfs()[0]

    @property
    def longest_chain(self) -> Iterable[int]:
        ''' The logest chain to iterate through the DFS algorithm '''
        return self.bfs()[1]

    def dfs(self) -> GGE:
        # TODO: should to work in the composition way
        maxdepth = 0
        visited = []
        queue = []
        visited.append(self._sliced_graph.tree_topic)
        queue.append((self._sliced_graph.tree_topic,1))
        while queue:
            x, depth = queue.pop(0)
            maxdepth = max(maxdepth, depth)
            # print(x)
            for child in self._sliced_graph[x].children:
                if child not in visited:
                    visited.append(child)
                    queue.append((child,depth+1))
        return maxdepth, map(lambda x: x.id, visited)

    def bfs(self) -> GGE:
        pass

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
    last_part: str = 'A1.'
    element_class: GE = RepresentativeGraphElementMask

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.tmp:
            with open(self.file, 'r', encoding='utf8') as file:
                self.tmp: str = file.read()
        # TODO: it worth but i have to load self.ids_map
        for _ in self:
            continue

    def __iter__(self) -> GGE:
        return iter(self._get_formated_links())

    def __len__(self) -> int:
        return len(list(self._get_formated_links()))

    def __str__(self) -> str:
        return self.separeter.join(str(tmp) for tmp in iter(self))

    def __repr__(self) -> str:
        return self.__str__()

    def __getitem__(self, key: int, pythonic_list: bool = True) -> GE:
        if pythonic_list:
            return tuple(self)[key]
        for part, _id in self.ids_map:
            if key <= _id:
                return self.get_element(part, key)
            key -= _id
            continue
        raise IndexError()

    def __contains__(self, element: GE) -> bool:
        try:
            element = self.get_element(element.part, element.id)
        except IndexError:
            return False
        return isinstance(element, self.element_class)

    def _get_formated_links(self):
        for link in self.tmp.split(self.separeter):
            if (tmp := link.strip()).endswith('.'):
                self.last_part = tmp
                continue
            if not tmp:
                # ATTENTION: ignore blank line
                continue
            yield from self._convert_element(tmp, self.last_part)

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
        for key, value in self.ids_map.items():
            if key == part:
                break
            id += value
        # TODO: sequence of keis have to start from zero indstead of one
        return self[id-1]

    @property
    def tree_topic(self) -> GE:
        ''' Highest element in the biggest tree of the graph '''
        return self[0] # TODO: make magic algortihm which return the top of the biggest tree

    def exlude_tree(self) -> Tree:
        '''
        Find the sequence which can work like a tree. Raise
        Vaildation Error if it has no any tree variant
        '''
        ids = {el.id for el in self.tree_topic.walk()}
        return GraphTreeRepresentationMask(self, ids)
