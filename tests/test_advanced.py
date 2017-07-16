# -*- coding: utf-8 -*-

from .context import FetchPublicBlacklists  # noqa
from FetchPublicBlacklists import FetchPublicBlacklists  # noqa
from FetchPublicBlacklists import helpers  # noqa

import unittest


class AdvancedTestSuite(unittest.TestCase):
	"""Advanced test cases."""

	def test_thoughts(self):
		assert True

	def test_IPv4_vs_CIDR(self):
		"""Test IPv4 host is treated the same as a CIDR /32"""
		host_test_list = ["1.2.3.0/29", "2.2.3.1", "2.2.3.2", "2.2.3.3", "2.2.3.4", "3.3.3.3"]
		cidr_test_list = ["1.2.3.0/29", "2.2.3.1", "2.2.3.2", "2.2.3.3", "2.2.3.4", "3.3.3.3/32"]
		self.assertEqual(
			helpers.compress_ip_list_to_cidr(host_test_list),
			helpers.compress_ip_list_to_cidr(cidr_test_list)
		)

	def test_dryrun_config(self):
		"""Test dry run of tool"""
		import subprocess
		try:
			print(str(
				subprocess.check_output(
					["FetchPublicBlacklists/FetchPublicBlacklists.py", "--dry-run"]
				)
			))
		except Exception:
			subprocess.check_output(["FetchPublicBlacklists/FetchPublicBlacklists.py", "--dry-run"])
			self.assertEqual(False, True)
		self.assertEqual(True, True)


if __name__ == '__main__':
	unittest.main()
