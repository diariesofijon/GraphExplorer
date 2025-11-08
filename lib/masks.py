#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TODO: move it to an another class like composition
# element_mask: Optional[str] = r'.+(?P<id>\D+)\..?(?P<grouped>.+): (?P<body>.*)\n'
# node_mask: Optional[str] = r'(?P<id>\D+)\((?P<children_list>.*)\)'
# part_mask: Optional[str] = r'.*(?P<id>\S+\D+\).\n'

'''
Docs Section
# TODO: #25 explain the idea of masks
'''

from typing import Optional

from bin.protocols import MaskProtocol


class NoMask(MaskProtocol):

    def allow_node(self, node):
        return True

    def allow_edge(self, u, v):
        return True


class NodeWhitelistMask(MaskProtocol):

    def __init__(self, allowed_nodes: set[str]):
        self.allowed = set(allowed_nodes)

    def allow_node(self, node):
        return node in self.allowed

    def allow_edge(self, u, v):
        return True


class EdgeWeightMask(MaskProtocol):

    def __init__(self, min_weight: float, weights: dict[tuple[str,str], float]):
        self.min_weight = min_weight
        self.weights = weights

    def allow_node(self, node):
        return True

    def allow_edge(self, u, v):
        # TODO: make access by the hash of them
        return self.weights.get((u, v), float('-inf')) >= self.min_weight


class CompositeMask(MaskProtocol):

    def __init__(self, *masks: MaskProtocol):
        self.masks = masks

    def allow_node(self, node):
        return all(m.allow_node(node) for m in self.masks)

    def allow_edge(self, u, v):
        return all(m.allow_edge(u, v) for m in self.masks)


class RegExpMask(MaskProtocol):
    pass
