#!/usr/bin/env python

# tests/test_abstracts.py
import unittest
from typing import List, Dict

from lib.protocols import (
    AbstractLoader,
    AbstractTree,
    AbstractElement,
    AbstractGraphMask,
)


# -------------------------------
# Dummy implementations for tests
# -------------------------------

class DummyElement(AbstractElement):
    def __init__(self, id_: str):
        self._id = id_

    def __hash__(self): return hash(self._id)
    def __repr__(self): return f"<DummyElement {self._id}>"
    def __str__(self): return self._id

    @property
    def id(self): return self._id
    @property
    def part(self): return "part"
    @property
    def grouped(self): return "grouped"
    @property
    def body(self): return "body"
    @property
    def graph(self): return None
    @property
    def children(self): return []
    @property
    def parents(self): return []


class DummyLoader(AbstractLoader[DummyElement]):
    def __init__(self):
        self._elements = [DummyElement("1"), DummyElement("2")]

    @property
    def whole_chain(self): return self._elements
    @property
    def element_class(self): return DummyElement
    @property
    def chain_type(self): return list
    @property
    def ids(self): return frozenset(e.id for e in self._elements)
    @property
    def map(self): return {e.id: e for e in self._elements}

    def loads_from(self, path: str, type: str, mode: str = "r", starts: int = 0):
        return self._elements

    def convert_element(self, tmp: str):
        return DummyElement(tmp)

    def chain_mapping_function(self, *args, **kwargs):
        return [DummyElement("mapped")]

    def mapping_function(self, func, sequence):
        return [func(e) for e in sequence]


class DummyTree(AbstractTree[DummyElement]):
    def __init__(self):
        self._elements = {0: DummyElement("root")}

    def __getitem__(self, k): return self._elements[k]
    def __iter__(self): return iter(self._elements)
    def __len__(self): return len(self._elements)

    @property
    def longest_chain(self): return list(self._elements.values())
    @property
    def depth(self): return 1
    def dfs(self): return iter(self._elements.values())
    def top(self): return self._elements[0]
    def bfs(self): return iter(self._elements.values())


class DummyGraph(AbstractGraphMask[DummyElement]):
    def __init__(self):
        self._elements = [DummyElement("a"), DummyElement("b")]

    def __iter__(self): return iter(self._elements)
    def __len__(self): return len(self._elements)
    def __contains__(self, item): return item in self._elements

    def __repr__(self): return "<DummyGraph>"
    def __str__(self): return "graph"

    @property
    def separator(self): return ":"
    @property
    def file(self): return "dummy.txt"
    @property
    def element_class(self): return DummyElement

    def exclude_tree(self): return DummyTree()
    @property
    def tree_topic(self): return self._elements[0]


# -------------------
# Unit Tests
# -------------------

class TestAbstractLoader(unittest.TestCase):
    def setUp(self): self.loader = DummyLoader()

    def test_whole_chain(self):
        self.assertEqual(len(self.loader.whole_chain), 2)

    def test_ids(self):
        self.assertEqual(self.loader.ids, frozenset({"1", "2"}))

    def test_mapping_function(self):
        res = self.loader.mapping_function(lambda e: e.id, self.loader.whole_chain)
        self.assertEqual(res, ["1", "2"])

    def test_convert_element(self):
        el = self.loader.convert_element("42")
        self.assertIsInstance(el, DummyElement)
        self.assertEqual(el.id, "42")


class TestAbstractTree(unittest.TestCase):
    def setUp(self): self.tree = DummyTree()

    def test_depth(self):
        self.assertEqual(self.tree.depth, 1)

    def test_longest_chain(self):
        self.assertEqual([e.id for e in self.tree.longest_chain], ["root"])

    def test_top(self):
        self.assertEqual(self.tree.top().id, "root")


class TestAbstractElement(unittest.TestCase):
    def setUp(self): self.el = DummyElement("X")

    def test_str_and_repr(self):
        self.assertEqual(str(self.el), "X")
        self.assertIn("DummyElement", repr(self.el))

    def test_hash(self):
        self.assertEqual(hash(self.el), hash("X"))

    def test_properties(self):
        self.assertEqual(self.el.part, "part")
        self.assertEqual(self.el.grouped, "grouped")


class TestAbstractGraphMask(unittest.TestCase):
    def setUp(self): self.graph = DummyGraph()

    def test_len_and_contains(self):
        self.assertEqual(len(self.graph), 2)
        self.assertIn(self.graph._elements[0], self.graph)

    def test_separator_and_file(self):
        self.assertEqual(self.graph.separator, ":")
        self.assertEqual(self.graph.file, "dummy.txt")

    def test_exclude_tree(self):
        tree = self.graph.exclude_tree()
        self.assertIsInstance(tree, DummyTree)

    def test_tree_topic(self):
        self.assertEqual(self.graph.tree_topic.id, "a")

    def test_is_bipartite_default(self):
        self.assertFalse(self.graph.is_bipartite)


if __name__ == "__main__":
    unittest.main()
