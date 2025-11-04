#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from lib.base.masks import NodeWhitelistMask, EdgeWeightMask, CompositeMask


class TestNodeWhitelistMask(unittest.TestCase):

    def test_allows_only_listed_nodes(self):
        mask = NodeWhitelistMask(["A", "B"])
        self.assertTrue(mask.allow_node("A"))
        self.assertTrue(mask.allow_node("B"))
        self.assertFalse(mask.allow_node("C"))

    def test_edges_are_not_filtered(self):
        mask = NodeWhitelistMask(["A"])
        self.assertTrue(mask.allow_edge("A", "B"))
        self.assertTrue(mask.allow_edge("X", "Y"))


class TestEdgeWeightMask(unittest.TestCase):

    def setUp(self):
        self.weights = {
            ("A", "B"): 5,
            ("A", "C"): 2,
            ("B", "D"): 10
        }

    def test_edges_above_threshold_are_allowed(self):
        mask = EdgeWeightMask(min_weight=5, weights=self.weights)
        self.assertTrue(mask.allow_edge("A", "B"))  # weight 5
        self.assertTrue(mask.allow_edge("B", "D"))  # weight 10

    def test_edges_below_threshold_are_filtered(self):
        mask = EdgeWeightMask(min_weight=5, weights=self.weights)
        self.assertFalse(mask.allow_edge("A", "C"))  # weight 2
        self.assertFalse(mask.allow_edge("X", "Y"))  # missing → inf

    def test_nodes_are_never_filtered(self):
        mask = EdgeWeightMask(min_weight=5, weights=self.weights)
        self.assertTrue(mask.allow_node("A"))
        self.assertTrue(mask.allow_node("Z"))


class TestCompositeMask(unittest.TestCase):

    def test_node_and_edge_conditions_must_both_pass(self):
        node_mask = NodeWhitelistMask(["A", "B"])
        edge_mask = EdgeWeightMask(min_weight=5, weights={("A", "B"): 5, ("A", "C"): 1})
        composite = CompositeMask(node_mask, edge_mask)

        # Node B is allowed by node mask, and edge (A,B) passes weight
        self.assertTrue(composite.allow_node("B"))
        self.assertTrue(composite.allow_edge("A", "B"))

        # Node C blocked by node mask
        self.assertFalse(composite.allow_node("C"))

        # Edge (A,C) blocked by edge mask
        self.assertFalse(composite.allow_edge("A", "C"))


if __name__ == "__main__":
    unittest.main()
