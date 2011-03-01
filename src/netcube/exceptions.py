'''
Created on Feb 24, 2011

@author: adona
'''
class ConnectionClosed(Exception):
    '''
    Raised when EOF is read from a pexpect child. This usually means the child has exited
    '''
    pass

class ConnectionTimedOut(Exception):
    '''
    Thrown when the connection timed out expecting a pattern match
    '''
    pass

class AuthenticationFailed(Exception):
    '''
    Thrown when the connection timed out expecting a pattern match
    '''
    pass

class ConfigFileError(Exception):
    '''
    Thrown when the pyco config file is invalid
    '''
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
