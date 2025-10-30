#!/usr/bin/env python

import unittest
import copy

from lib.chains import (
    BaseChain,
    TxtChain,
    GraphChain,
    EisenhowerMatrixChain,
    JSONChain,
)


class TestBaseChain(unittest.TestCase):

    def setUp(self):
        self.sample_data = [1, 2, 3, 2]
        self.chain = BaseChain(self.sample_data)

    def test_initialization_and_uniqueness(self):
        """Should remove duplicates while preserving order"""
        chain = BaseChain(self.sample_data, unique=True)
        self.assertEqual(list(chain), [1, 2, 3])

    def test_getitem_len_iter(self):
        """Should behave like pythonic list"""
        self.assertEqual(self.chain[0], 1)
        self.assertEqual(len(self.chain), 3)
        self.assertListEqual(list(self.chain), [1, 2, 3])

    def test_contains(self):
        """Membership check must work"""
        self.assertIn(2, self.chain)
        self.assertNotIn(5, self.chain)

    def test_dunders_str_and_repr(self):
        """Should return meaningful string representations"""
        self.assertIn("Chain", str(self.chain))
        self.assertIn("BaseChain", repr(self.chain))

    def test_eq_and_hash(self):
        """Equality and hashing by data"""
        same = BaseChain([1, 2, 3])
        diff = BaseChain([9, 9])
        self.assertEqual(self.chain, same)
        self.assertNotEqual(self.chain, diff)
        self.assertEqual(hash(self.chain), hash(same))

    def test_copy_and_deepcopy(self):
        """__copy__ and __deepcopy__ should return new independent instances"""
        shallow_copy = copy.copy(self.chain)
        deep_copy = copy.deepcopy(self.chain)
        self.assertIsInstance(shallow_copy, BaseChain)
        self.assertIsInstance(deep_copy, BaseChain)
        self.assertEqual(self.chain, deep_copy)

    def test_start_and_end(self):
        """start() and end() should access first and last elements"""
        self.assertEqual(self.chain.start(), 1)
        self.assertEqual(self.chain.end(), 3)

    def test_filtered(self):
        """filtered() should return a new Chain filtered by predicate"""
        filtered_chain = self.chain.filtered(lambda x: x > 1)
        self.assertEqual(list(filtered_chain), [2, 3])

    def test_skip_blank_and_store_blank(self):
        """Default blank behavior"""
        self.assertTrue(self.chain.skip_blank("data"))
        self.assertTrue(self.chain.store_blank("data"))


class TestTxtChain(unittest.TestCase):

    def test_store_blank_uses_shortcuts(self):
        """TxtChain.store_blank() must return bool and call shortcuts"""
        txt = TxtChain(["A1. task"])
        # mock eisenhower_part_spliter
        from lib import shortcuts

        # TODO: there is the mock, but the function has undetectable behavior
        shortcuts.eisenhower_part_spliter = lambda x: ("A1.", True)
        txt.whole_parts = {"A1.": 0}
        txt.increase_on = 1
        result = txt.store_blank("A1. task")
        self.assertTrue(result)
        self.assertEqual(txt.whole_parts["A1."], 1)


class TestGraphChain(unittest.TestCase):

    def test_properties_placeholder(self):
        """Test the property placeholders behave safely"""
        gchain = GraphChain([])
        # mock its graph
        class DummyGraph:
            def dfs(self):
                return (["u1", "u2"], ["v1", "v2"])

        gchain.graph = DummyGraph()
        self.assertIsInstance(gchain.unconnected_chain, GraphChain)
        self.assertIsInstance(gchain.deepest_chain, GraphChain)


class TestEisenhowerMatrixChain(unittest.TestCase):

    def test_skip_blank_inverts_flag(self):
        chain = EisenhowerMatrixChain()
        chain.blank = False
        self.assertTrue(chain.skip_blank("X"))
        chain.blank = True
        self.assertFalse(chain.skip_blank("X"))


class TestJSONChain(unittest.TestCase):

    def test_inherits_graphchain(self):
        """JSONChain should still be subclass of GraphChain"""
        jchain = JSONChain()
        self.assertIsInstance(jchain, GraphChain)


if __name__ == "__main__":
    unittest.main()
