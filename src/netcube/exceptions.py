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

