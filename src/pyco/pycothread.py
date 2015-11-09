#! /usr/bin/env python

'''

@author: Attilio Dona' (attdona)
'''

import threading
import time  
from pyco.threadpool import *

import sys, time

from pyco.daemon import Daemon
from pyco.device import device


class MyDaemon(Daemon):

    def run(self):
        main()
  

def doLs(hostname,user,pwd,protocol):
    h=Linux(hostname,user,pwd,protocol);
    out=h('ls')
    
    
def doUname(hostname,user,pwd,protocol):
    print("doUname")
    h=device("%s://%s:%s@%s:7777" % (protocol,user,pwd,hostname))
    out=h('uname -a')

def main():

    ti = time.time()
    pool = ThreadPool(10)
    pool.add_task(doUname,'localhost','xxxx','secret','telnet')
    pool.add_task(doUname,'localhost','xxxx','secret','telnet')
    pool.add_task(doUname,'localhost','xxxx','secret','telnet')
    pool.wait_completion()
    tf = time.time()
    print("Impiegati", str(tf - ti), "secondi per i THREADPOOL.")
    
    
def deamoniac(cmd):
    daemon = MyDaemon('/tmp/daemon-example.pid',stdout='/tmp/pycoLog', stderr='/tmp/pycoLog')

    if 'start' == cmd:
        daemon.start()
    elif 'stop' == cmd:
        daemon.stop()
    elif 'restart' == cmd:
        daemon.restart()
    else:
        print("Unknown command")
        sys.exit(2)
    sys.exit(0)

if __name__ == '__main__':
    
    if len(sys.argv) == 1:
        main()
    
    elif len(sys.argv) == 2:
        deamoniac(sys.argv[1])
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
