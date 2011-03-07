'''
Created on Feb 24, 2011

@author: adona
'''

class NetworkException(Exception):
    
    def __init__(self, device):
        self.device = device
        self.response = device.esession.pipe.before

    def __str__(self):
        errInfo =  "%s\n\n%s" % (self.device.name, self.response)
        return errInfo

class ConnectionClosed(NetworkException):
    '''
    Raised when EOF is read from a pexpect child. This usually means the child has exited
    '''
    pass

class ConnectionRefused(NetworkException):
    '''
    Thrown when the connection was refused by the remote endpoint
    '''
    def __init__(self, device):
        NetworkException.__init__(self, device)
        device.close()

class PermissionDenied(NetworkException):
    '''
    Thrown when the connection is unauthorized (wrong username(/password)
    '''
    def __init__(self, device):
        NetworkException.__init__(self, device)
        device.close()


class ConnectionTimedOut(NetworkException):
    '''
    Thrown when the connection timed out expecting a pattern match
    '''
    pass

class AuthenticationFailed(NetworkException):
    '''
    Thrown when the connection timed out expecting a pattern match
    '''
    pass


class EventHandlerUndefined(Exception):
    '''
    Thrown when an event action is undefined
    '''
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return "event handler %s not defined" % self.value
    


class ConfigFileError(Exception):
    '''
    Thrown when the pyco config file is invalid
    '''
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
