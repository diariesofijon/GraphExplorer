#!/usr/bin/env python

import unittest
import sys
import os
import os.path
from string import Template

import config
import fixtures
from lib import masks


class CICDIntegrationCase(unittest.TestCase):

    def setUp(self):
        self.assertTrue(os.path.exists(config.FILE_DATA_CONTAINER_PATH))

    def test_is_python_3_12(self):
        self.assertTrue(sys.version.startswith('3.12.6'))

    def test_is_support_this_LTS(self):
        # Check LTS for this platform
        version_check = sys.version.startswith("3.12")  # Loosened to major.minor
        platform_template = Template(
            "Platform: $platform does not meet LTS requirement (running $version)"
        )
        if sys.platform in ("win32", "linux", "darwin"):
            self.assertTrue(
                version_check,
                platform_template.substitute(
                    platform=sys.platform, version=sys.version)
            )
        else:
            self.fail("Platform is unavailable to use")

    def test_is_assets_exists(self):
        self.assertTrue(os.path.exists(config.FILE_DATA_LOADER_PATH))
        self.assertTrue(os.path.exists(config.FILE_DATA_OUTLOADER_PATH_CSV))
        self.assertTrue(os.path.exists(config.FILE_DATA_OUTLOADER_PATH_JSON))

class MathUnitCase(unittest.TestCase):
    pass

class DiscreteMatrixUnitCase(MathUnitCase):
    pass

class DiscreteGraphUnitCase(MathUnitCase):
    pass


def run_test_progression(self, python=sys.version, os=sys.platform):
    print(f'GRAPH EXPLORER TESTING PROCESS OF PYTHON {python} RUNNED ON {os}.\n')

    suite = unittest.TestSuite()

    suite.addTest(CICDIntegrationCase('test_is_python_3_12'))
    suite.addTest(CICDIntegrationCase('test_is_support_this_LTS'))
    suite.addTest(CICDIntegrationCase('test_is_assets_exists'))

    return suite

# class TestFormatters(unittest.TestCase):
#     def test_basic_formatter_removes_comments_and_spaces(self):
#         text = "A -> B , C\n# comment\n\nB->C"
#         fmt = drivers.BasicTextFormatter()
#         result = fmt.format(text)
#         self.assertEqual(result, "A->B , C\nB->C")

# class TestDrivers(unittest.TestCase):
#     def test_text_driver_loads_graph(self):
#         text = "A->B,C\nB->C"
#         graph = drivers.TextGraphDriver().load(text)
#         self.assertEqual(graph, {"A": ["B", "C"], "B": ["C"]})

#     def test_json_driver_loads_graph(self):
#         data = {"A": ["B"], "B": ["C"]}
#         graph = drivers.JsonDriver().load(data)
#         self.assertEqual(graph, {"A": ["B"], "B": ["C"]})

class TestMasks(unittest.TestCase):
    def test_node_whitelist_mask(self):
        mask = masks.NodeWhitelistMask({"A"})
        self.assertTrue(mask.allow_node("A"))
        self.assertFalse(mask.allow_node("B"))

    def test_edge_weight_mask(self):
        weights = {("A","B"): 2}
        mask = masks.EdgeWeightMask(1, weights)
        self.assertTrue(mask.allow_edge("A","B"))
        self.assertFalse(mask.allow_edge("A","C"))

    def test_composite_mask(self):
        mask1 = masks.NodeWhitelistMask({"A"})
        mask2 = masks.NodeWhitelistMask({"B"})
        comp = masks.CompositeMask(mask1, mask2)
        self.assertFalse(comp.allow_node("A"))
        self.assertFalse(comp.allow_node("B"))

class TestBaseGraphMask(unittest.TestCase):
    def setUp(self):
        self.graph = {"A": ["B"], "B": ["C"], "C": []}
        self.bg = masks.BaseGraphMask(self.graph)

    def test_len_and_contains(self):
        self.assertEqual(len(self.bg), 3)
        self.assertIn("A", self.bg)
        self.assertNotIn("X", self.bg)

    def test_getitem_and_iteration(self):
        self.assertEqual(self.bg["A"], ["B"])
        nodes = list(iter(self.bg))
        self.assertEqual(set(nodes), {"A", "B", "C"})

    def test_dfs(self):
        visited = self.bg.dfs("A")
        self.assertEqual(visited, {"A", "B", "C"})

class TestShortcuts(unittest.TestCase):
    def test_from_text(self):
        text = "A->B,B\nB->C"
        g = fixtures.from_text(text)
        self.assertEqual(g.dfs("A"), {"A", "B", "C"})

    def test_from_json(self):
        data = {"A": ["B"], "B": ["C"]}
        g = fixtures.from_json(data)
        self.assertEqual(g.dfs("A"), {"A", "B", "C"})

    def test_with_masks(self):
        m = fixtures.with_masks(masks.NoMask(), masks.NoMask())
        self.assertTrue(m.allow_node("A"))
        self.assertTrue(m.allow_edge("A","B"))



if __name__ == '__main__':

    runner = unittest.TextTestRunner()

    runner.run(run_test_progression())
