#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stress test for recursive depth and balanced-tree graph serialization.

Run with:
    RUN_STRESS=1 python -m unittest tests.test_performance_tree_depth -v
"""
import os
import time
import unittest
import tracemalloc
from lib.graph import Graph
from lib.graph_elements import Element
from lib.functional_json import to_json_data, from_json_data

RUN_STRESS = os.getenv("RUN_STRESS", "0") == "1"
DEPTH = int(os.getenv("STRESS_DEPTH", "10"))          # recursion depth
BRANCH = int(os.getenv("STRESS_BRANCH", "3"))         # branching factor
TIME_LIMIT = float(os.getenv("STRESS_TIME_LIMIT", "15.0"))
MEM_LIMIT_MB = float(os.getenv("STRESS_MEM_LIMIT_MB", "400.0"))


def build_balanced_tree(graph, parent, depth, branch):
    """Recursively build a balanced tree graph of given depth and branching."""
    if depth == 0:
        return
    for i in range(branch):
        child = Element(f"{parent.id}-{i}")
        graph.add_edge(parent, child)
        build_balanced_tree(graph, child, depth - 1, branch)


@unittest.skipUnless(RUN_STRESS, "Tree stress tests disabled (RUN_STRESS=1 to enable)")
class TestGraphTreeDepth(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.root = Element("root")
        self.graph.add_node(self.root)
        build_balanced_tree(self.graph, self.root, DEPTH, BRANCH)

    def test_recursive_serialization_stability(self):
        tracemalloc.start()
        t0 = time.perf_counter()
        json_data = to_json_data(self.graph)
        roundtrip_graph = from_json_data(json_data)
        t1 = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peak_mb = peak / 1024 / 1024
        elapsed = t1 - t0

        self.assertLessEqual(elapsed, TIME_LIMIT, f"Took too long: {elapsed:.2f}s")
        self.assertLessEqual(peak_mb, MEM_LIMIT_MB, f"Too much memory: {peak_mb:.1f}MB")
        self.assertIsNotNone(roundtrip_graph)
        print(f"\nTree depth={DEPTH}, branch={BRANCH}, time={elapsed:.2f}s, mem={peak_mb:.1f}MB")


if __name__ == "__main__":
    unittest.main()

