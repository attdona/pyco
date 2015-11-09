[![Build Status](https://travis-ci.org/attdona/pyco.svg?branch=master)](https://travis-ci.org/attdona/pyco)

# Pyco


The goal of Pyco project is to automates the interaction with systems and network devices with a convention over configuration approach.

Pyco is a python 3 library based on [pexpect](http://www.noah.org/wiki/pexpect) tools written by Noah Spurrier and [others contributors](WikiOthers.md).

For a quick taste this is the short story for the basic Pyco usage:

```
from pyco.device import device

myHost = device('ssh://willy:coyote@beepbeep.acme.com')

#send a shell command
output = myHost.send('uname -a') 

```

The output string is the command device response, in this case something like:

```
Linux cencenighe 2.6.32-30-generic #59-Ubuntu SMP Tue Mar 1 21:30:46 UTC 2011 x86_64 GNU/Linux
```

The device() argument follow the [URI scheme](http://en.wikipedia.org/wiki/URI_scheme) syntax and allow telnet and ssh as communication protocols.


For a detailed introduction and pyco features read the PycoUserGuide

