#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Integration-level tests for utils.py.
Covers functional serialization/deserialization of Element, Graph, and JSONChain.
"""

import io
import json
import tempfile
import unittest
from pathlib import Path

# Core imports
from elements import Element
from graph import Graph
from lib.chains import JSONChain
from lib.utils import (
    serialize_element,
    serialize_graph,
    serialize_chain,
    deserialize_element,
    deserialize_graph,
    deserialize_chain,
    to_json_data,
    from_json_data,
    store_json,
    load_json,
)


class TestUtilsFunctional(unittest.TestCase):
    """Functional-level tests for serialization and deserialization."""

    def setUp(self):
        # Basic test elements and graph
        self.e1 = Element("A", meta={"color": "red"})
        self.e2 = Element("B", meta={"color": "blue"})
        self.graph = Graph(directed=True)
        self.graph.add_edge(self.e1, self.e2)
        self.chain = JSONChain(self.graph)

    # --- Element Tests ---

    def test_serialize_element(self):
        data = serialize_element(self.e1)
        self.assertEqual(data["type"], "Element")
        self.assertEqual(data["name"], "A")
        self.assertIn("meta", data)
        self.assertEqual(data["meta"]["color"], "red")

    def test_deserialize_element(self):
        data = {"type": "Element", "name": "C", "meta": {"shape": "circle"}}
        el = deserialize_element(data)
        self.assertIsInstance(el, Element)
        self.assertEqual(el.name, "C")
        self.assertEqual(el.meta["shape"], "circle")

    # --- Graph Tests ---

    def test_serialize_graph(self):
        data = serialize_graph(self.graph)
        self.assertEqual(data["type"], "Graph")
        self.assertTrue(data["directed"])
        self.assertIn("edges", data)
        self.assertEqual(len(data["edges"]), 1)
        edge = data["edges"][0]
        self.assertEqual(edge["parent"]["name"], "A")
        self.assertEqual(edge["child"]["name"], "B")

    def test_deserialize_graph(self):
        data = serialize_graph(self.graph)
        g = deserialize_graph(data)
        self.assertIsInstance(g, Graph)
        self.assertEqual(len(list(g.edges())), 1)
        u, v = next(iter(g.edges()))
        self.assertEqual(u.name, "A")
        self.assertEqual(v.name, "B")

    # --- JSONChain Tests ---

    def test_serialize_chain(self):
        data = serialize_chain(self.chain)
        self.assertEqual(data["type"], "JSONChain")
        self.assertIn("graph", data)
        self.assertIn("edges", data["graph"])

    def test_deserialize_chain(self):
        data = serialize_chain(self.chain)
        c = deserialize_chain(data)
        self.assertIsInstance(c, JSONChain)
        self.assertIsInstance(c.graph, Graph)

    # --- Universal Dispatcher Tests ---

    def test_to_json_data_dispatch(self):
        for obj in (self.e1, self.graph, self.chain):
            data = to_json_data(obj)
            self.assertIn("type", data)

    def test_from_json_data_dispatch(self):
        e = from_json_data(to_json_data(self.e1))
        g = from_json_data(to_json_data(self.graph))
        c = from_json_data(to_json_data(self.chain))
        self.assertIsInstance(e, Element)
        self.assertIsInstance(g, Graph)
        self.assertIsInstance(c, JSONChain)

    def test_from_json_data_invalid_type(self):
        with self.assertRaises(ValueError):
            from_json_data({"type": "Unknown"})

    def test_to_json_data_invalid_type(self):
        with self.assertRaises(TypeError):
            to_json_data(object())

    # --- File-based Tests ---

    def test_store_and_load_json(self):
        tmp = Path(tempfile.gettempdir()) / "test_chain.json"
        store_json(self.chain, tmp)
        self.assertTrue(tmp.exists())
        loaded = load_json(tmp)
        self.assertIsInstance(loaded, JSONChain)
        self.assertEqual(len(list(loaded.graph.edges())), 1)
        tmp.unlink(missing_ok=True)

    def test_json_round_trip_integrity(self):
        """Ensure that serialization -> JSON -> deserialization preserves structure."""
        buf = io.StringIO()
        json.dump(to_json_data(self.chain), buf)
        buf.seek(0)
        restored = from_json_data(json.load(buf))
        self.assertEqual(len(list(restored.graph.edges())), len(list(self.chain.graph.edges())))


# --- Optional Performance/Stress Test ---

class TestUtilsPerformance(unittest.TestCase):
    """Stress test with large graph serialization."""

    def test_large_graph_serialization(self):
        g = Graph(directed=True)
        nodes = [Element(str(i)) for i in range(1000)]
        for i in range(999):
            g.add_edge(nodes[i], nodes[i+1])
        chain = JSONChain(g)
        data = serialize_chain(chain)
        self.assertEqual(len(data["graph"]["edges"]), 999)


if __name__ == "__main__":
    unittest.main(verbosity=2)
