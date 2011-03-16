#!/usr/bin/env python
import ez_setup
ez_setup.use_setuptools()

import os
from setuptools import setup



setup(name='pyco',
      version='0.1.a1',
      description='python library for network devices control and automation',
      author='adona',
      author_email='attilio.dona@gmail.com',
      url='http://code.google.com/p/pyco/',
      packages=['netcube'],
      package_dir={'': 'src'},
      install_requires = ['configobj>=4.7.0', 'docutils>=0.7', 'pexpect>=2.4', 'mako'],
      
      package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        'netcube': ['cfg/*.*']
      }

     )

