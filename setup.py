#!/usr/bin/env python
import ez_setup
ez_setup.use_setuptools()

import os
import sys
from setuptools import setup, find_packages

if sys.platform != 'win32':
    expect = 'pexpect>=4.0.1'
else:
    expect = 'winpexpect'


setup(name='pyco',
      version='0.3.0',
      description='python library for network devices control and automation',
      author='adona',
      author_email='attilio.dona@gmail.com',
      url='http://code.google.com/p/pyco/',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      install_requires = ['configobj>=4.7.0', 
                          'docutils>=0.7',
                           expect,
                           'mako',
                           'sqlalchemy', 'zope.sqlalchemy', 'transaction'],
      
      package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        'pyco': ['cfg/*.*']
      },
      
      entry_points="""
        [pyco.plugin]
            auth=pyco.device:getAccount
        """


     )

