#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

here = os.path.dirname(os.path.abspath(__file__))
# get documentation from the README
try:
    with open(os.path.join(here, 'README.rst')) as doc:
        long_description = doc.read()
except:
    long_description = ''

# version
try:
    with open(os.path.join(here, 'diff_py', 'VERSION')) as f:
        version = f.readline().strip()
except:
    version = '0.0.1'

# dependencies
try:
    with open(os.path.join(here, 'diff_py', 'requirements.txt')) as f:
        deps = f.read().splitlines()
except:
    deps = ['py']

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
      package_data={'diff_py': ['diff_py/VERSION', 'diff_py/requirements.txt']},
      include_package_data=True,
      zip_safe=False,
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      diff_py = diff_py.runner:main
      """,
      install_requires=deps,
      )
