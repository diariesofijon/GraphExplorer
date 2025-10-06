#!/usr/bin/env python

import unittest
import copy
import sys

from lib.protocols import (
    AbstractChain,
    AbstractLoader,
    AbstractTree,
    AbstractElement,
    AbstractTextFormatter,
)


# ------------------------------
# Mock Implementations for Test
# ------------------------------

class DummyChain(AbstractChain):
    @property
    def blank(self):
        return False

    def filtered(self, func):
        return [x for x in self if func(x)]


class DummyLoader(AbstractLoader):
    @property
    def whole_chain(self): return [1, 2]

    @property
    def element_class(self): return int

    @property
    def chain_type(self): return list

    @property
    def ids(self): return frozenset([1, 2])

    @property
    def map(self): return {1: "a", 2: "b"}

    def loads_from(self, path, type="r", mode="r", starts=0): return path

    def convert_element(self, tmp): return int(tmp)

    def chain_mapping_fuction(self, *args, **kwargs): return args

    def mapping_fuction(self, func, sequence): return list(map(func, sequence))


class DummyTree(AbstractTree):
    @property
    def longest_chain(self): return [1, 2, 3]

    @property
    def depth(self): return 3

    def dfs(self): return [1, 2, 3]

    def top(self): return 1

    def bfs(self): return [1, 2, 3]

    def __iter__(self): yield from [1, 2, 3]
    def __getitem__(self, k): return [1, 2, 3][k]
    def __len__(self): return 3


class DummyElement(AbstractElement):
    @property
    def id(self): return "X1"

    @property
    def part(self): return "A"

    @property
    def grouped(self): return "G"

    @property
    def body(self): return "Hello"

    @property
    def graph(self): return None

    @property
    def children(self): return []

    @property
    def parents(self): return []

    def __hash__(self): return hash(self.id)

    def __repr__(self): return f"<DummyElement id={self.id}>"

    def __str__(self): return f"Element({self.id})"


class DummyFormatter(AbstractTextFormatter):
    def format(self, text: str) -> str: return text.strip()
    def mask(self, kind): return f"mask:{kind}"


# ------------------------------
# Tests
# ------------------------------

class TestDunders(unittest.TestCase):

    def test_chain_dunders(self):
        c1 = DummyChain([1, 2])
        c2 = DummyChain([1, 2])
        self.assertEqual(c1, c2)
        self.assertEqual(hash(c1), hash(c2))
        self.assertIn("DummyChain", repr(c1))
        self.assertIn("Chain", str(c1))
        self.assertGreater(sys.getsizeof(c1), 0)
        self.assertEqual(copy.copy(c1), c1)
        self.assertEqual(copy.deepcopy(c1), c1)

    def test_loader_dunders(self):
        l1 = DummyLoader()
        l2 = DummyLoader()
        self.assertEqual(l1, l2)
        self.assertEqual(hash(l1), hash(l2))
        self.assertIn("Loader", str(l1))
        self.assertIn("DummyLoader", repr(l1))
        self.assertGreater(sys.getsizeof(l1), 0)
        self.assertEqual(copy.copy(l1).map, l1.map)
        self.assertEqual(copy.deepcopy(l1).map, l1.map)

    def test_tree_dunders(self):
        t1 = DummyTree()
        t2 = DummyTree()
        self.assertEqual(t1, t2)
        self.assertEqual(hash(t1), hash(t2))
        self.assertIn("Tree", str(t1))
        self.assertIn("DummyTree", repr(t1))
        self.assertGreater(sys.getsizeof(t1), 0)

    def test_element_dunders(self):
        e1 = DummyElement()
        e2 = DummyElement()
        self.assertEqual(e1, e2)
        self.assertEqual(hash(e1), hash(e2))
        self.assertIn("DummyElement", repr(e1))
        self.assertIn("Element", str(e1))
        self.assertGreater(sys.getsizeof(e1), 0)

    def test_formatter_dunders(self):
        f1 = DummyFormatter()
        f2 = DummyFormatter()
        self.assertEqual(f1, f2)
        self.assertEqual(hash(f1), hash(f2))
        self.assertIn("Formatter", str(f1))
        self.assertIn("DummyFormatter", repr(f1))


if __name__ == "__main__":
    unittest.main()
