# -*- coding: utf-8 -*-

from .context import code
from code import core
from code import helpers

import unittest


class AdvancedTestSuite(unittest.TestCase):
	"""Advanced test cases."""

	def test_thoughts(self):
		assert True

if __name__ == '__main__':
	unittest.main()
