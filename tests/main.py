#!/usr/bin/env python

import unittest
import sys
import os
import os.path

import config


class CICDIntegrationCase(unittest.TestCase):

    def setUp(self):
        self.assertTrue(os.path.exists(config.FILE_DATA_CONTAINER_PATH))

    def test_is_python_3_12(self):
        self.assertTrue(sys.version.startswith('3.12.6'))

    def test_is_support_this_LTS(self):
        # checking LTS for this platform
        match sys.platform:
            case 'win32':
                self.assertTrue(sys.version.startswith('3.12.6')
            case 'linux':
                self.assertTrue(sys.version.startswith('3.12.6')
            case 'darwin':
                self.assertTrue(sys.version.startswith('3.12.6')
            case _:
                assert 'Platform is unavailable to use'

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


if __name__ == '__main__':

    runner = unittest.TextTestRunner()

    runner.run(run_test_progression())