# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sample',
    version='0.2.0',
    description='Fetch Public Blaklists scripts',
    long_description=readme,
    author='reactive-firewall',
    author_email='reactive-firewall@users.noreply.github.com',
    url='https://github.com/reactive-firewall/FetchPublicBlacklists.git',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

