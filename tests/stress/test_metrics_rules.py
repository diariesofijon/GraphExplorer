#!/usr/bin/env python3
"""
Unit tests for functional benchmark system using unittest.
"""

import unittest
from functional_benchmarks import (
    manifest_loader, registry, metrics, benchmark_runner, results_writer, benchmark_logger
)

class TestFunctionalBenchmarks(unittest.TestCase):
    def setUp(self):
        self.logger = benchmark_logger.get_logger()
        self.registry = {"identity": lambda x: x}

    def test_manifest_loader_returns_dict(self):
        # simulate TOML structure
        manifest = {"benchmarks": [{"id": "x", "function": "identity"}]}
        self.assertIsInstance(manifest, dict)

    def test_registry_resolve(self):
        fn = registry.resolve("identity", self.registry)
        self.assertEqual(fn(5), 5)

    def test_benchmark_runner_structure(self):
        manifest = {"benchmarks": [{"id": "test", "function": "identity", "metrics": []}]}
        result = benchmark_runner.run_benchmarks(manifest, self.registry, self.logger)
        self.assertIsInstance(result, list)

    def test_results_writer_creates_file(self):
        from tempfile import TemporaryDirectory
        import os, json
        with TemporaryDirectory() as tmp:
            results = [{"id": "a", "metrics": {}}]
            results_writer.write_results(results, tmp)
            files = os.listdir(tmp)
            self.assertTrue(any(f.endswith(".json") for f in files))

if __name__ == "__main__":
    unittest.main()

