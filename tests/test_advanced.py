# -*- coding: utf-8 -*-

from .context import code
from code import core
from code import helpers

import unittest


class AdvancedTestSuite(unittest.TestCase):
	"""Advanced test cases."""

	def test_thoughts(self):
		assert True

        def test_IPv4_vs_CIDR(self):
                """Test IPv4 host is treated the same as a CIDR /32"""
		host_test_list = ["1.2.3.0/29", "2.2.3.1", "2.2.3.2", "2.2.3.3", "2.2.3.4", "3.3.3.3"]
		cidr_test_list = ["1.2.3.0/29", "2.2.3.1", "2.2.3.2", "2.2.3.3", "2.2.3.4", "3.3.3.3/32"]
		self.assertEqual(helpers.compress_ip_list_to_cidr(host_test_list), helpers.compress_ip_list_to_cidr(cidr_test_list))
if __name__ == '__main__':
	unittest.main()
