#!/usr/bin/env python

import unittest
import tempfile
import os
from lib.drivers import (
    FactoryLoader,
    YAMLLoader,
    XMLLoader,
)


import unittest
from lib.drivers import (
    FactoryLoader,
    MetaFactoryLoader,
    TextLoader,
    JSONLoader,
    CSVLoader,
)


class TestFactoryLoader(unittest.TestCase):

    def SetUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)

    def _make_file(self, name: str, content: str):
        path = os.path.join(self.tmpdir.name, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_registry_contains_loaders(self):
        """Check loaders are auto-registered in LoaderMeta."""
        self.assertIn("txt", LoaderMeta._registry)
        self.assertIn("json", LoaderMeta._registry)
        self.assertIs(LoaderMeta._registry["txt"], TextLoader)
        self.assertIs(LoaderMeta._registry["json"], JSONLoader)

    def test_text_loader_via_factory(self):
        """FactoryLoader should pick TextLoader automatically."""
        path = self._make_file("example.txt", "line1\nline2\n")
        loader = FactoryLoader()
        data = loader.loads_from(path, "txt")

        self.assertEqual(data, ["line1", "line2"])
        self.assertEqual(loader.map, {0: "line1", 1: "line2"})
        self.assertEqual(loader.ids, {0, 1})

    def test_json_loader_via_factory(self):
        """FactoryLoader should pick JSONLoader automatically."""
        path = self._make_file("graph.json", json.dumps([{"id": 1}, {"id": 2}]))
        loader = FactoryLoader()
        data = loader.loads_from(path, "json")

        self.assertEqual(data, [{"id": 1}, {"id": 2}])
        self.assertEqual(loader.map[0], {"id": 1})
        self.assertEqual(loader.ids, {0, 1})

    def test_invalid_extension_raises(self):
        """FactoryLoader should raise on unknown extension."""
        loader = FactoryLoader()
        with self.assertRaises(ValueError):
            loader.loads_from("data.unknown", "unknown")

    def test_txt_loader_dispatch(self):
        loader = FactoryLoader.create("txt")
        self.assertIsInstance(loader, TextLoader)

    def test_json_loader_dispatch(self):
        loader = FactoryLoader.create("json")
        self.assertIsInstance(loader, JSONLoader)

    def test_unknown_loader_raises(self):
        with self.assertRaises(ValueError):
            FactoryLoader.create("xml")


class TestMetaLoader(unittest.TestCase):

    def test_registry_contains_builtin_loaders(self):
        """Check that metaclass auto-registered loaders into the registry."""
        self.assertIn("txt", MetaLoader._registry)
        self.assertIn("json", MetaLoader._registry)
        self.assertIs(MetaLoader._registry["txt"], TextLoader)
        self.assertIs(MetaLoader._registry["json"], JSONLoader)

    def test_dynamic_loader_registration(self):
        """Defining a new loader dynamically should register it via MetaLoader."""

        class DummyLoader(metaclass=MetaLoader):

            extension = "dummy"

            def loads_from(self, path, type, mode="r", starts=0): 
                return "ok"

            def convert_element(self, tmp):
                return tmp

            def chain_mapping_fuction(self, *args, **kwargs):
                return args

            def mapping_fuction(self, func, sequence):
                return list(map(func, sequence))

            @property
            def whole_chain(self):
                return []

            @property
            def element_class(self):
                return str

            @property
            def chain_type(self):
                return list

            @property
            def ids(self):
                return set()

            @property
            def map(self):
                return {}

        # Registry check
        self.assertIn("dummy", MetaLoader._registry)
        self.assertIs(MetaLoader._registry["dummy"], DummyLoader)

        # Ensure FactoryLoader can now use it
        loader = FactoryLoader.create("dummy")
        self.assertIsInstance(loader, DummyLoader)
        self.assertEqual(loader.loads_from("x", "t"), "ok")

    def test_class_metaclass_identity(self):
        """Ensure that loaders are using MetaLoader as their metaclass."""
        self.assertIs(type(TextLoader), MetaLoader)
        self.assertIs(type(JSONLoader), MetaLoader)


class TestMetaFactoryLoaderRegistry(unittest.TestCase):

    def test_registered_extensions(self):
        """Check that all loaders registered their extensions."""
        exts = MetaFactoryLoader.list_registered()
        self.assertIn("txt", exts)
        self.assertIn("log", exts)   # alias of TextLoader
        self.assertIn("json", exts)
        self.assertIn("csv", exts)
        self.assertIn("tsv", exts)

    def test_list_loaders_mapping(self):
        """Verify that list_loaders returns correct mapping."""
        mapping = MetaFactoryLoader.list_loaders()
        self.assertIs(mapping["txt"], TextLoader)
        self.assertIs(mapping["log"], TextLoader)
        self.assertIs(mapping["json"], JSONLoader)
        self.assertIs(mapping["csv"], CSVLoader)
        self.assertIs(mapping["tsv"], CSVLoader)

    def test_get_loader_class(self):
        """Check direct loader class retrieval by extension."""
        self.assertIs(MetaFactoryLoader.get_loader_class("json"), JSONLoader)
        self.assertIs(MetaFactoryLoader.get_loader_class("TXT"), TextLoader)  # case-insensitive
        self.assertIs(MetaFactoryLoader.get_loader_class("tsv"), CSVLoader)
        self.assertIsNone(MetaFactoryLoader.get_loader_class("xml"))


class TestFactoryLoaderIntegration(unittest.TestCase):

    def test_create_txt_loader(self):
        loader = FactoryLoader.create("txt")
        self.assertIsInstance(loader, TextLoader)

    def test_create_json_loader(self):
        loader = FactoryLoader.create("json")
        self.assertIsInstance(loader, JSONLoader)

    def test_create_csv_and_tsv_loader(self):
        csv_loader = FactoryLoader.create("csv")
        tsv_loader = FactoryLoader.create("tsv")
        self.assertIsInstance(csv_loader, CSVLoader)
        self.assertIsInstance(tsv_loader, CSVLoader)

    def test_from_path_resolves_extension(self):
        loader = FactoryLoader.from_path("data.json")
        self.assertIsInstance(loader, JSONLoader)

    def test_from_path_with_unknown_ext_raises(self):
        with self.assertRaises(ValueError):
            FactoryLoader.from_path("file.unknown")

    def test_create_with_unknown_ext_raises(self):
        with self.assertRaises(ValueError):
            FactoryLoader.create("unknown")


class TestYAMLAndXMLLoaders(unittest.TestCase):

    def test_yaml_loader(self):
        loader = FactoryLoader.create("yaml")
        self.assertIsInstance(loader, YAMLLoader)

        sample = {"a": 1, "b": [2, 3]}
        with tempfile.NamedTemporaryFile("w+", suffix=".yaml", delete=False) as f:
            import yaml
            yaml.safe_dump(sample, f)
            fname = f.name

        loaded = loader.loads_from(fname, "yaml")
        self.assertEqual(loaded, sample)
        os.remove(fname)

    def test_xml_loader(self):
        loader = FactoryLoader.create("xml")
        self.assertIsInstance(loader, XMLLoader)

        sample_xml = "<root><child id='1'>test</child></root>"
        with tempfile.NamedTemporaryFile("w+", suffix=".xml", delete=False) as f:
            f.write(sample_xml)
            fname = f.name

        root = loader.loads_from(fname, "xml")
        self.assertEqual(root.tag, "root")
        self.assertEqual(root[0].tag, "child")
        os.remove(fname)


if __name__ == "__main__":
    unittest.main()
