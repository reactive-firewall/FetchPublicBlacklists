# -*- coding: utf-8 -*-

try:
	from setuptools import setup
	from setuptools import find_packages
except Exception:
	raise ImportError("""Not Implemented.""")

try:
	with open("""./requirements.txt""") as f:
		requirements = f.read().splitlines()
except Exception:
	requirements = None

try:
	with open("""./README.rst""") as f:
		readme = f.read()
except Exception:
	readme = str("""See https://github.com/reactive-firewall/FetchPublicBlacklists/README.rst""")

try:
	with open("""./LICENSE""") as f:
		license = f.read()
except Exception:
	license = str("""See https://github.com/reactive-firewall/FetchPublicBlacklists/LICENSE""")

setup(
	name='Fetch Public Blacklists',
	version='0.3.3',
	description='Fetch Public Blacklists scripts',
	long_description=readme,
	author='reactive-firewall',
	author_email='reactive-firewall@users.noreply.github.com',
	url='https://github.com/reactive-firewall/FetchPublicBlacklists.git',
	license=license,
	packages=find_packages(exclude=('tests', 'docs'))
)

