#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Fetch Public Blacklists
# ......................................................................
# Copyright (c) 2016-2017, Kendrick Walls
# ......................................................................
# Licensed under MIT (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# ......................................................................
# http://www.github.com/reactive-firewall/FetchPublicBlacklists/LICENSE
# ......................................................................
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ......................................................................

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
	with open("""./LICENSE.rst""") as f:
		license = f.read()
except Exception:
	license = str("""See https://github.com/reactive-firewall/FetchPublicBlacklists/LICENSE""")

try:
	class_tags = [
		str("""Development Status :: 4 - Beta"""),
		str("""Operating System :: POSIX :: Linux"""),
		str("""Programming Language :: Python"""),
		str("""Programming Language :: Python :: 3.7"""),
		str("""Programming Language :: Python :: 3.6"""),
		str("""Programming Language :: Python :: 3.5"""),
		str("""Programming Language :: Python :: 3.4"""),
		str("""Programming Language :: Python :: 3.3"""),
		str("""Programming Language :: Python :: 3.2"""),
		str("""Programming Language :: Python :: 2.7"""),
		str("""Topic :: Security""")
	]
except Exception:
	class_tags = str("""Development Status :: 4 - Beta""")

setup(
	name="""FetchPublicBlackists""",
	version="""0.3.3""",
	description="""A Tool for downloading public blacklists""",
	long_description=readme,
	install_requires=requirements,
	author="""reactive-firewall""",
	author_email="""reactive-firewall@users.noreply.github.com""",
	classifiers=class_tags,
	url="""https://github.com/reactive-firewall/FetchPublicBlacklists.git""",
	license=license,
	packages=find_packages(exclude=("""tests""", """docs""")),
)

