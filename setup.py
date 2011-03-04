#!/usr/bin/env python

from distutils.core import setup

setup(name='pyco',
      version='1.10',
      description='python library for network devices control and automation',
      author='adona',
      #author_email='gward@python.net',
      url='http://code.google.com/p/pyco/',
      packages=['netcube'],
      package_dir={'netcube': 'src/netcube'},
      package_data={'cfg': ['cfg/*.*']},

     )

