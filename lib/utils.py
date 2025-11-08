#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0103,E0401,R0903

import json
from typing import Any, Dict, List, Callable, Type

# Assume these are already defined in your codebase:
from elements import Element
from graph import Graph
from lib.chains import JSONChain


# --- Pure Functional Serializers ---

def serialize_element(el: Element) -> Dict[str, Any]:
    """Functional: element -> dict."""
    return {
        "type": "Element",
        "name": el.name,
        "meta": getattr(el, "meta", {}),
    }


def serialize_graph(graph: Graph) -> Dict[str, Any]:
    """Functional: graph -> dict (no side effects)."""
    return {
        "type": "Graph",
        "directed": graph.directed,
        "weighted": getattr(graph, "weighted", False),
        "edges": [
            {
                "parent": serialize_element(u),
                "child": serialize_element(v),
                "weight": w if hasattr(graph, "weighted") and graph.weighted else None,
            }
            for (u, v, *maybe_w) in graph.edges(data=True)
            for w in [maybe_w[0] if maybe_w else None]
        ],
    }


def serialize_chain(chain: JSONChain) -> Dict[str, Any]:
    """Functional: chain -> dict."""
    return {
        "type": "JSONChain",
        "graph": serialize_graph(chain.graph),
    }


# --- Pure Functional Deserializers ---

def deserialize_element(data: Dict[str, Any]) -> Element:
    return Element(data["name"], **data.get("meta", {}))


def deserialize_graph(data: Dict[str, Any]) -> Graph:
    g = Graph(directed=data.get("directed", True))
    for e in data["edges"]:
        parent = deserialize_element(e["parent"])
        child = deserialize_element(e["child"])
        if e.get("weight") is not None:
            g.add_edge(parent, child, weight=e["weight"])
        else:
            g.add_edge(parent, child)
    return g


def deserialize_chain(data: Dict[str, Any]) -> JSONChain:
    g = deserialize_graph(data["graph"])
    return JSONChain(g)


# --- Functional Interface (Public API) ---

def to_json_data(obj: Any) -> Dict[str, Any]:
    """Universal serializer dispatch."""
    if isinstance(obj, JSONChain):
        return serialize_chain(obj)
    elif isinstance(obj, Graph):
        return serialize_graph(obj)
    elif isinstance(obj, Element):
        return serialize_element(obj)
    else:
        raise TypeError(f"Unsupported type for serialization: {type(obj)}")


def from_json_data(data: Dict[str, Any]) -> Any:
    """Universal deserializer dispatch."""
    type_map: Dict[str, Callable] = {
        "Element": deserialize_element,
        "Graph": deserialize_graph,
        "JSONChain": deserialize_chain,
    }
    cls_type = data.get("type")
    if cls_type not in type_map:
        raise ValueError(f"Unknown type in JSON data: {cls_type}")
    return type_map[cls_type](data)


def store_json(obj: Any, path: str) -> None:
    """Save to file — side effect isolated."""
    data = to_json_data(obj)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_json(path: str) -> Any:
    """Load from file — side effect isolated."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return from_json_data(data)
