'''
A device automation patterns library 
'''
import os

if 'PYCO_HOME' in os.environ:
    pyco_home = os.environ['PYCO_HOME']
else:
    pyco_home = os.environ['HOME']
