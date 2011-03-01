'''
Created on Jan 31, 2011

to start a communication a cliStart event has to be generated.

@author: adona
'''
import pexpect

class CliSession:

    def __init__(self, device):
        self.device = device




telnetClient = "telnet kabul.sodalia.it"

endpoint = pexpect.spawn(telnetClient)

endpoint.expect("login1:*", timeout = 1)

print endpoint.before


