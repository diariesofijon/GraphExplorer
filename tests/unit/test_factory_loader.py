#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Type, Dict

from lib.abc import AbstractLoader
from lib.protocols import ProtocolLoader
from lib.drivers import FactoryLoader


# -------------------------------
# Dummy subclasses for factory
# -------------------------------

class DummyCSVLoader(AbstractLoader):
    """Loader that pretends to load CSV files."""
    file_type = "csv"

    @property
    def whole_chain(self): return ["a,b,c"]
    @property
    def element_class(self): return str
    @property
    def chain_type(self): return list
    @property
    def ids(self): return frozenset({"a", "b", "c"})
    @property
    def map(self): return {"a": 1, "b": 2, "c": 3}

    def loads_from(self, path: str, type: str, mode: str = "r", starts: int = 0):
        return ["loaded", path]

    def convert_element(self, tmp: str): return tmp.strip()
    def chain_mapping_function(self, *args, **kwargs): return ["mapped"]
    def mapping_function(self, func, sequence): return [func(e) for e in sequence]


class DummyJSONLoader(AbstractLoader):
    """Loader that pretends to load JSON files."""
    file_type = "json"

    @property
    def whole_chain(self): return [{"id": 1}, {"id": 2}]
    @property
    def element_class(self): return dict
    @property
    def chain_type(self): return list
    @property
    def ids(self): return frozenset({1, 2})
    @property
    def map(self): return {1: {"id": 1}, 2: {"id": 2}}

    def loads_from(self, path: str, type: str, mode: str = "r", starts: int = 0):
        return [{"loaded": path}]

    def convert_element(self, tmp: str): return {"id": tmp}
    def chain_mapping_function(self, *args, **kwargs): return [{"mapped": True}]
    def mapping_function(self, func, sequence): return [func(e) for e in sequence]


# -------------------------------
# Tests
# -------------------------------

class TestProtocolLoaderRegistration(unittest.TestCase):
    def test_metaclass_registration(self):
        """Ensure subclasses are automatically registered in the loader registry."""
        registry: Dict[str, Type[AbstractLoader]] = ProtocolLoader.registry

        self.assertIn("csv", registry)
        self.assertIn("json", registry)
        self.assertTrue(issubclass(registry["csv"], AbstractLoader))
        self.assertTrue(issubclass(registry["json"], AbstractLoader))

    def test_duplicate_registration_warning(self):
        """Simulate registering the same type twice; the metaclass should handle it gracefully."""
        class DuplicateCSVLoader(DummyCSVLoader):
            pass

        registry = ProtocolLoader.registry
        self.assertIn("csv", registry)
        # Should not break existing registry consistency
        self.assertTrue(issubclass(registry["csv"], AbstractLoader))


class TestFactoryLoader(unittest.TestCase):
    def test_create_valid_loader(self):
        """Ensure FactoryLoader dynamically instantiates correct loader based on file type."""
        loader = FactoryLoader.create_loader("csv")
        self.assertIsInstance(loader, DummyCSVLoader)
        self.assertEqual(loader.file_type, "csv")

    def test_create_other_loader(self):
        loader = FactoryLoader.create_loader("json")
        self.assertIsInstance(loader, DummyJSONLoader)
        self.assertEqual(loader.file_type, "json")

    def test_invalid_loader_type(self):
        """Unknown loader type must raise a ValueError."""
        with self.assertRaises(ValueError):
            FactoryLoader.create_loader("unknown")

    def test_loader_behavior(self):
        """Check that FactoryLoader can use loader methods."""
        loader = FactoryLoader.create_loader("csv")
        res = loader.loads_from("data.csv", "csv")
        self.assertIn("loaded", res)
        mapped = loader.chain_mapping_function()
        self.assertEqual(mapped, ["mapped"])


class TestEndToEndChain(unittest.TestCase):
    def test_dynamic_resolution_and_chain_map(self):
        """End-to-end: create loader via FactoryLoader and test mapping integration."""
        loader = FactoryLoader.create_loader("json")
        ids = loader.ids
        self.assertEqual(ids, frozenset({1, 2}))
        chain = loader.whole_chain
        self.assertEqual(len(chain), 2)
        mapped = loader.mapping_function(lambda e: e["id"], chain)
        self.assertEqual(mapped, [1, 2])


if __name__ == "__main__":
    unittest.main()
