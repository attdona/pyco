import os

if 'PYCO_HOME' in os.environ:
    pyco_home = os.environ['PYCO_HOME']
else:
    print("WARNING: PYCO_HOME environment variable not defined, using current dir as PYCO_HOME") 
    pyco_home = os.curdir

 

        
