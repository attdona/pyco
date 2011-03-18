#! /usr/bin/env python

'''
Created on Mar 8, 2011

@author: tt005893
'''
# counterTest.py, a1eio

import threading
from netcube.master import *
import time  
from threadpool import *
#
import sys, time
#
from daemon import Daemon
#
 
#
class MyDaemon(Daemon):
#
    def run(self):
        main(sys.argv[2])
  
 
  
  


# create a thread object that will do the counting in a separate thread
class Counter(threading.Thread):
    def __init__(self, hostname,user,pwd,protocol):
        threading.Thread.__init__(self) # init the thread
        self.hostname = hostname # initial value
        self.user = user # amount to increment
        self.pwd = pwd # controls the while loop in the run command
        self.protocol = protocol # controls the while loop in the run command
        self.tempo_iniziale = time.time()  
        self.tempo_finale = time.time()
        
    def run(self): # this is the main function that will run in a separate thread
        doUname(self.hostname,self.user,self.pwd,self.protocol);
        self.finish()


    def finish(self): # close the thread, return final value
        print 'ended %s' % self.hostname
        self.tempo_finale = time.time()    # stop the while loop in 'run'
        print '##################' , self.hostname, str(self.tempo_finale - self.tempo_iniziale), "secondi." 
        return self.hostname # return value

def doLs(hostname,user,pwd,protocol):
    h=Linux(hostname,user,pwd,protocol);
    out=h('ls')
    
    
def doUname(hostname,user,pwd,protocol):
    h=Linux(hostname,user,pwd,protocol);
    out=h('uname -a')

def main(casestudy):
    # create separate instances of the counter
    
    print casestudy
    if casestudy=='0':
        banner('sequenziali...')
        ti = time.time()  
        doUname('163.162.155.86','tbox','qwe123','ssh');
        doUname('163.162.155.83','tbox','qwe123','ssh');
        doUname('163.162.155.76','tbox','qwe123','ssh');
        tf = time.time()
        print "Impiegati", str(tf - ti), "secondi per i sequenziali."  
        banner('fine sequenziali...')
    elif casestudy == '1':
        banner('THREADPOOL')#'
        ti = time.time()
        pool = ThreadPool(10)
        pool.add_task(doUname, '163.162.155.86','tbox','qwe123','ssh')
        pool.add_task(doUname, '163.162.155.83','tbox','qwe123','ssh')
        pool.add_task(doUname, '163.162.155.76','tbox','qwe123','ssh')
        pool.wait_completion()
        tf = time.time()
        print "Impiegati", str(tf - ti), "secondi per i THREADPOOL."
        banner('FINE THREADPOOL')
    elif casestudy == '2':
        banner('THREAD PARALLELI')#'
        counterA = Counter('163.162.155.86','tbox','qwe123','ssh') #initial value, increment
        counterB = Counter('163.162.155.83','tbox','qwe123','ssh') #initial value, increment
        counterC = Counter('163.162.155.76','tbox','qwe123','ssh') #initial value, increment
        
        # start each counter
        print 'THREAD'
        print('start A')
        counterA.start()
        print('start B')
        counterB.start()
        print('start C')
        counterC.start()
        print('started all...')
    else:
        banner('errore')
    
    
def banner(b):    
        print '####################################################################'
        print '####################################################################'
        print '####################################################################'
        print '####################################################################'
        print '#####################%s#####################################' % b
        print '####################################################################'
        print '####################################################################'
        print '####################################################################'
        print '####################################################################'

if __name__ == '__main__':
    daemon = MyDaemon('/tmp/daemon-example.pid',stdout='/tmp/pycoLog')
    if len(sys.argv) == 3:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart casestudy" % sys.argv[0]
        print "casestudy= 0|1|2   0:sequenziali; 1:THREADPOOL; 2:thread paralleli lanciati in sequenza" 
        sys.exit(2)
