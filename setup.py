#!/usr/bin/env python

from distutils.core import setup

setup(name='pyco',
      version='1.10',
      description='Python Distribution Utilities',
      author='Greg Ward',
      author_email='gward@python.net',
      url='http://www.python.org/sigs/distutils-sig/',
      packages=['netcube'],
      package_dir={'netcube': 'src/netcube'},
      package_data={'cfg': ['cfg/*.*']},

     )

