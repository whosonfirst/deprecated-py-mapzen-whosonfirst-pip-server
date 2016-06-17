#!/usr/bin/env python

import os, sys
from shutil import rmtree

cwd = os.path.dirname(os.path.realpath(sys.argv[0]))
egg_info = cwd + "/mapzen.whosonfirst.pip.server.egg-info"
if os.path.exists(egg_info):
    rmtree(egg_info)

from setuptools import setup, find_packages

packages = find_packages()
desc = open("README.md").read(),
version = open("VERSION").read()

setup(
    name='mapzen.whosonfirst.pip.server',
    namespace_packages=['mapzen', 'mapzen.whosonfirst', 'mapzen.whosonfirst.pip', 'mapzen.whosonfirst.pip.server'],
    version=version,
    description='Python utilities for working with the go-whosonfirst-pip pip and proxy servers',
    author='Mapzen',
    url='https://github.com/mapzen/py-mapzen-whosonfirst-pip-server',
    install_requires=[
        ],
    dependency_links=[
        ],
    packages=packages,
    scripts=[
        ],
    download_url='https://github.com/mapzen/py-mapzen-whosonfirst-pip-server/releases/tag/' + version,
    license='BSD')
