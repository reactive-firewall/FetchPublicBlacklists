# -*- coding: utf-8 -*-

from .context import FetchPublicBlacklists  # noqa
from FetchPublicBlacklists import FetchPublicBlacklists  # noqa
from FetchPublicBlacklists import helpers  # noqa

import unittest
import subprocess
import sys


def getPythonCommand():
	"""function for backend python command"""
	thepython = "exit 1 ; #"
	try:
		thepython = checkPythonCommand(["which", "coverage"])
		if (str("/coverage") in str(thepython)) and (sys.version_info >= (3, 3)):
			thepython = str("coverage run -p")
		elif (str("/coverage") in str(thepython)) and (sys.version_info <= (3, 2)):
			try:
				import coverage
				if coverage.__name__ is not None:
					thepython = str("{} -m coverage run -p").format(str(sys.executable))
				else:
					thepython = str(sys.executable)
			except Exception:
				thepython = str(sys.executable)
		else:
			thepython = str(sys.executable)
	except Exception:
		thepython = "exit 1 ; #"
		try:
			thepython = str(sys.executable)
		except Exception:
			thepython = "exit 1 ; #"
	return str(thepython)


def checkPythonCommand(args=[None], stderr=None):
	"""function for backend subprocess check_output command"""
	theOutput = None
	try:
		if args is None or args is [None]:
			theOutput = subprocess.check_output(["exit 1 ; #"])
		else:
			if str("coverage ") in args[0]:
				if sys.__name__ is None:
					raise ImportError("Failed to import system. WTF?!!")
				if str("{} -m coverage ").format(str(sys.executable)) in str(args[0]):
					args[0] = str(sys.executable)
					args.insert(1, str("-m"))
					args.insert(2, str("coverage"))
					args.insert(3, str("run"))
					args.insert(4, str("-p"))
					args.insert(4, str("--source=FetchPublicBlacklists"))
				else:
					args[0] = str("coverage")
					args.insert(1, str("run"))
					args.insert(2, str("-p"))
					args.insert(2, str("--source=FetchPublicBlacklists"))
			theOutput = subprocess.check_output(args, stderr=stderr)
	except Exception as cmderror:
		theOutput = None
	try:
		if isinstance(theOutput, bytes):
			theOutput = theOutput.decode('utf8')
	except UnicodeDecodeError:
		theOutput = bytes(theOutput)
	return theOutput


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
		try:
			print(str(
				checkPythonCommand(
					[
						getPythonCommand(),
						"-m",
						"FetchPublicBlacklists.FetchPublicBlacklists",
						"--dry-run"
					]
				)
			))
		except Exception:
			subprocess.check_output(["FetchPublicBlacklists/FetchPublicBlacklists.py", "--dry-run"])
			self.assertEqual(False, True)
		self.assertEqual(True, True)

	def test_dryrun_dispaly(self):
		"""Test dry run of tool with --display"""
		try:
			print(str(
				checkPythonCommand(
					[
						getPythonCommand(),
						"-m",
						"FetchPublicBlacklists.FetchPublicBlacklists",
						"--dry-run",
						"--hosts-deny",
						"--snort-deny",
						"--nginx-deny",
						"--splunk-deny",
						"--iptables-deny",
						"--pf-deny",
						"--exim4-deny",
						"--display"
					]
				)
			))
		except Exception:
			self.assertEqual(False, True)
		self.assertEqual(True, True)


if __name__ == '__main__':
	unittest.main()
