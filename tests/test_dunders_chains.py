#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from lib.chains import BaseChain, TxtChain, GraphChain, EisenhowerMatrixChain, JSONChain


class TestBaseChain(unittest.TestCase):
    def setUp(self):
        self.data = [1, 2, 3, 4, 5]
        self.chain = BaseChain(self.data)

    # --- Iterator Engine ---
    def test_iterator_protocol(self):
        it = iter(self.chain)
        self.assertEqual(next(it), 1)
        self.assertEqual(next(it), 2)
        with self.assertRaises(StopIteration):
            for _ in range(len(self.data) - 2):
                next(it)
            next(it)

    def test_len_and_getitem(self):
        self.assertEqual(len(self.chain), 5)
        self.assertEqual(self.chain[0], 1)
        self.assertEqual(self.chain[-1], 5)

    def test_contains_and_equality(self):
        self.assertIn(3, self.chain)
        self.assertNotIn(99, self.chain)
        self.assertEqual(self.chain, BaseChain([1, 2, 3, 4, 5]))
        self.assertNotEqual(self.chain, BaseChain([2, 3]))

    # --- Functional Methods ---
    def test_map_doubles_values(self):
        mapped = self.chain.__map__(lambda x: x * 2)
        self.assertIsInstance(mapped, BaseChain)
        self.assertEqual(list(mapped), [2, 4, 6, 8, 10])

    def test_filter_evens(self):
        filtered = self.chain.__filter__(lambda x: x % 2 == 0)
        self.assertEqual(list(filtered), [2, 4])

    def test_reduce_sum(self):
        total = self.chain.__reduce__(lambda a, b: a + b)
        self.assertEqual(total, 15)

    def test_reduce_with_initializer(self):
        total = self.chain.__reduce__(lambda a, b: a + b, 10)
        self.assertEqual(total, 25)

    # --- Utilities ---
    def test_start_end_methods(self):
        self.assertEqual(self.chain.start(), 1)
        self.assertEqual(self.chain.end(), 5)

    def test_filtered_method(self):
        result = self.chain.filtered(lambda x: x > 3)
        self.assertEqual(list(result), [4, 5])

    def test_repr_hash_copy(self):
        rep = repr(self.chain)
        self.assertIn("BaseChain", rep)
        h = hash(self.chain)
        self.assertIsInstance(h, int)

        shallow = self.chain.__copy__()
        deep = self.chain.__deepcopy__({})
        self.assertEqual(shallow, deep)
        self.assertEqual(shallow, self.chain)

    def test_sizeof_returns_int(self):
        self.assertIsInstance(self.chain.__sizeof__(), int)


class TestTxtChain(unittest.TestCase):
    def test_store_blank_calls_eisenhower_splitter(self):
        # mock shortcuts.eisenhower_part_spliter
        import lib.shortcuts as shortcuts

        called = {}

        def mock_splitter(element):
            called['x'] = element
            return ('A1.', True)

        shortcuts.eisenhower_part_spliter = mock_splitter

        c = TxtChain(["A1.task"])
        c.whole_parts = {'A1.': 0, 'B2.': 0, 'C3.': 0, 'L4.': 0}
        c.increase_on = 1
        result = c.store_blank("A1.task")

        self.assertTrue(result)
        self.assertIn("x", called)
        self.assertEqual(c.whole_parts["A1."], 1)


class TestEisenhowerMatrixChain(unittest.TestCase):
    def test_skip_blank_behavior(self):
        c = EisenhowerMatrixChain(["Task 1", "Task 2"])
        self.assertFalse(c.skip_blank("anything"))


class TestGraphChain(unittest.TestCase):
    def test_graphchain_placeholder_behavior(self):
        # Since graph structure isn't fully implemented, just ensure init and props
        g = GraphChain([1, 2, 3])
        self.assertIsInstance(g, GraphChain)
        self.assertTrue(hasattr(g, "_cache"))


class TestJSONChain(unittest.TestCase):
    def test_jsonchain_instantiation(self):
        j = JSONChain([{"a": 1}, {"b": 2}])
        self.assertIsInstance(j, JSONChain)
        self.assertEqual(len(j), 2)


if __name__ == "__main__":
    unittest.main()
