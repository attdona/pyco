import pytoml as toml
import signal
import subprocess

from pyco.device import device

import time

try:
    sig = signal.CTRL_C_EVENT
except AttributeError:
    sig = signal.SIGTERM

class Process:
	pass

def setup():
	print("starting ... {0}".format(sig))
	Process.p = subprocess.Popen(['./telserver.py'])
	print("started with pid {0}".format(Process.p))

def tearDown():
	print("stopping ...")
	Process.p.send_signal(sig)

def read_test():
	with open('sim.cfg', 'rb') as f:
		obj = toml.load(f)

	print(obj['commands'].keys())
	time.sleep(1)