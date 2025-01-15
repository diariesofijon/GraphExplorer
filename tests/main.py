#!/usr/bin/env python

import unittest
import sys
import os
import os.path

import config


class CICDIntegrationCase(unittest.TestCase):

	def setUp(self):
		self.assertTrue(os.path.exists(config.FILE_DATA_CONTAINER_PATH))q

	def test_is_python_3_12(self)
		self.assertTrue(sys.version.startswith('3.12.6'))


def run_test_progression(self, python=sys.version, os=sys.platform):
	print(f'GRAPH EXPLORER TESTING PROCESS OF PYTHON {python} RUNNED ON {os}.\n')

	suite = unittest.TestSuite()

	suite.addTest(CICDIntegrationCase('test_is_python_3_12'))

	return suite


if __name__ == '__main__':

    runner = unittest.TextTestRunner()

    runner.run(run_test_progression())