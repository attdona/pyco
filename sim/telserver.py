#!/usr/bin/env python3

"""
simple telnet server simulator
"""

import logging
import sys
import os
import re
import argparse
from miniboa import TelnetServer
import pytoml as toml
import socket
import threading
import socketserver

IDLE_TIMEOUT = 300
CLIENT_LIST = []
SERVER_RUN = True

OOB_PORT = 7778


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = str(self.request.recv(1024), 'ascii')
        cur_thread = threading.current_thread()
        
        print("RCV: %s" % data)
        r = re.match("__face__ (\w+)", data)
        if (r):
            simulator_face(r.group(1))

        #response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
        #self.request.sendall(response)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def simulator_face(cfgfile):
    global config

    cwd = os.path.dirname(os.path.realpath(__file__))
    f = os.path.join(cwd, cfgfile + '.cfg')

    if (os.path.isfile(f)):
        with open(f, 'rb') as f:
            config = toml.load(f)
            config['datadir'] = os.path.join(cwd, 'data', cfgfile)
    else:
        print("not found config file [%s], simulator not changed" % f)


def reset(client):
    global login_count
    
    client.active = False
    

def on_connect(client):
    """
    Sample on_connect function.
    Handles new connections.
    """
    global config

    logging.info("Opened connection to {}".format(client.addrport()))
    #broadcast("{} joins the conversation.\n".format(client.addrport()))
    CLIENT_LIST.append(client)

    client.send(config['banner'])
    #client.send("Welcome to the Chat Server, {}.\n".format(client.addrport()))

    client.send(config['LOGIN']['response'])

def on_disconnect(client):
    """
    Sample on_disconnect function.
    Handles lost connections.
    """
    logging.info("Lost connection to {}".format(client.addrport()))
    CLIENT_LIST.remove(client)
    #broadcast("{} leaves the conversation.\n".format(client.addrport()))


def kick_idle():
    """
    Looks for idle clients and disconnects them by setting active to False.
    """
    # Who hasn't been typing?
    for client in CLIENT_LIST:
        if client.idle() > IDLE_TIMEOUT:
            logging.info("Kicking idle lobby client from {}".format(client.addrport()))
            client.active = False



def process_clients():
    """
    Check each client, if client.cmd_ready == True then there is a line of
    input available via client.get_command().
    """
    global SERVER_RUN, config

    for client in CLIENT_LIST:
        if client.active and client.cmd_ready:
            msg = client.get_command()
            #print("--> %s" % msg)

            if (not hasattr(client, 'status')):
                client.status = 'LOGIN'
                client.failed_logins = 0
                
            if (client.status == 'LOGIN'):
                config['username'] = msg
                print("login username: " + config['username'])
                client.status = config['LOGIN']['next_status']

            elif (client.status == 'PASSWD'):
                if (config[client.status]['password'] == msg):
                    client.status = config[client.status]['next_status']
                    client.send(config[client.status]['response'])
                    break
                elif (client.failed_logins == 1):
                    reset(client)
                else:
                    client.send('\nLogin incorrect\n')
                    client.status = 'LOGIN'
                    client.failed_logins += 1
                    
            sts = client.status
            if ('commands' in config[sts] and msg in config[sts]['commands']):
                client.send(config[sts]['commands'][msg] + "\n")
            elif (os.path.isfile(os.path.join(config["datadir"], msg))):
                with open (os.path.join(config["datadir"], msg), "r") as myfile:
                    data=myfile.read()
                    client.send(data)
            client.send(config[sts]['response'])
                
            cmd = msg.lower()
            # bye = disconnect
            if cmd == 'exit':
                reset(client)
            # shutdown == stop the server
            elif cmd == 'shutdown':
                SERVER_RUN = False
            else:
                r = re.match("__face__ (\w+)", cmd)
                if (r):
                    simulator_face(r.group(1))



def broadcast(msg):
    """
    Send msg to every client.
    """
    for client in CLIENT_LIST:
        client.send(msg)


if __name__ == '__main__':

    # Simple chat server to demonstrate connection handling via the
    # async and telnet modules.
    parser = argparse.ArgumentParser()
    parser.add_argument("cfg_file", help="simulator config file")
    parser.add_argument("--port", help="telnet port", type=int, default=7777)
    args = parser.parse_args()
    
    cwd = os.path.dirname(os.path.realpath(__file__))
    
    logging.basicConfig(level=logging.DEBUG)

    with open(os.path.join(cwd,args.cfg_file + '.cfg'), 'rb') as f:
        config = toml.load(f)

    config['datadir'] = os.path.join(cwd, 'data', args.cfg_file)

    oob_server = ThreadedTCPServer(("localhost", OOB_PORT), ThreadedTCPRequestHandler)
    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=oob_server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)

       
    #print(config['commands'].keys())

    # Create a telnet server with a port, address,
    # a function to call with new connections
    # and one to call with lost connections.

    telnet_server = TelnetServer(
        port=args.port,
        address='',
        on_connect=on_connect,
        on_disconnect=on_disconnect,
        timeout = .05
        )



    logging.info("Listening for connections on port {}. CTRL-C to break.".format(telnet_server.port))

    # Server Loop
    while SERVER_RUN:
        telnet_server.poll()        # Send, Recv, and look for new connections
        kick_idle()                 # Check for idle clients
        process_clients()           # Check for client input

    logging.info("Server shutdown.")
