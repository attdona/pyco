'''
Created on Jan 31, 2011

@author: adona
'''

from netcube.common import Common


class Linux(Common):
    '''
    classdocs
    '''
    def __init__(self, name, username = None, password = None, protocol='ssh', hops = []):
        Common.__init__(self, name, username, password, protocol, hops)

        
        