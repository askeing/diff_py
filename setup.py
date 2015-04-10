#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

# get documentation from the README
long_description = ''
with open('README.rst') as doc:
    long_description = doc.read()

# version
version = '0.0.1'
with open('diff_py' + os.sep + 'VERSION') as f:
    version = f.readline().strip()

# dependencies
deps = []
with open('diff_py' + os.sep + 'requirements.txt') as f:
    deps = f.read().splitlines()

setup(name='diff_py',
      version=version,
      description='The simple diff tool which is written by Python. The diff result can be printed in console or to html file.',
      long_description=long_description,
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='diff html ',
      author='Askeing Yen',
      author_email='askeing@gmail.com',
      url='http://www.github.com/askeing/diff_py',
      license='MPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      diff_py = diff_py.runner:main
      """,
      install_requires=deps,
      )
