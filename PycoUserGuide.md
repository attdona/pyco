# pyco user guide

# Introduction #

The design driving rules of pyco are:

  * convention over configuration
  * ease of configuration when needed
  * high quality source code

The strong opinion of the pyco designer are that **test code** is more important that the application code.


# Installation #

pyco use _pexpect_ library so a Unix machine is needed. Indeed pyco integrate _winpexpect_ for windows platform but at the moment it seem not work as expected.

pyco is pure python so what you need is a python interpreter.
This first pyco version is developed and tested with python 2.7, but it is reported working with older python versions.

A python 3 porting may be put in the roadmap if interest arise.

Unpack the package and run install:

```
  > tar zxvf pyco-x.y.z.tar.gz
  > cd pyco-x.y.z
  > python setup.py install
```

Now pyco is ready to use:
```
  > python

  >>> from pyco.device import device
  >>> host = device('ssh://myUser:myPassword@hostname/ciscoios')
  >>> out = host('show version')
       go on ...
   




```