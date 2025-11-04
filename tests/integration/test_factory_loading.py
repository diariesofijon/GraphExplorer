#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import yaml
import tempfile
import unittest
import xml.etree.ElementTree as ET

from lib.drivers import FactoryLoader


class TestFactoryLoader(unittest.TestCase):

    def setUp(self):
        self.factory = FactoryLoader()
        self.tempdir = tempfile.TemporaryDirectory()
        self.basedir = self.tempdir.name

    def tearDown(self):
        self.tempdir.cleanup()

    def make_file(self, name: str, content: str):
        """Helper: create a temporary file with content."""
        path = os.path.join(self.basedir, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_txt_loader(self):
        path = self.make_file("hello.txt", "Hello, FactoryLoader!")
        result = self.factory.load(path)
        self.assertIn("Hello, FactoryLoader!", result)

    def test_json_loader(self):
        data = {"name": "ijon", "age": 33}
        path = self.make_file("data.json", json.dumps(data))
        result = self.factory.load(path)
        self.assertEqual(result["name"], "ijon")
        self.assertEqual(result["age"], 33)

    def test_yaml_loader(self):
        data = {"lang": "python", "version": 3}
        path = self.make_file("config.yaml", yaml.dump(data))
        result = self.factory.load(path)
        self.assertEqual(result["lang"], "python")
        self.assertEqual(result["version"], 3)

    def test_xml_loader(self):
        content = "<root><child name='A'/><child name='B'/></root>"
        path = self.make_file("tree.xml", content)
        result = self.factory.load(path)
        self.assertEqual(result.tag, "root")
        children = [c.attrib["name"] for c in result]
        self.assertIn("A", children)
        self.assertIn("B", children)

    def test_unknown_extension(self):
        path = self.make_file("data.unknown", "???")
        with self.assertRaises(ValueError):
            self.factory.load(path)

    def test_registry_contains_all_loaders(self):
        """Check that MetaLoader auto-registered all loaders correctly."""
        registered = set(self.factory._registry.keys())
        expected = {"txt", "json", "yaml", "yml", "xml"}
        self.assertTrue(expected.issubset(registered),
                        f"Registry missing: {expected - registered}")


if __name__ == "__main__":
    unittest.main()
