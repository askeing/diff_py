import os
from setuptools import setup, find_packages

# get documentation from the README
here = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(here, 'README.rst')) as f:
        description = f.read()
except:
    description = ''

# version
try:
    with open('diff_py' + os.sep + 'VERSION') as f:
        version = f.readline()
except:
    version = '0.0.1'

# dependencies
try:
    with open('diff_py' + os.sep + 'requirements.txt') as f:
        deps = f.read().splitlines()
except:
    deps = []

setup(name='diff_py',
      version=version,
      description='The simple diff tool which is written by Python. The diff result can be printed in console or to html file.',
      long_description=description,
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
