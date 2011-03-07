#!/usr/bin/env python
import os
from setuptools import setup



setup(name='pyco',
      version='0.1',
      description='python library for network devices control and automation',
      author='adona',
      author_email='gward@python.net',
      url='http://code.google.com/p/pyco/',
      packages=['netcube'],
      package_dir={'netcube': 'src/netcube'},
      package_data={'cfg': ['cfg/*.*']},
      install_requires = ["configobj>=4.7.2"],
     )

